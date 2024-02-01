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
	.text
	.globl swap
	.type swap, @function
swap:
	pushq %rbp
	movq %rsp, %rbp
	subq $16, %rsp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	subq $8, %rsp
	subq $8, %rsp
	movq -8(%rbp), %rcx
	movq %rcx, -24(%rbp)
	movq -16(%rbp), %rcx
	movq %rcx, -8(%rbp)
	movq -24(%rbp), %rcx
	movq %rcx, -16(%rbp)
	movq -16(%rbp), %rcx
	movq %rcx, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	movq -8(%rbp), %rcx
	movq %rcx, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
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
	leaq i(%rip), %rsi
	leaq .int_rformat(%rip), %rdi
	movq $0, %rax
	call scanf
	leaq j(%rip), %rsi
	leaq .int_rformat(%rip), %rdi
	movq $0, %rax
	call scanf
	movq i(%rip), %rcx
	movq %rcx, %rdi
	movq j(%rip), %rcx
	movq %rcx, %rsi
	call swap
	movq i(%rip), %rcx
	movq %rcx, %rsi
	leaq .int_wformat(%rip), %rdi
	mov $0, %rax
	call printf
	leave
	ret
