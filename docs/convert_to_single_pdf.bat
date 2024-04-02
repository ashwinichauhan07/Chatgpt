@echo off
setlocal enabledelayedexpansion

set "WKHTMLTOPDF_PATH=C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
set "OUTPUT_FILE=CombinedOutput.pdf"

if not exist "%WKHTMLTOPDF_PATH%" (
    echo wkhtmltopdf is not installed or the path is incorrect.
    exit /b 1
)

echo Converting URLs to a single PDF...

set "URLS="

for /f "tokens=*" %%a in (urls.txt) do (
    set "URLS=!URLS! "%%a""
)

"%WKHTMLTOPDF_PATH%" %URLS% "%OUTPUT_FILE%"

if errorlevel 1 (
    echo Conversion failed.
) else (
    echo Conversion successful. Output file: %OUTPUT_FILE%
)

echo All conversions completed.
