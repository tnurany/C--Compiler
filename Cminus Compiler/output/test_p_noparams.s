	.section .rodata
.char_wformat: .string "%c\n"
.int_wformat: .string "%d\n"
.float_wformat: .string "%f\n"
.str_wformat: .string "%s\n"
.char_rformat: .string "%c"
.int_rformat: .string "%ld"
.float_rformat: .string "%f"
.comm i, 8, 8
.comm j, 8, 8
.comm k, 8, 8
.comm l, 8, 8
	.text
	.globl a1
	.type a1, @function
a1:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movq $1, %rcx
	movq %rcx, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	movq $0, %rcx
	movq %rcx, %rax
	leave
	ret
	.text
	.globl a2
	.type a2, @function
a2:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	pushq %rcx
	subq $8, %rsp
	call a1
	movq %rax, %r8
	addq $8, %rsp
	popq %rcx
	movq %r8, j(%rip)
	movq $2, %r8
	movq %r8, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	movq $0, %r8
	movq %r8, %rax
	leave
	ret
	.text
	.globl a3
	.type a3, @function
a3:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	pushq %rcx
	pushq %r8
	call a1
	movq %rax, %r9
	popq %r8
	popq %rcx
	movq %r9, i(%rip)
	pushq %rcx
	pushq %r8
	call a2
	movq %rax, %r9
	popq %r8
	popq %rcx
	movq %r9, j(%rip)
	movq $3, %r9
	movq %r9, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	movq $0, %r9
	movq %r9, %rax
	leave
	ret
	.text
	.globl a4
	.type a4, @function
a4:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	pushq %rcx
	pushq %r8
	pushq %r9
	subq $8, %rsp
	call a1
	movq %rax, %rsi
	addq $8, %rsp
	popq %r9
	popq %r8
	popq %rcx
	movq %rsi, i(%rip)
	pushq %rcx
	pushq %r8
	pushq %r9
	subq $8, %rsp
	call a2
	movq %rax, %rsi
	addq $8, %rsp
	popq %r9
	popq %r8
	popq %rcx
	movq %rsi, j(%rip)
	pushq %rcx
	pushq %r8
	pushq %r9
	subq $8, %rsp
	call a3
	movq %rax, %rsi
	addq $8, %rsp
	popq %r9
	popq %r8
	popq %rcx
	movq %rsi, k(%rip)
	movq $4, %rsi
	movq %rsi, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	movq $0, %rsi
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
	call a1
	movq %rax, %rdi
	popq %r9
	popq %r8
	popq %rsi
	popq %rcx
	movq %rdi, i(%rip)
	pushq %rcx
	pushq %rsi
	pushq %r8
	pushq %r9
	call a2
	movq %rax, %rdi
	popq %r9
	popq %r8
	popq %rsi
	popq %rcx
	movq %rdi, j(%rip)
	pushq %rcx
	pushq %rsi
	pushq %r8
	pushq %r9
	call a3
	movq %rax, %rdi
	popq %r9
	popq %r8
	popq %rsi
	popq %rcx
	movq %rdi, k(%rip)
	pushq %rcx
	pushq %rsi
	pushq %r8
	pushq %r9
	call a4
	movq %rax, %rdi
	popq %r9
	popq %r8
	popq %rsi
	popq %rcx
	movq %rdi, l(%rip)
	leave
	ret
