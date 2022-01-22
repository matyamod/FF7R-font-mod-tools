#for End\Content\GameContents\Menu\Resident\Font\*\*.uexp

import os, json, argparse
from glyph_file import Fnt, GlyphUexp

#---args---
def get_args():
    parser = argparse.ArgumentParser() 
    parser.add_argument('--uexp', default=None)
    parser.add_argument('--fnt', default=None)
    parser.add_argument('--new_uexp', default=None, help='File name of new uexp file.')
    parser.add_argument('--first_page', default=0, type=int, help='This value will be added to all page ids in .fnt before importing them.')
    parser.add_argument('--slide_offset', default=None, help='This value will be added to all offsets in .fnt before importing them.')
    parser.add_argument('--widen_xadvance', default=0, help='This value will be added to all xadvance values in .fnt before importing them.')
    parser.add_argument('--requests', default=None, help='Loads request file.')
    parser.add_argument('--silent', action='store_true', help='Hides all messages.')
    args = parser.parse_args()
    return args

#---utils---
def mkdir(dir):
    os.makedirs(dir, exist_ok=True)

#---main---
def fnt_to_uexp(fnt_file, uexp_file, new_uexp_name=None, first_page=0, slide_offset=None, widen_xadvance=0, vorbose=False):
    if new_uexp_name is None:
        new_uexp_name = 'new_'+os.path.basename(uexp_file)

    fnt = Fnt(fnt_file, vorbose=vorbose)
    if first_page!=0:
        fnt.slide_page_index(first_page)
    if slide_offset is not None:
        fnt.slide_offset(slide_offset)
    if widen_xadvance!=0:
        fnt.widen_xadvance(widen_xadvance)

    uexp = GlyphUexp(uexp_file, vorbose=vorbose)
    uexp.import_glyph(fnt, replace_pages=True)
    uexp.save_as(new_uexp_name)

if __name__=='__main__':

    #get args
    args=get_args()
    vorbose = not args.silent
    first_page=args.first_page
    requests=args.requests
    slide_offset=args.slide_offset
    widen_xadvance=args.widen_xadvance
    if slide_offset is not None:
        if slide_offset[0]=='[':
            slide_offset=slide_offset[1:-1]
        slide_offset=slide_offset.split(',')
        for i in range(len(slide_offset)):
            slide_offset[i]=int(slide_offset[i])

    if requests is None:
        if args.uexp is None or args.fnt is None:
            raise RuntimeError('You should specify a uexp file and a fnt file.')
        #import glyph data
        fnt_to_uexp(args.fnt, args.uexp, new_uexp_name = args.new_uexp, first_page=first_page, slide_offset=slide_offset, widen_xadvance=widen_xadvance, vorbose=vorbose)

    else:
        #load .json
        with open(requests, 'r', encoding="utf-8") as f:
            requests_json = json.load(f)
        uexp_folder=requests_json['uexp_folder']
        fnt_folder=requests_json['fnt_folder']
        new_uexp_folder = requests_json['new_uexp_folder']
        requests= requests_json['requests']
        
        if uexp_folder==new_uexp_folder:
            raise RuntimeError('input folder and output folder are the same.')

        mkdir(new_uexp_folder)

        #import glyph data
        for req in requests:
            uexp_file = req['uexp']
            fnt_file = req['fnt']
            first_page = req['first_page']
            offset = req['slide_offset']
            xadvance = req['widen_xadvance']
            fnt = os.path.join(fnt_folder, fnt_file)
            uexp = os.path.join(uexp_folder, uexp_file)
            new_uexp = os.path.join(new_uexp_folder, uexp_file)
            fnt_to_uexp(fnt, uexp, new_uexp_name = new_uexp, first_page=first_page, slide_offset=offset, widen_xadvance=xadvance, vorbose=vorbose)
