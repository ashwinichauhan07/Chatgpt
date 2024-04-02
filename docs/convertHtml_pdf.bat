@echo off
setlocal enabledelayedexpansion

set "WKHTMLTOPDF_PATH=C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
set "TEMP_HTML_FILE=temp_urls.html"
set "OUTPUT_FILE=output.pdf"

if not exist "%WKHTMLTOPDF_PATH%" (
    echo wkhtmltopdf is not installed or the path is incorrect.
    exit /b 1
)

:: Create a temporary HTML file
echo Creating temporary HTML file...
if exist "%TEMP_HTML_FILE%" del "%TEMP_HTML_FILE%"
echo ^<!DOCTYPE html^> >> "%TEMP_HTML_FILE%"
echo ^<html^> >> "%TEMP_HTML_FILE%"
echo ^<body^> >> "%TEMP_HTML_FILE%"
for /f "tokens=*" %%a in (urls.txt) do (
    echo    ^<a href="%%a"^>%%a^</a^>^<br/^> >> "%TEMP_HTML_FILE%"
)
echo ^</body^> >> "%TEMP_HTML_FILE%"
echo ^</html^> >> "%TEMP_HTML_FILE%"

:: Convert the temporary HTML file to PDF
echo Converting URLs to a single PDF...
"%WKHTMLTOPDF_PATH%" "%TEMP_HTML_FILE%" "%OUTPUT_FILE%"

if errorlevel 1 (
    echo Conversion failed.
) else (
    echo Conversion successful. Output file: %OUTPUT_FILE%
)

:: Clean up
del "%TEMP_HTML_FILE%"
