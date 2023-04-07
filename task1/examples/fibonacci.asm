FBEG 1
IFNIL r1 ret1
ASSIGN r2 1
SUB r1 r2
IFNIL r1 ret1
PUSHREG r1
CALL 1
TOP r1
POP
ASSIGN r2 1
SUB r1 r2
PUSHREG r6
CALL 1
TOP r5
POP
ADD r6 r5
JUMP finish
ret1: ASSIGN r6 1
finish: FEND
PUTSTR This program returns n-th Fibonacci number
PUTSTR Enter the n:
READ r1
CALL 1
PUTSTR Result:
PRINT r6
STOP