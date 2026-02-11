section .data
    header      db  "PRIMES UNDER 100", 10
    header_len  equ $ - header

    newline     db  10

section .bss
    sieve       resb 100

section .text
    global _start

_start:
    ; print header
    mov rax, 1
    mov rdi, 1
    mov rsi, header
    mov rdx, header_len
    syscall

    ; initialize sieve
    mov rcx, 2
.init:
    cmp rcx, 100
    jge .sieve_loop
    mov byte [sieve + rcx], 1
    inc rcx
    jmp .init

.sieve_loop:
    mov rbx, 2
.outer:
    cmp rbx, 10
    jge .print_primes
    mov al, [sieve + rbx]
    cmp al, 0
    je .next_outer

    mov rcx, rbx
    imul rcx, rbx
.inner:
    cmp rcx, 100
    jge .next_outer
    mov byte [sieve + rcx], 0
    add rcx, rbx
    jmp .inner

.next_outer:
    inc rbx
    jmp .outer

.print_primes:
    mov rbx, 2
.print_loop:
    cmp rbx, 100
    jge .exit
    mov al, [sieve + rbx]
    cmp al, 0
    je .next_print

    ; convert number to string (two-digit max)
    mov rax, rbx
    mov rcx, 10
    xor rdx, rdx
    div rcx

    add rax, '0'
    add rdx, '0'

    cmp rbx, 10
    jl .single_digit

    mov [sieve], al
    mov [sieve+1], dl
    mov rsi, sieve
    mov rdx, 2
    jmp .write

.single_digit:
    mov [sieve], dl
    mov rsi, sieve
    mov rdx, 1

.write:
    mov rax, 1
    mov rdi, 1
    syscall

    ; print newline
    mov rax, 1
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall

.next_print:
    inc rbx
    jmp .print_loop

.exit:
    mov rax, 60
    xor rdi, rdi
    syscall
