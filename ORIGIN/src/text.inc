; ----------------------------------------
; draw_char_8x16
; input:
;   AL = character code
;   BX = x
;   DX = y
;   CL = color
; ----------------------------------------
draw_char_8x16:
    push ax
    push bx
    push cx
    push dx
    push si
    push di
    push bp
    push ds
    push es

    ; character offset = AL * 16
    xor ah, ah
    shl ax, 1
    shl ax, 1
    shl ax, 1
    shl ax, 1

    push cs
    pop ds
    mov si, font_buffer
    add si, ax

    mov ax, SCREEN_SEG
    mov es, ax

    ; di = y * 320 + x = y*256 + y*64 + x
    mov ax, dx
    shl ax, 6
    mov di, ax

    mov ax, dx
    shl ax, 8
    add di, ax
    add di, bx

    mov bp, FONT_HEIGHT

.row_loop:
    lodsb                   ; one row bitmap
    mov ah, al              ; preserve row bits
    mov bl, 8

.pixel_loop:
    test ah, 80h
    jz .skip_pixel
    mov al, cl
    mov [es:di], al
.skip_pixel:
    shl ah, 1
    inc di
    dec bl
    jnz .pixel_loop

    add di, 320 - 8
    dec bp
    jnz .row_loop

    pop es
    pop ds
    pop bp
    pop di
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret


; ----------------------------------------
; draw_string_8x16
; input:
;   DS:SI = zero-terminated string
;   BX = x
;   DX = y
;   CL = color
; ----------------------------------------
draw_string_8x16:
    push ax
    push bx
    push dx
    push si

.next_char:
    lodsb
    or al, al
    jz .done

    call draw_char_8x16
    add bx, 8
    jmp .next_char

.done:
    pop si
    pop dx
    pop bx
    pop ax
    ret