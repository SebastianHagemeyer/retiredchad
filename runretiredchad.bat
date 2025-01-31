@echo off
:loop
echo Running GPT...
python whyScan.py
echo Waiting for 10 seconds before restarting...
timeout /t 10
goto loop