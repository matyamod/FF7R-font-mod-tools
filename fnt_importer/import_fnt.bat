@echo off

set uexp=exported\End\Content\GameContents\Menu\Resident\Font\JP\SystemFontLarge4K.uexp
set fnt=fnt\sampleL.fnt
set new_uexp=new_glyph_uexp\SystemFontLarge4K.uexp
set first_page=1
set slide_offset=[0,0]
set widen_xadvance=0

python fnt_importer.py --uexp="%uexp%" --fnt="%fnt%" --new_uexp="%new_uexp%" --first_page=%first_page% --slide_offset=%slide_offset% --widen_xadvance=%widen_xadvance%

pause