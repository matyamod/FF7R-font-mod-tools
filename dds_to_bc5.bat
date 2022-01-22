rem @echo off

REM Drop a dds file onto this (dds_to_bc5.bat)
REM A new .dds file will be generated.

set dir=C:\Program Files\NVIDIA Corporation\NVIDIA Texture Tools

@if "%~1"=="" goto skip

set a=%~1

@pushd %~dp0
"%dir%\nvtt_export.exe" -f 21 -o "%a:~0,-4%_bc5.dds" "%~1%"
@popd

pause

:skip