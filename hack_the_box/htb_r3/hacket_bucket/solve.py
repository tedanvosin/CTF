#!/usr/bin/env python3

from scapy.all import *
import argparse
import sys
import gzip

def analyze_pcap(pcap_file):
    """
    Opens a PCAP file and prints the contents of all packets
    
    Parameters:
    pcap_file (str): Path to the PCAP file
    """
    try:
        # Read the pcap file
        print(f"Reading PCAP file: {pcap_file}")
        packets = rdpcap(pcap_file)
        
        # Print summary of the capture
        print(f"\nCapture Summary:")
        print(f"Total packets: {len(packets)}")
        
        # Print detailed contents of each packet
        for i, packet in enumerate(packets):
            
            print(f"\n{'='*80}")
            print(f"Packet {i+1}/{len(packets)}")
            print(f"{'='*80}")
            
            # Print packet summary
            print(f"Packet Summary: {packet.summary()}")
            
            # Print packet details (verbose)
            print("\nPacket Details:")
            packet.show()
            
            # Print packet in hexdump format
            print("\nPacket Hexdump:")
            hexdump(packet)
            
            # # Optional: If you want to print raw bytes
            # print("\nRaw Bytes:")
            # print(bytes(packet))
            
    except FileNotFoundError:
        print(f"Error: File '{pcap_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing the PCAP file: {e}")
        sys.exit(1)

def main():
    
    # Run the analysis
    analyze_pcap('capture.pcapng')

if __name__ == "__main__":
    main()