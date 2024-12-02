@echo off
IF ["%1"]==[""] GOTO ERROR
:CREATE 

COPY "template.py" "%1.py"
set num=%1
set num=%num:0=%

START code "%1.in" "%1.py"

START "" https://adventofcode.com/2024/day/%num%
echo Successfully created Day %num%
exit
GOTO END

:ERROR
echo No day was specified

:END