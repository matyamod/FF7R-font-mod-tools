@echo off

REM Replaces bitmap data with dds
REM You need to edit requests.json before running this .bat file.

python font_4Ktexture_replacer.py --requests=requests.json

pause