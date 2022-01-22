# FF7R Font Mod Tools

Tools for importing font data (`.ttf`) into FF7R (Final Fantasy VII Remake)

<img src = "image/sample.jpg" width=600>

<br>

## Other Tools You Will Need

- [BMFont](https://www.angelcode.com/products/bmfont/): Generates bitmap textures (`.dds`) and glyph data (`.fnt`) from `.ttf`.
- [NVIDIA Texture Tools](https://developer.nvidia.com/nvidia-texture-tools-exporter): Converts bitmap textures to BC5 format.

## Over view

- `FF7R.bmfc`: Configuration file for BMFont.
- `dds_to_bc5.bat`: Batch file for running NVIDIA Texture Tools with CLI.
- `fnt_importer`: Tool for importing glyph data from `.fnt` into `.uexp`.
- `font_4Ktexture_replacer`: DDS replacer for font bitmap.
