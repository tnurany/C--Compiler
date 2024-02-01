	.section .rodata
.char_wformat: .string "%c\n"
.int_wformat: .string "%d\n"
.float_wformat: .string "%f\n"
.str_wformat: .string "%s\n"
.char_rformat: .string "%c"
.int_rformat: .string "%ld"
.float_rformat: .string "%f"
.comm c, 8, 8
.float0:	.float 2.0
	.text
	.globl b
	.type b, @function
b:
	pushq %rbp
	movq %rsp, %rbp
	subq $24, %rsp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	movss %xmm2, -24(%rbp)
	subq $8, %rsp
	movq -8(%rbp), %rcx
	movq -16(%rbp), %r8
	addq %r8, %rcx
	movss -24(%rbp), %xmm0
	pxor %xmm1, %xmm1
	cvtsi2ss %rcx, %xmm1
	addss %xmm0, %xmm1
	movss %xmm1, -24(%rbp)
	movss -24(%rbp), %xmm0
	cvtss2sd %xmm0, %xmm0
	leaq .float_wformat(%rip), %rdi
	movq $1, %rax
	call printf
	leave
	ret
	.text
	.globl main
	.type main, @function
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movq $1, %rcx
	movq %rcx, %rdi
	movq $1, %rcx
	movq %rcx, %rsi
	movss .float0(%rip), %xmm0
	movss %xmm0, %xmm2
	call b
	leave
	ret
