@echo off
SETLOCAL

REM Download and install MongoDB Server
powershell -Command "Invoke-WebRequest https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-latest-signed.msi -OutFile mongodb.msi"
msiexec /qn /i mongodb.msi

REM Download and install MongoDB Compass
powershell -Command "Invoke-WebRequest https://downloads.mongodb.com/compass/mongodb-compass-latest-win32-x64.exe -OutFile compass.exe"
start /wait compass.exe /S

REM Configure database according to config.json
for /f "delims=" %%A in ('powershell -NoProfile -Command "(Get-Content 'config.json' | ConvertFrom-Json).database.uri"') do set DBURI=%%A
for /f "delims=" %%A in ('powershell -NoProfile -Command "(Get-Content 'config.json' | ConvertFrom-Json).database.name"') do set DBNAME=%%A
mongosh %DBURI% --eval "db.getSiblingDB('%DBNAME%').createCollection('logs')"

ENDLOCAL
