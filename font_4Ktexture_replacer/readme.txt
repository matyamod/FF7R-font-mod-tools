How to Use font_4Ktexture_replacer.exe by MatyaModding

Usage
  fnt_importer.exe --uexp=uexp --dds=dds [options]

  uexp: uexp file
  dds: dds file
  --new_uexp=new_uexp: File name of a new uexp file.
  --requests=requests.json: Sets parameters with .json.
  --exports_as_dds: Exports bitmap from uexp as dds.

How to Use font_4Ktexture_replacer.py with requests.json

  You can set the parameters with a json file.

  1. Edit requests.json
    uexp_folder: Uexp folder you want to mod.
    dds_folder: Where dds files are.
    new_uexp_folder: New uexp files will be generated here.

    requests: Runs the replacer for each parameter set.
      uexp: File name of uexp. All files should be in 'uexp_folder'.
      dds: File name of dds. All files should be in 'dds_folder'.
  
  2. Run replace_texture_requests.bat
