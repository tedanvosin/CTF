#!/usr/bin/env python3
from pwn import *

def find_function_address(elf, func_name):
    # Search through all symbols for a matching substring
    matching_funcs = []
    
    for name, addr in elf.symbols.items():
        if isinstance(name, bytes):
            name = name.decode('utf-8', errors='ignore')
        if func_name in str(name):
            matching_funcs.append((name, addr))
    
    if not matching_funcs:
        print(f"Error: No function containing '{func_name}' found in binary")
        return None
        
    if len(matching_funcs) > 1:
        print(f"Found multiple matching functions:")
        for i, (name, addr) in enumerate(matching_funcs):
            print(f"{i}: {name} at {hex(addr)}")
        print("Using the first match.")
    
    return matching_funcs[0][1]  # Return address of first matching function

def to_unsigned_byte(n):
    # Convert any integer to its unsigned byte representation (0-255)
    return n & 0xFF

def modify_function(elf,func_name, xor_value):
    
    # Get the function address
    func_addr = find_function_address(elf, func_name)
    if not func_addr:
        return
    
    # Convert xor_value to unsigned byte
    xor_byte = to_unsigned_byte(xor_value)
    print(f"Found function containing '{func_name}' at address {hex(func_addr)}")
    print(f"Using XOR value: {xor_value} (0x{xor_byte:02x})")
    
    # Read the original bytes
    original_bytes = elf.read(func_addr, 86)
    print(f"Original bytes: {original_bytes.hex()}")
    
    # XOR the bytes
    modified_bytes = bytes([b ^ xor_byte for b in original_bytes])
    print(f"Modified bytes: {modified_bytes.hex()}")
    
    # Write back the modified bytes
    elf.write(func_addr, modified_bytes)
    

def main():
    elf = ELF('./morph_modified')
    for i in range(45):
        xor_val = int(input("xor_value:"))
        modify_function(elf,"_Z9verify_"+str(i)+'R', xor_val)
        elf.save('./morph_modified')
    print(f"Saved modified binary as 'morph_modified_final'")

if __name__ == "__main__":
    main()