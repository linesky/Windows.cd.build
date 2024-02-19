@set paths=%PATH%
@set PATH=c:\mingw\bin\;%paths%
@del .\tmp\*.exe >.\tmp\null
@del .\tmp\*.o  >.\tmp\null
@copy %1 .\tmp\kernel.c
@as.exe .\file\boot.s -o .\tmp\boot.o
@g++.exe -mconsole -c -I.\\file .\tmp\kernel.c -o .\tmp\kernel.o
@ld.exe -nostdlib -T  .\file\link.ld .\tmp\boot.o .\tmp\kernel.o  -o .\tmp\hello.bin
@set PATH=%paths%
