	.section .rodata
.char_wformat: .string "%c\n"
.int_wformat: .string "%d\n"
.float_wformat: .string "%f\n"
.str_wformat: .string "%s\n"
.char_rformat: .string "%c"
.int_rformat: .string "%ld"
.float_rformat: .string "%f"
	.text
	.globl b1
	.type b1, @function
b1:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movq $1, %rcx
	movq %rcx, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	movq $1, %rcx
	movq %rcx, %rax
	leave
	ret
	.text
	.globl b2
	.type b2, @function
b2:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movq $2, %r8
	movq %r8, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	pushq %rcx
	subq $8, %rsp
	call b1
	movq %rax, %r8
	addq $8, %rsp
	popq %rcx
	movq %r8, %rax
	leave
	ret
	.text
	.globl b3
	.type b3, @function
b3:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movq $3, %r9
	movq %r9, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	pushq %rcx
	pushq %r8
	call b1
	movq %rax, %r9
	popq %r8
	popq %rcx
	pushq %rcx
	pushq %r8
	pushq %r9
	subq $8, %rsp
	call b2
	movq %rax, %rsi
	addq $8, %rsp
	popq %r9
	popq %r8
	popq %rcx
	addq %rsi, %r9
	movq %r9, %rax
	leave
	ret
	.text
	.globl b4
	.type b4, @function
b4:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movq $4, %rsi
	movq %rsi, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	pushq %rcx
	pushq %r8
	pushq %r9
	subq $8, %rsp
	call b1
	movq %rax, %rsi
	addq $8, %rsp
	popq %r9
	popq %r8
	popq %rcx
	pushq %rcx
	pushq %rsi
	pushq %r8
	pushq %r9
	call b2
	movq %rax, %rdi
	popq %r9
	popq %r8
	popq %rsi
	popq %rcx
	addq %rdi, %rsi
	pushq %rcx
	pushq %rsi
	pushq %r8
	pushq %r9
	call b3
	movq %rax, %rdi
	popq %r9
	popq %r8
	popq %rsi
	popq %rcx
	addq %rdi, %rsi
	movq %rsi, %rax
	leave
	ret
	.text
	.globl main
	.type main, @function
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	pushq %rcx
	pushq %rsi
	pushq %r8
	pushq %r9
	call b1
	movq %rax, %rdi
	popq %r9
	popq %r8
	popq %rsi
	popq %rcx
	pushq %rcx
	pushq %rsi
	pushq %rdi
	pushq %r8
	pushq %r9
	subq $8, %rsp
	call b2
	movq %rax, %rdx
	addq $8, %rsp
	popq %r9
	popq %r8
	popq %rdi
	popq %rsi
	popq %rcx
	addq %rdx, %rdi
	pushq %rcx
	pushq %rsi
	pushq %rdi
	pushq %r8
	pushq %r9
	subq $8, %rsp
	call b3
	movq %rax, %rdx
	addq $8, %rsp
	popq %r9
	popq %r8
	popq %rdi
	popq %rsi
	popq %rcx
	addq %rdx, %rdi
	pushq %rcx
	pushq %rsi
	pushq %rdi
	pushq %r8
	pushq %r9
	subq $8, %rsp
	call b4
	movq %rax, %rdx
	addq $8, %rsp
	popq %r9
	popq %r8
	popq %rdi
	popq %rsi
	popq %rcx
	addq %rdx, %rdi
	movq %rdi, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	leave
	ret
