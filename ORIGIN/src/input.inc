; return AL:
; 0 = none
; 1 = up
; 2 = down
; 3 = enter
; 4 = esc
input_read_menu_key:
    mov al, 0
    mov ah, 01h
    int 16h
    jz .done

    mov ah, 00h
    int 16h

    cmp ah, 48h        ; up
    je .key_up

    cmp ah, 50h        ; down
    je .key_down

    cmp al, 13         ; enter
    je .key_enter

    cmp ah, 01h        ; esc
    je .key_esc

    jmp .done

.key_up:
    mov al, 1
    ret

.key_down:
    mov al, 2
    ret

.key_enter:
    mov al, 3
    ret

.key_esc:
    mov al, 4
    ret

.done:
    ret