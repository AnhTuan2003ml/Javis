@echo off
echo Checking connected ADB devices...
echo.
C:\platform-tools\adb.exe devices
echo.
echo Device status meanings:
echo - device: Connected and ready
echo - offline: Connected but not responding
echo - unauthorized: Connected but not authorized (check phone for prompt)
echo - no permissions: USB debugging not enabled
echo.
pause