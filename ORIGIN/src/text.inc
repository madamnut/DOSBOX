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

    ; di = y * 320 + x
    mov ax, dx
    shl ax, 6
    mov di, ax

    mov ax, dx
    shl ax, 8
    add di, ax
    add di, bx

    mov bp, FONT_HEIGHT

.row_loop:
    lodsb
    mov ah, al
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


; ----------------------------------------
; draw_string_outline_8x16
; input:
;   DS:SI = zero-terminated string
;   BX = x
;   DX = y
;   CL = fill color
;   CH = outline color
; ----------------------------------------
draw_string_outline_8x16:
    push ax
    push bx
    push cx
    push dx
    push si

    mov [outline_fill_color], cl

    ; up-left
    dec bx
    dec dx
    push si
    mov cl, ch
    call draw_string_8x16
    pop si
    inc bx
    inc dx

    ; up
    dec dx
    push si
    mov cl, ch
    call draw_string_8x16
    pop si
    inc dx

    ; up-right
    inc bx
    dec dx
    push si
    mov cl, ch
    call draw_string_8x16
    pop si
    dec bx
    inc dx

    ; left
    dec bx
    push si
    mov cl, ch
    call draw_string_8x16
    pop si
    inc bx

    ; right
    inc bx
    push si
    mov cl, ch
    call draw_string_8x16
    pop si
    dec bx

    ; down-left
    dec bx
    inc dx
    push si
    mov cl, ch
    call draw_string_8x16
    pop si
    inc bx
    dec dx

    ; down
    inc dx
    push si
    mov cl, ch
    call draw_string_8x16
    pop si
    dec dx

    ; down-right
    inc bx
    inc dx
    push si
    mov cl, ch
    call draw_string_8x16
    pop si
    dec bx
    dec dx

    ; center fill
    mov cl, [outline_fill_color]
    push si
    call draw_string_8x16
    pop si

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret


; ----------------------------------------
; get_string_width_8x16
; input:
;   DS:SI = zero-terminated string
; output:
;   AX = width in pixels
; ----------------------------------------
get_string_width_8x16:
    push si
    xor ax, ax

.count_loop:
    lodsb
    or al, al
    jz .done
    add ax, 8
    jmp .count_loop

.done:
    pop si
    ret


; ----------------------------------------
; draw_string_outline_centered_8x16
; input:
;   DS:SI = zero-terminated string
;   DX = y
;   CL = fill color
;   CH = outline color
; output:
;   string centered on screen by base text width
; ----------------------------------------
draw_string_outline_centered_8x16:
    push ax
    push bx
    push cx
    push dx
    push si

    push si
    call get_string_width_8x16
    pop si

    ; x = 160 - (width / 2)
    mov bx, ax
    shr bx, 1
    mov ax, 160
    sub ax, bx
    mov bx, ax

    call draw_string_outline_8x16

    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret


; ----------------------------------------
; draw_menu_item_centered_8x16
; input:
;   DS:SI = base label string
;   DX = y
;   CL = fill color
;   CH = outline color
;   AL = 0 normal, nonzero selected
;
; behavior:
;   - base label is always centered
;   - when selected, draw >> and << around it
; ----------------------------------------
draw_menu_item_centered_8x16:
    push ax
    push bx
    push cx
    push dx
    push si

    mov [menu_item_selected], al

    ; base label width
    push si
    call get_string_width_8x16
    mov [menu_item_width], ax
    pop si

    ; base x = 160 - (width / 2)
    mov bx, ax
    shr bx, 1
    mov ax, 160
    sub ax, bx
    mov [menu_item_x], ax

    ; draw base label
    mov bx, [menu_item_x]
    call draw_string_outline_8x16

    cmp byte [menu_item_selected], 0
    je .done

    ; left marker
    mov si, menu_marker_left
    call get_string_width_8x16
    mov bx, [menu_item_x]
    sub bx, ax
    sub bx, 8
    call draw_string_outline_8x16

    ; right marker
    mov si, menu_marker_right
    mov bx, [menu_item_x]
    add bx, [menu_item_width]
    add bx, 8
    call draw_string_outline_8x16

.done:
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret


menu_item_selected db 0
menu_item_width    dw 0
menu_item_x        dw 0


outline_fill_color db 0