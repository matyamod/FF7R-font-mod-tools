## fnt_importer

### Usage
  
  ```
  fnt_importer.exe --uexp=uexp --fnt=fnt [options]
  ```
  
  - uexp: uexp file
  - fnt: fnt file
  - --new_uexp=*: File name of a new uexp file.
  - --first_page=i: This value will be added to all page ids in .fnt before importing them.
  - --slide_offset=[x,y]: This value will be added to all offsets in .fnt before importing them.
  - --widen_xadvance=w: This value will be added to all xadvance values in .fnt before importing them.
  - --requests=*.json: Sets parameters with .json.
  - --silent: Hides all messages.


### How to Use fnt_impoter with requests.json

  You can set the parameters with a json file.

  #### 1. Edit requests.json
  
  - uexp_folder: Uexp folder you want to mod.
  - fnt_folder: Where fnt files are.
  - new_uexp_folder: New uexp files will be generated here.
  - requests: Runs the importer for each parameter set.
    + uexp: File name of uexp. All files should be in 'uexp_folder'.
    + fnt: File name of fnt. All files should be in 'fnt_folder'. 
    + first_page: This value will be added to all page ids in .fnt before importing them.
    + slide_offset: This value will be added to all offsets in .fnt before importing them.
    + widen_xadvance: This value will be added to all xadvance values in .fnt before importing them.
  
  #### 2. Run import_fnt_requests.bat
