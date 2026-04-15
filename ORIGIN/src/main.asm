org 100h

jmp start

%include "defs.inc"

; -------------------------
; data
; -------------------------
logo_raw    db 'data\Image\Title\LOGO.RAW',0
logo_pal    db 'data\Image\Title\LOGO.PAL',0
title_raw   db 'data\Image\Title\TITLE.RAW',0
title_pal   db 'data\Image\Title\TITLE.PAL',0
font_file   db 'data\font\CGA-TH_D.F16',0

menu_start          db 'START',0
menu_start_sel      db '>> START <<',0
menu_exit           db 'EXIT',0
menu_exit_sel       db '>> EXIT <<',0

menu_newgame        db 'NEW GAME',0
menu_newgame_sel    db '>> NEW GAME <<',0
menu_loadgame       db 'LOAD GAME',0
menu_loadgame_sel   db '>> LOAD GAME <<',0

menu_state      db 0      ; 0=main, 1=start submenu
menu_index      db 0      ; 0 or 1

menu_marker_left    db '>>',0
menu_marker_right   db '<<',0

temp_buffer:
    times RAW_CHUNK_SIZE db 0

pal_triplet:
    times 3 db 0

font_buffer:
    times FONT_BYTES db 0

%include "video.inc"
%include "fileio.inc"
%include "palette.inc"
%include "timer.inc"
%include "input.inc"
%include "text.inc"

; -------------------------
; code
; -------------------------
start:
    cli
    push cs
    pop ds
    push cs
    pop es
    sti
    cld

    mov dx, font_file
    call load_font_file

    call video_set_13h

    ; logo
    call clear_vram
    mov dx, logo_pal
    call load_palette_direct
    mov dx, logo_raw
    call load_raw_to_vram

    call wait_3_seconds

    mov byte [menu_state], 0
    mov byte [menu_index], 0
    call redraw_title_menu

title_loop:
    call input_read_menu_key

    cmp al, 0
    je title_loop

    cmp al, 1
    je menu_up

    cmp al, 2
    je menu_down

    cmp al, 3
    je menu_enter

    cmp al, 4
    je menu_esc

    jmp title_loop


menu_up:
    cmp byte [menu_index], 0
    je title_loop
    dec byte [menu_index]
    call redraw_title_menu
    jmp title_loop


menu_down:
    cmp byte [menu_index], 1
    je title_loop
    inc byte [menu_index]
    call redraw_title_menu
    jmp title_loop


menu_enter:
    cmp byte [menu_state], 0
    je .main_enter

    ; submenu: NEW GAME / LOAD GAME
    ; not implemented yet -> exit
    jmp exit_program

.main_enter:
    cmp byte [menu_index], 0
    je .go_start_submenu

    ; EXIT selected
    jmp exit_program

.go_start_submenu:
    mov byte [menu_state], 1
    mov byte [menu_index], 0
    call redraw_title_menu
    jmp title_loop


menu_esc:
    cmp byte [menu_state], 1
    je .back_to_main

    ; main menu: ESC does nothing
    jmp title_loop

.back_to_main:
    mov byte [menu_state], 0
    mov byte [menu_index], 0
    call redraw_title_menu
    jmp title_loop


; -------------------------
; redraw current title + menu
; -------------------------
redraw_title_menu:
    push cs
    pop ds

    call clear_vram
    mov dx, title_pal
    call load_palette_direct
    mov dx, title_raw
    call load_raw_to_vram

    cmp byte [menu_state], 0
    je draw_main_menu
    jmp draw_start_submenu


draw_main_menu:
    ; normal = fill 0 / outline 255
    ; selected = fill 255 / outline 0

    ; START
    cmp byte [menu_index], 0
    je .start_selected

    mov si, menu_start
    mov dx, 128
    mov cl, 0
    mov ch, 255
    xor al, al
    call draw_menu_item_centered_8x16
    jmp .draw_exit

.start_selected:
    mov si, menu_start
    mov dx, 128
    mov cl, 255
    mov ch, 0
    mov al, 1
    call draw_menu_item_centered_8x16

.draw_exit:
    cmp byte [menu_index], 1
    je .exit_selected

    mov si, menu_exit
    mov dx, 148
    mov cl, 0
    mov ch, 255
    xor al, al
    call draw_menu_item_centered_8x16
    ret

.exit_selected:
    mov si, menu_exit
    mov dx, 148
    mov cl, 255
    mov ch, 0
    mov al, 1
    call draw_menu_item_centered_8x16
    ret


draw_start_submenu:
    ; NEW GAME
    cmp byte [menu_index], 0
    je .new_selected

    mov si, menu_newgame
    mov dx, 128
    mov cl, 0
    mov ch, 255
    xor al, al
    call draw_menu_item_centered_8x16
    jmp .draw_load

.new_selected:
    mov si, menu_newgame
    mov dx, 128
    mov cl, 255
    mov ch, 0
    mov al, 1
    call draw_menu_item_centered_8x16

.draw_load:
    cmp byte [menu_index], 1
    je .load_selected

    mov si, menu_loadgame
    mov dx, 148
    mov cl, 0
    mov ch, 255
    xor al, al
    call draw_menu_item_centered_8x16
    ret

.load_selected:
    mov si, menu_loadgame
    mov dx, 148
    mov cl, 255
    mov ch, 0
    mov al, 1
    call draw_menu_item_centered_8x16
    ret


exit_program:
    call video_set_text
    mov ax, 4C00h
    int 21h