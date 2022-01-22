@echo off

REM Replaces bitmap data with dds

set uexp=asset\U_Com_JP_SystemFontLarge4K-01.uexp
set dds=dds\sampleL.dds
set new_uexp=new_bitmap_uexp\U_Com_JP_SystemFontLarge4K-01.uexp

python font_4Ktexture_replacer.py --uexp="%uexp%" --dds="%dds%" --new_uexp="%new_uexp%"

pause