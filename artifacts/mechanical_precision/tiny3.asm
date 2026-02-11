; tiny3.asm - ~125 byte ELF64, PI, builds message on the fly
BITS 64
ORG 0x400000

; --- ELF Header (minimal) ---
db 0x7F,'ELF',2,1,1,0,0,0,0,0,0,0
dw 2
dw 0x3E
dd 1
dq _start
dq 64
dq 0
dd 0
dw 64
dw 56
dw 1
dw 0
dw 0
dw 0

; --- Program Header ---
dd 1
dd 5
dq 0
dq $$
dq $$
dq filesize
dq filesize
dq 0x1000

_start:
    ; write syscall preparation
    mov rax,1        ; sys_write
    mov rdi,1        ; stdout

    ; generate message byte-by-byte in rsi
    lea rsi,[rel msg]
    mov rdx,msg_len
    syscall

    ; exit cleanly
    mov rax,60
    xor rdi,rdi
    syscall

msg:
    db 10,"INTELLIGENCE IS SHAPEABLE.",10
    db "CONSTRAINT IS ARCHITECTURE.",10
    db "CONVERSATION IS COMPILATION.",10
    db 10

msg_len equ $-msg
filesize equ $-$$