	.section .rodata
.char_wformat: .string "%c\n"
.int_wformat: .string "%d\n"
.float_wformat: .string "%f\n"
.str_wformat: .string "%s\n"
.char_rformat: .string "%c"
.int_rformat: .string "%ld"
.float_rformat: .string "%f"
.comm a, 8, 8
.comm b, 8, 8
.float0:	.float 7.3
	.text
	.globl decls
	.type decls, @function
decls:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movq a(%rip), %rcx
	movq %rcx, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	movq a(%rip), %rcx
	movq $0, %r8
	xor %rax, %rax
	cmpq %r8, %rcx
	setg %al
	movzbq %al, %rax
	cmp $1, %rax
	jne .L0
	movq a(%rip), %rcx
	movq $1, %r8
	subq %r8, %rcx
	movq %rcx, a(%rip)
	call decls
	movq %rax, %rcx
	movq %rcx, %rax
	jmp .L1
.L0:
	movq $0, %r8
	movq %r8, a(%rip)
	movq a(%rip), %r8
	movq %r8, %rax
	jmp .L1
.L1:
	leave
	ret
	.text
	.globl foo
	.type foo, @function
foo:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movq a(%rip), %r9
	movq %r9, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	movq b(%rip), %r9
	movq %r9, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
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
	leaq a(%rip), %rsi
	leaq .int_rformat(%rip), %rdi
	movq $0, %rax
	call scanf
	pushq %rcx
	pushq %r8
	call decls
	movq %rax, %r9
	popq %r8
	popq %rcx
	movq %r9, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	movq $10, %r9
	movq %r9, b(%rip)
	pushq %rcx
	pushq %r8
	call foo
	movss %xmm0, %xmm1
	popq %r8
	popq %rcx
	movss %xmm1, %xmm0
	cvtss2sd %xmm0, %xmm0
	leaq .float_wformat(%rip), %rdi
	movq $1, %rax
	call printf
	leave
	ret
