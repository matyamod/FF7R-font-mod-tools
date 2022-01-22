#for End\Content\GameContents\Menu\Billboard\Common\*SystemFont*4K-*.uexp

import os, argparse, json

def get_args():
    parser = argparse.ArgumentParser() 
    parser.add_argument('--uexp', default=None)
    parser.add_argument('--dds', default=None)
    parser.add_argument('--new_uexp', default=None)
    parser.add_argument('--export_as_dds', action='store_true', help="Export bitmap texture as dds")
    parser.add_argument('--requests', default=None, help='Load requests.json')
    args = parser.parse_args()
    return args

def mkdir(dir):
    os.makedirs(dir, exist_ok=True)

def get_file_size(f):
    pos=f.tell()
    f.seek(0, 2)
    size = f.tell()
    f.seek(pos)
    return size

class ImageBaseClass:
    SIZE_UEXP = [5592960]
    SIZE_DDS  = [SIZE_UEXP[0] - 380, SIZE_UEXP[0] - 400]
    SIZE_RAW  = SIZE_DDS[1] - 128

    def __init__(self, file, size, extension):

        #check extension
        if file.split('.')[-1]!=extension:
            raise RuntimeError("File format error: Not .{} ({})".format(extension, file))

        self.file = file

        f = open(file, 'rb')

        #check file size
        if not get_file_size(f) in size:
            raise RuntimeError('File format error: File size should be {}. ({})'.format(size[0], file))
        return f
        
    def del_img(self):
        self.raw_img=None

    def save_as_dds(self, file, dds_header_file='dds_header_2048x2048_BC5_mipmap_DX10.bin'):
        if self.raw_img is None:
            raise RuntimeError('save_as_dds: Image data not found')
        with open(dds_header_file, 'rb') as f:
            dds_header = f.read()
        with open(file, 'wb') as f:
            f.write(dds_header)
            f.write(self.raw_img)

    def replace_img_with(self, image_object):
        if image_object.raw_img is None:
            raise RuntimeError('replace_img_with: Image data not found')
        self.raw_img = image_object.raw_img

class DDS(ImageBaseClass):
    # pixel format: BC5
    # size: 2048x2048
    # mipmap: true

    def __init__(self, dds_file):
        dds = super(DDS, self).__init__(dds_file, ImageBaseClass.SIZE_DDS, 'dds')
        self.header = dds.read(128)
        self.fourCC = self.header[84:88]
        if self.fourCC.decode()=='DX10':
            self.header2=dds.read(20)

        self.raw_img = dds.read(DDS.SIZE_RAW)
        dds.close()

class FontBitmapUexp(ImageBaseClass):
    #for Menu\Billboard\Common\*SystemFont*4K-*.uexp
    
    UNREAL=b'\xC1\x83\x2A\x9E' #Unreal signature

    def __init__(self, uexp_file):
        uexp = super(FontBitmapUexp, self).__init__(uexp_file, ImageBaseClass.SIZE_UEXP, 'uexp')
        self.header = uexp.read(116)
        self.raw_img = uexp.read(FontBitmapUexp.SIZE_RAW)
        self.footer=uexp.read(412)
        if self.footer[-4:]!=FontBitmapUexp.UNREAL:
            raise RuntimeError('File format error: Unreal signature not found')
        uexp.close()

    def save_as_uexp(self, file):
        if self.raw_img is None:
            raise RuntimeError('save_as_uexp: Image data not found')
        with open(file, 'wb') as f:
            f.write(self.header)
            f.write(self.raw_img)
            f.write(self.footer)

def dds_to_fontBitmap(dds_file, uexp_file, new_uexp_name=None):
    uexp = FontBitmapUexp(uexp_file)
    dds = DDS(dds_file)
    uexp.replace_img_with(dds)
    if new_uexp_name is None:
        new_uexp_name = 'new_'+os.path.basename(uexp_file)
    uexp.save_as_uexp(new_uexp_name)
    print(new_uexp_name+' has been generated successfully.')

def fontBitmap_to_dds(uexp_file, dds_name=None):
    uexp = FontBitmapUexp(uexp_file)
    if dds_name is None:
        dds_name = 'new_'+os.path.basename(uexp_file)[:-4]+"dds"
    uexp.save_as_dds(dds_name)
    print(dds_name+' has been generated successfully.')

if __name__=='__main__':
    args = get_args()
    if args.export_as_dds:
        if args.uexp is None:
            raise RuntimeError('You should specify a uexp file.')
        fontBitmap_to_dds(args.uexp, dds_name = args.dds)
    
    else:

        requests = args.requests
        if requests is None:
            if args.uexp is None:
                raise RuntimeError('You should specify a uexp file.')
            if args.dds is None:
                raise RuntimeError('You should specify a DDS file.')
            dds_to_fontBitmap(args.dds, args.uexp, new_uexp_name = args.new_uexp)

        else:
            with open(requests, 'r', encoding="utf-8") as f:
                requests_json = json.load(f)
            uexp_folder=requests_json['uexp_folder']
            dds_folder=requests_json['dds_folder']
            new_uexp_folder = requests_json['new_uexp_folder']
            requests = requests_json['requests']

            if uexp_folder==new_uexp_folder:
                raise RuntimeError('input folder and output folder are the same.')

            mkdir(new_uexp_folder)
            for req in requests:
                uexp = req['uexp']
                dds = req['dds']
                dds_file = os.path.join(dds_folder, dds)
                uexp_file = os.path.join(uexp_folder, uexp)
                new_uexp_file = os.path.join(new_uexp_folder, uexp)
                dds_to_fontBitmap(dds_file, uexp_file, new_uexp_name = new_uexp_file)