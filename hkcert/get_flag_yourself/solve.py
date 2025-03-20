from pwn import *
from base64 import *
r = remote("c03-get-flag-yourself.hkcert24.pwnable.hk", 1337, ssl=True)
go_script = b'''
package main

import (
    "fmt"
    "os"
)

func main() {
    fmt.Println("Hello, World!")
    os.Exit(10)
}
'''
b64_go_script = b64encode(go_script)
print(b64decode(b64_go_script).decode())
r.sendline(b64_go_script)
print(r.recvall())