@echo off
set "DIR=%~dp0"
if exist "%DIR%glagol.exe" (
  "%DIR%glagol.exe" %*
) else (
  py -3 "%DIR%glagol.py" %*
)
