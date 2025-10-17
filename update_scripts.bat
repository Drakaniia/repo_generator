@echo off
REM Quick script updater for Windows
REM Run this to update all Python scripts with UTF-8 fixes

echo ================================================
echo   Updating Python Scripts with UTF-8 Fixes
echo ================================================
echo.

REM Backup old files
echo Creating backups...
if exist daily_activity.py (
    copy /Y daily_activity.py daily_activity.py.backup >nul 2>&1
    echo   - daily_activity.py backed up
)
if exist auto_update.py (
    copy /Y auto_update.py auto_update.py.backup >nul 2>&1
    echo   - auto_update.py backed up
)
if exist update_profile.py (
    copy /Y update_profile.py update_profile.py.backup >nul 2>&1
    echo   - update_profile.py backed up
)
if exist test_automation.py (
    copy /Y test_automation.py test_automation.py.backup >nul 2>&1
    echo   - test_automation.py backed up
)

echo.
echo Backups created with .backup extension
echo.
echo ================================================
echo Please update the files manually:
echo 1. Copy the fixed code from the artifacts
echo 2. Save each file with UTF-8 encoding
echo ================================================
echo.
echo Alternative: Use the Linux/Mac update script
echo   Run: bash update_scripts.sh
echo.
pause