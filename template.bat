@echo off

set arguments=%*

:__main
echo %arguments%
goto:eof

call:__main