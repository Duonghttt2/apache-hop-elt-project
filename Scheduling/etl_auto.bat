@echo off
set D=%date:~0,2%
set M=%date:~3,2%
set Y=%date:~6,4%
set LOG_FILE=etl_log_%D%_%M%_%Y%.txt

echo Dang chay ETL va ghi Log vao file %LOG_FILE%...

cd /d "C:\hop"

call hop-run.bat --project "etl-project_1" -r local -f "D:\apache-hop-project\Workflows\03_data_workflow.hwf" -l Basic >> "D:\apache-hop-project\Log\%LOG_FILE%" 2>&1

echo Da chay xong toan bo he thong!
pause