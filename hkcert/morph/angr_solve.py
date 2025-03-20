#!/usr/bin/env python3
import angr
import sys
import claripy
from pwn import *

def find_path_to_instruction(binary_path, target_addr, input_length=50):
    # Create project
    proj = angr.Project(binary_path, auto_load_libs=False)
    
    # Create a symbolic buffer for input
    flag_chars = [claripy.BVS(f'flag_{i}', 8) for i in range(input_length)]
    flag = claripy.Concat(*flag_chars)
    
    # Create initial state at program entry
    state = proj.factory.entry_state(args=[binary_path])
    
    # Constrain input to be printable ASCII
    for c in flag_chars:
        # Constrain to printable ASCII range (32-126)
        state.solver.add(c >= ord(' '))
        state.solver.add(c <= ord('~'))
    
    # Set up stdin with our symbolic input
    state.posix.get_fd(0).write(flag)
    state.posix.get_fd(0).seek(0)
    state.posix.get_fd(0).write(state.solver.BVV(b'\n'))  # Add newline
    state.posix.get_fd(0).seek(0)
    
    # Create simulation manager
    simgr = proj.factory.simulation_manager(state)
    
    # Define find function to locate our target address
    def is_successful(state):
        return state.addr == target_addr
    
    # Define avoid function
    def should_avoid(state):
        # Avoid paths that clearly lead to failure
        # Customize this based on your binary
        return False
    
    print(f"[*] Starting path exploration to {hex(target_addr)}")
    print(f"[*] Looking for solution with input length up to {input_length} chars")
    
    # Explore until we find our target
    simgr.explore(find=is_successful, avoid=should_avoid)
    
    # Check if we found a solution
    if simgr.found:
        found_state = simgr.found[0]
        
        # Get concrete input that leads to this state
        solution = found_state.posix.dumps(0)  # stdin
        solution = solution.rstrip(b'\n')  # Remove trailing newline
        
        print(f"[+] Found solution!")
        print(f"[+] Input (hex): {solution.hex()}")
        print(f"[+] Input (raw): {repr(solution)}")
        print(f"[+] Length: {len(solution)} bytes")
        
        try:
            printable = solution.decode('ascii')
            print(f"[+] Input (ascii): {printable}")
        except:
            print("[-] Warning: Solution contains non-ASCII characters")
            
        return solution
    else:
        print("[-] No solution found")
        if simgr.deadended:
            print(f"[-] Paths deadended: {len(simgr.deadended)}")
        if simgr.active:
            print(f"[-] Paths still active: {len(simgr.active)}")
        return None

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: ./script.py <binary> <target_address> [input_length]")
        print("Example: ./script.py ./binary 0x4006aa 30")
        return
    
    binary_path = sys.argv[1]
    try:
        target_addr = int(sys.argv[2], 16) if '0x' in sys.argv[2] else int(sys.argv[2])
    except ValueError:
        print("[-] Error: Target address must be a valid hexadecimal or decimal number")
        return
    
    # Optional input length parameter
    input_length = 50  # default
    if len(sys.argv) == 4:
        try:
            input_length = int(sys.argv[3])
            if input_length <= 0:
                print("[-] Error: Input length must be positive")
                return
        except ValueError:
            print("[-] Error: Input length must be a number")
            return
    
    # Attempt to verify target address exists in binary
    try:
        elf = ELF(binary_path)
        binary_text = elf.get_section_by_name('.text')
        if binary_text:
            text_start = binary_text.header.sh_addr
            text_end = text_start + binary_text.header.sh_size
            if not (text_start <= target_addr < text_end):
                print(f"[!] Warning: Target address {hex(target_addr)} might not be in .text section")
    except:
        print("[!] Warning: Could not verify target address in binary")
    
    solution = find_path_to_instruction(binary_path, target_addr, input_length)
    
    if solution:
        # Save solution to file
        with open('solution.txt', 'wb') as f:
            f.write(solution)
        print("[+] Solution saved to 'solution.txt'")

if __name__ == "__main__":
    main()