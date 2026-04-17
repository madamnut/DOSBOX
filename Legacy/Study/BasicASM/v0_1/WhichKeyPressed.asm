; ============================================================
; hello.asm
;
; 목적:
;   1) 화면에 안내 문구를 출력한다
;   2) 키 하나를 입력받는다
;   3) 입력한 키가 'A'인지 비교한다
;   4) 맞으면 A pressed 출력
;   5) 아니면 Not A 출력
;   6) 종료한다
;
; 빌드:
;   nasm -f bin hello.asm -o hello.com
; ============================================================

org 100h
; .COM 프로그램은 DOS가 보통 오프셋 0100h부터 적재하므로
; 어셈블러에게 기준 주소를 100h로 잡으라고 알려준다.

mov ah, 09h
; DOS int 21h 기능 중
; AH=09h 는 '$'로 끝나는 문자열 출력 기능이다.

mov dx, prompt_msg
; 출력할 문자열의 시작 주소를 DX에 넣는다.

int 21h
; prompt_msg 문자열을 화면에 출력한다.

mov ah, 00h
; BIOS 키보드 인터럽트 int 16h 기능 중
; AH=00h 는 키 하나를 입력받을 때까지 대기하는 기능이다.

int 16h
; 키를 하나 입력받는다.
; 결과:
;   AL = ASCII 코드(문자 키인 경우)
;   AH = 스캔 코드
; 지금은 AL을 이용해 문자 비교를 한다.

cmp al, 'A'
; AL에 들어온 문자와 대문자 A를 비교한다.

je key_is_a
; 같으면 key_is_a 라벨로 점프한다.

cmp al, 'a'
; 혹시 소문자 a인지도 비교한다.

je key_is_a
; 소문자 a여도 같은 처리로 보낸다.

mov ah, 09h
; A가 아니었으므로
; "Not A" 문자열을 출력하기 위해 다시 출력 기능 준비.

mov dx, not_a_msg
; not_a_msg 문자열 주소를 DX에 넣는다.

int 21h
; "Not A" 출력

jmp program_exit
; A가 아닌 경우 출력 후 종료 코드 쪽으로 이동

key_is_a:
; A 또는 a 를 눌렀을 때 여기로 온다.

mov ah, 09h
; 문자열 출력 기능 준비

mov dx, a_msg
; a_msg 문자열 주소를 DX에 넣는다.

int 21h
; "A pressed" 출력

program_exit:
; 여기부터 공통 종료 구간

mov ax, 4c00h
; DOS 종료 기능 준비
; AH=4Ch -> 종료
; AL=00h -> 종료 코드 0

int 21h
; 프로그램 종료

prompt_msg db 'Press A key...$'
; 시작할 때 보여줄 안내 문구
; AH=09h 출력용 문자열이므로 끝에 반드시 '$' 필요

a_msg db 13, 10, 'A pressed$'
; 13,10은 줄바꿈(CR, LF)
; 그 다음 "A pressed" 출력 후 '$'에서 종료

not_a_msg db 13, 10, 'Not A$'
; A가 아닐 때 출력할 문자열
; 역시 줄바꿈 후 메시지 출력