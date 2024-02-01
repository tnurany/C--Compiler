	.section .rodata
.char_wformat: .string "%c\n"
.int_wformat: .string "%d\n"
.float_wformat: .string "%f\n"
.str_wformat: .string "%s\n"
.char_rformat: .string "%c"
.int_rformat: .string "%ld"
.float_rformat: .string "%f"
.comm c, 8, 8
	.text
	.globl b
	.type b, @function
b:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movq $4, %rcx
	movq %rcx, %rax
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
	subq $8, %rsp
	call b
	movq %rax, %r8
	addq $8, %rsp
	popq %rcx
	movq %r8, c(%rip)
	movq c(%rip), %r8
	movq %r8, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	leave
	ret
