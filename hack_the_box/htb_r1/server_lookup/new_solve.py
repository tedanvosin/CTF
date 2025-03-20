from scapy.all import *

def main():

    source_ip = '192.168.1.180'
    pcap_file = 'capture.pcap'

    dns_queries = ""
    
    # Read the pcap file
    packets = rdpcap(pcap_file)
    out = b''
    # Iterate through each packet
    for packet in packets:
        # Check if packet has IP layer and source IP matches
        if IP in packet and packet[IP].src == source_ip:
            # Check if packet has DNS layer and a query
            if DNS in packet and packet[DNS].qr == 1:  # 0 means query (not response)
                # Extract the query name
                if packet[DNS].qd:
                    query_name = packet[DNS].qd.qname.decode('utf-8')
                    
                    #print(query_name[:-1])
                    #print(bytes.fromhex(query_name[:-1]))
                    
                    out += bytes.fromhex(query_name[:-1])

    #print(out.decode())

    out = out.split(b'\n')
    #print(out)
    with open('attachment','wb') as f:
        for i in out:
            try:
                if len(i) < 56:
                    continue
                i = base64.b64decode(i)
                print(i)
                f.write(i)
            except:
                pass

if __name__ == "__main__":
    main()

