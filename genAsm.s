
.section .text

.globl start

start:

    mul x25, x25, x5
    lui x21, 0x3d8bf
    jalr x7, x3, 0xb9
    lh x1, -761(x28)
    add x13, x9, x0
    mulhsu x20, x12, x30
    mulhu x6, x10, x25
    auipc x28, 0x500f9
    div x8, x3, x6
    sb x21, 27(x17)
    jal x27, 0x1ef
    auipc x20, 0xa4911
    divu x30, x26, x25
    xori x9, x3, -0x48e
    sra x8, x3, x23
    bne x1, x28, 0x2f
    sltu x9, x28, x7
    or x12, x10, x21
    xori x28, x2, 0x784
    ori x24, x4, -0x8c
    sb x9, 22(x13)
    sb x5, 91(x16)
    bltu x13, x23, 0x3f
    sltu x22, x12, x19
    
    sb x12, 91(x20)
    sltiu x13, x8, 0x54b
    lbu x29, 1606(x20)
    jalr x17, x1, 0x65b
    bge x18, x8, 0x17
    sll x6, x6, x28
    sll x26, x4, x21
    mulhsu x22, x13, x9
    andi x10, x21, 0x69c
    beq x5, x15, 0x2
    slt x30, x16, x12
    addi x3, x18, 0x52e
    sltiu x26, x25, -0x191
    lui x25, 0x5f0d2
    mulh x25, x25, x18
    bge x17, x14, 0x2d
    addi x31, x17, -0x3
    sh x25, 15(x2)
    slti x15, x23, 0x286
    mul x13, x13, x27
    sw x7, 59(x7)
    sra x12, x25, x4
    rem x5, x25, x24
    divu x20, x27, x31
    beq x30, x22, 0xf
    sra x14, x16, x28
    mul x30, x20, x20
    lh x18, -575(x12)
    lh x13, -1182(x27)
    jal x22, 0x2ef
    srl x24, x1, x19
    lw x12, 1847(x10)
    sub x19, x2, x13
    mulhsu x27, x29, x14
    srl x28, x5, x13
    lbu x4, -1373(x22)
    blt x22, x19, 0x1f
    beq x2, x9, 0x7
    sub x26, x5, x12
    beq x6, x22, 0xf
    beq x13, x27, 0x2d
    beq x5, x12, 0xb
    lbu x19, 467(x31)
    lbu x22, 383(x10)
    and x12, x1, x7
    divu x30, x6, x1
    blt x29, x2, 0x3f
    beq x6, x25, 0x3b
    jal x25, 0x3bb
    mulh x26, x0, x28
    mulhsu x17, x11, x12
    divu x28, x4, x12
    divu x27, x10, x28
    
    jalr x22, x5, 0x10e
    sw x20, 127(x1)
    div x6, x27, x23
    srl x22, x10, x5
    ori x21, x10, 0x1b3
    sltu x4, x21, x25
    blt x10, x0, 0xf
    
    lui x30, 0x1147a
    or x23, x13, x19
    mulhsu x8, x26, x15
    add x28, x6, x2
    xor x5, x2, x29
    xori x31, x5, -0x11a
    bne x3, x19, 0x19
    slt x20, x5, x14
    add x18, x27, x15
    srl x2, x2, x13
    xori x5, x30, 0xf0
    bge x31, x23, 0x19
    lhu x14, -510(x25)
