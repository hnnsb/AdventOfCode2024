@echo off
IF ["%1"]==[""] GOTO ERROR
:CREATE 

COPY "template.py" "%1.py"
set num=%1
REM Remove leading zeros from the num variable
set num=%num:0=%

START /B code . "%1.in" "%1.py"
START /B "" https://adventofcode.com/2024/day/%num%

echo Successfully created Day %num%

GOTO END

:ERROR
echo No day was specified

:END