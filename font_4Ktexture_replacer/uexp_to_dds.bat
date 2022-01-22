@echo off

REM Drop a uexp file onto this (uexp_to_dds.bat)
REM A new .dds file will be generated.

@if "%~1"=="" goto skip

@pushd %~dp0
python font_4Ktexture_replacer.py --uexp="%~1" --export_as_dds
@popd

pause

:skip