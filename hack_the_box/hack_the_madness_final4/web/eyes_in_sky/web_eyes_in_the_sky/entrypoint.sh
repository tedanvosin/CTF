#!/bin/sh

generate_random() {
    length=$1
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $length | head -n 1
}

export ADMIN_PASSWORD=$(generate_random 16)

cat > /app/.env << EOF
ADMIN_PASSWORD=$ADMIN_PASSWORD
FLAG=HTB{FAKE_FLAG_FOR_TESTING}
EOF

/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf