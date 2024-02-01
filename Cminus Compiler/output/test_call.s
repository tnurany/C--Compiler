	.section .rodata
.char_wformat: .string "%c\n"
.int_wformat: .string "%d\n"
.float_wformat: .string "%f\n"
.str_wformat: .string "%s\n"
.char_rformat: .string "%c"
.int_rformat: .string "%ld"
.float_rformat: .string "%f"
.float0:	.float 7.3
	.text
	.globl decls
	.type decls, @function
decls:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movq $7, %rcx
	movq %rcx, %rax
	leave
	ret
	.text
	.globl foo
	.type foo, @function
foo:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movss .float0(%rip), %xmm0
	movss %xmm0, %xmm0
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
	call decls
	movq %rax, %r8
	addq $8, %rsp
	popq %rcx
	movq %r8, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	pushq %rcx
	subq $8, %rsp
	call foo
	movss %xmm0, %xmm1
	addq $8, %rsp
	popq %rcx
	movss %xmm1, %xmm0
	cvtss2sd %xmm0, %xmm0
	leaq .float_wformat(%rip), %rdi
	movq $1, %rax
	call printf
	leave
	ret
