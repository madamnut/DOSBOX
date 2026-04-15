; DX = zero-terminated filename
load_palette_direct:
    push ax
    push bx
    push cx
    push dx
    push ds

    push cs
    pop ds
    mov ax, 3D00h
    int 21h
    jc .done

    mov bx, ax

    mov dx, 03C8h
    xor al, al
    out dx, al

    mov cx, 256

.next_color:
    push cx

    push cs
    pop ds
    mov dx, pal_triplet
    mov cx, 3
    mov ah, 3Fh
    int 21h
    cmp ax, 3
    jne .close_file_pop

    mov dx, 03C9h

    mov al, [pal_triplet + 0]
    shr al, 1
    shr al, 1
    out dx, al

    mov al, [pal_triplet + 1]
    shr al, 1
    shr al, 1
    out dx, al

    mov al, [pal_triplet + 2]
    shr al, 1
    shr al, 1
    out dx, al

    pop cx
    loop .next_color
    jmp .close_file

.close_file_pop:
    pop cx

.close_file:
    mov ah, 3Eh
    int 21h

.done:
    pop ds
    pop dx
    pop cx
    pop bx
    pop ax
    ret

clear_palette_black:
    push ax
    push cx
    push dx

    mov dx, 03C8h
    xor al, al
    out dx, al

    mov dx, 03C9h
    mov cx, 768
    xor al, al

.black_loop:
    out dx, al
    loop .black_loop

    pop dx
    pop cx
    pop ax
    ret