import os

#---utils---

def get_file_size(f):
    pos=f.tell()
    f.seek(0, 2)
    size = f.tell()
    f.seek(pos)
    return size

def read_uint32(file):
    bin = file.read(4)
    return int.from_bytes(bin, "little")

def read_uint16(file):
    bin = file.read(2)
    return int.from_bytes(bin, "little")

def read_uint8(file):
    bin = file.read(1)
    return int.from_bytes(bin, "little")

def read_int16(file):
    bin = file.read(2)
    return int.from_bytes(bin, "little", signed=True)

def read_str(file):
    num = read_uint32(file)
    if num==0:
        return None
    string = file.read(num-1).decode()
    file.seek(1,1)
    return string

def write_uint32(file, n):
    bin = n.to_bytes(4, byteorder="little")
    file.write(bin)

def write_uint16(file, n):
    bin = n.to_bytes(2, byteorder="little")
    file.write(bin)

def write_int16(file, n):
    bin = n.to_bytes(2, byteorder="little", signed=True)
    file.write(bin)

def write_uint8(file, n):
    bin = n.to_bytes(1, byteorder="little")
    file.write(bin)

def write_str(file, s):
        num = len(s)+1
        num_byte = num.to_bytes(4, 'little')
        str_byte = s.encode()
        file.write(num_byte + str_byte + b'\x00')

#---objects---

class Glyph:
    # Glyph object
    
    # type=0: .fnt : (unicode, x, y, w, h, xoffset, yoffset, xadvance, page, chnl)
    # type=1: .uexp : (unicode, page, x, y, w, h, xoffset, yoffset, xadvance)
    def __init__(self, f, type):
        if type==0:
            self.unicode=read_uint32(f)
        else:
            self.unicode=read_uint16(f)
            self.page=read_uint16(f)

        self.x=read_uint16(f)
        self.y=read_uint16(f)
        self.width=read_uint16(f)
        self.height=read_uint16(f)
        self.xoffset=read_int16(f)
        self.yoffset=read_int16(f)
        self.xadvance=read_uint16(f)

        if type==0:
            self.page=read_uint8(f)
            self.chnl=read_uint8(f)

    def write(self, f):
        write_uint16(f, self.unicode)
        write_uint16(f, self.page)
        write_uint16(f, self.x)
        write_uint16(f, self.y)
        write_uint16(f, self.width)
        write_uint16(f, self.height)
        write_int16(f, self.xoffset)
        write_int16(f, self.yoffset)
        write_uint16(f, self.xadvance)

    def is_in_page(self, page):
        return self.page==page
    
    def update(self, glyph):
        if self.unicode!=glyph.unicode:
            raise RuntimeError('Wrong glyph')
        self.page=glyph.page
        self.x=glyph.x
        self.y=glyph.y
        self.width=glyph.width
        self.height=glyph.height
        self.xoffset=glyph.xoffset
        self.yoffset=glyph.yoffset
        self.xadvance=glyph.xadvance

    def print(self, padding=2):
        print(' '*padding+'[{}, {}, {}, {}, {}, {}, {}, {}, {}]'.format(\
            self.unicode, self.page, self.x, self.y, self.width, self.height,\
            self.xoffset, self.yoffset, self.xadvance))

class Kerning:
    def __init__(self, f):
        self.first=read_uint32(f)
        self.second=read_uint32(f)
        self.amount=read_int16(f)

class GlyphFileBase:
    def __init__(self, file, extension, vorbose=False):
        self.vorbose=vorbose
        if self.vorbose:
            print('Loading '+file+'...')

        #check extension
        if file.split('.')[-1]!=extension:
            raise RuntimeError("File format error: Not .{} ({})".format(extension, file))

        self.file = file

    def remove_page(self, page):
        new_glyphs=[]
        for g in self.glyphs:
            if not g.is_in_page(page):
                new_glyphs.append(g)
        removed=len(self.glyphs)-len(new_glyphs)
        self.glyphs=new_glyphs

        if self.vorbose:
            print('Glyph data in page {} has been removed.'.format(page))
            print('  removed count: {}'.format(removed))

    def slide_page_index(self, slide):
        if slide==0:
            return
        for g in self.glyphs:
            g.page+=slide
        if self.vorbose:
            print('page index += {}'.format(slide))

    def slide_offset(self, offset):
        if offset is None or offset==[0,0]:
            return
        for g in self.glyphs:
            g.xoffset+=offset[0]
            g.yoffset+=offset[1]
        if self.vorbose:
            print('offset += {}'.format(offset))

    def widen_xadvance(self, xadvance):
        if xadvance==0:
            return
        for g in self.glyphs:
            g.xadvance+=xadvance
        if self.vorbose:
            print('xadvance += {}'.format(xadvance))

    def get_page_range(self):
        a, b = 100, 0
        for g in self.glyphs:
            p = g.page
            a=min(a, p)
            b=max(b, p)
        return a,b

    def get_size_range(self):
        wa, wb = 100, 0
        ha, hb = 100, 0
        for g in self.glyphs:
            w = g.width
            h = g.height
            wa=min(wa, w)
            wb=max(wb, w)
            ha=min(ha, h)
            hb=max(hb, h)
        return wa, wb, ha, hb
    
    def get_same_code_glyph(self, unicode):
        same=None
        for g in self.glyphs:
            if g.unicode==unicode:
                same=g
                break
        return same
    
    def print_page_range(self, padding=2):
        a,b=self.get_page_range()
        print(' '*padding+'page: {} ~ {}'.format(a,b))
    
    def print_size_range(self, padding=2):
        a, b, c, d = self.get_size_range()
        print(' '*padding+'width: {} ~ {}'.format(a,b))
        print(' '*padding+'height: {} ~ {}'.format(c,d))

    def print_glyph_sample(self, num=5, padding=2):
        pad = ' '*padding
        print(pad+'Glyph samples')
        print(pad+'  [unicode, page, x, y, w, h, xoffset, yoffset, xadvance]')
        num = min(len(self.glyphs), num)
        for i in range(num):
            g=self.glyphs[i]
            g.print(padding=padding+2)
    
    def print(self, padding=2):
        print(' '*padding+'font size: {}'.format(self.font_size))
        print(' '*padding+'char count: {}'.format(len(self.glyphs)))
        self.print_page_range(padding=padding)
        self.print_size_range(padding=padding)
        self.print_glyph_sample(padding=padding)

class Fnt(GlyphFileBase):
    # .fnt
    # https://angelcode.com/products/bmfont/doc/file_format.html
    #
    # byte {5} - magic
    # uint32 {4} - info size
    # info {
    #   uint16 {2} - font size
    #   bits {1} - bit0: smooth, bit1: unicode, bit2: italic, bit3: bold, bit4: fiexedHeight
    #   byte {1} - charSet
    #   uint16 {2} - stretchH
    #   byte {1} - aa
    #   byte {4} - padding (x,x,x,x)
    #   byte {2} - spacing (x,x)
    #   uint8 {1} - outline thickness
    #   byte {info size - 14} - font name (e.g. Arial)
    # }
    # byte {5} - ?
    # uint16 {2} - lineHeight
    # uint16 {2} - base
    # uint16 {2} - scaleW
    # uint16 {2} - scaleH
    # uint8 {1} - number of pages
    # bits {1} - bitField
    # bits {1} - alphaChnl
    # bits {1} - redChnl
    # bits {1} - greenChnl
    # bits {1} - blueChnl
    # byte {2} - ?
    # uint32 {4} - string length
    # byte {x} - name of texture files
    # byte {1} - ?
    # uint32 {4} - data size (number of charactors * 20)
    # for each glyph
    #   glyph {20} - glyph data
    # if kerning data exists {
    #   byte {1} - ?
    #   uint32 {4} - data size (number of kernings * 10)
    #   for each kerning
    #     kerning {10} - kerning data
    # }

    HEAD = b'\x42\x4d\x46\x03\x01' #BMF**

    #load fnt file
    def __init__(self, fnt_file, vorbose=False):
        super(Fnt, self).__init__(fnt_file, 'fnt', vorbose)
        fnt = open(fnt_file, 'rb')
        size = get_file_size(fnt)
        head=fnt.read(5)
        if head!=Fnt.HEAD:
            raise RuntimeError("Not .fnt generated by BMFont")

        info_size=read_uint32(fnt)
        self.font_size = read_uint16(fnt)
        fnt.seek(11,1)
        self.outline = read_uint8(fnt)
        self.font_name = fnt.read(info_size-14).decode()
        
        fnt.seek(5,1)
        self.lineHeight=read_uint16(fnt)
        self.base=read_uint16(fnt)
        self.scaleW=read_uint16(fnt)
        self.scaleH=read_uint16(fnt)
        self.pages = read_uint8(fnt)
        fnt.seek(7,1)
        _ = read_str(fnt)
        fnt.seek(1,1)

        data_size = read_uint32(fnt)
        data_num = data_size//20

        self.glyphs=[]
        for i in range(data_num):
            glyph=Glyph(fnt,0)
            self.glyphs.append(glyph)
        
        self.kernings=[]
        if fnt.tell()!=size:
            fnt.seek(1,1)
            kerning_size = read_uint32(fnt)
            kerning_num = kerning_size//10
            for i in range(kerning_num):
                kerning=Kerning(fnt)
                self.kernings.append(kerning)
            
            if fnt.tell()!=size:
                raise RuntimeError("Parse failed (.fnt)")

        fnt.close()

        if self.vorbose:
            self.print()

    def print(self, padding=2):
        pad = ' '*padding
        print(pad+'font: '+self.font_name)
        print(pad+'texture width: {}'.format(self.scaleW))
        print(pad+'texture height: {}'.format(self.scaleH))
        print(pad+'texture count: {}'.format(self.pages))
        n = len(self.kernings)
        if n>0:
            print(pad+"kerning count: {}".format(n))
        super(Fnt, self).print(padding=padding)

class GlyphUexp(GlyphFileBase):
    #.uexp for glyph data (End\Content\GameContents\Menu\Resident\Font\*\*.uexp)

    # byte {6 or 8} - header? (\x01\x09\x00\x00\x00\x00 or \x01\x02\x01\x05\x00\x00\x00\x00) 
    # uint32 {4} - data size (number of glyphs * 18)
    # for each glyph
    #   glyph {18} - glyph data without chnl
    # if header is \x01\x09\x00\x00\x00\x00 {
    #   byte {4} - null?
    #   uint32 {4} - number of strings
    #   for eche string
    #     uint32 {4} - string length
    #     byte {x} - string i
    #     uint8 {1} - i
    #     byte {1} - \xE0
    # }
    # uint32 {4} - font size
    # uint32 {4} - outline thickness
    # uint32 {4} - null?
    # byte {4} - Unreal signature (\xC1\x83\x2A\x9E)

    HEAD = b'\x01\x09'
    HEAD2 = b'\x01\x02\x01\x05'
    FOOT = b"\xC1\x83\x2A\x9E"

    #load uexp file
    def __init__(self, uexp_file, vorbose=False):
        super(GlyphUexp, self).__init__(uexp_file, 'uexp', vorbose)
        
        uexp = open(uexp_file, 'rb')
        self.size = get_file_size(uexp)
        self.head=uexp.read(2)
        if self.head!=GlyphUexp.HEAD:
            uexp.seek(0)
            self.head=uexp.read(4)
            if self.head!=GlyphUexp.HEAD2:
                raise RuntimeError("Not .uexp for glyph data")
        zero = read_uint32(uexp)
        if zero!=0:
            raise RuntimeError("Not .uexp for glyph data")
        data_num = read_uint32(uexp)
        self.glyphs=[]
        for i in range(data_num):
            glyph = Glyph(uexp, 1)
            self.glyphs.append(glyph)

        if self.head==GlyphUexp.HEAD:
            self.null=uexp.read(4)        
            info_num = read_uint32(uexp)
            self.info=[]
            for i in range(info_num):
                s = read_str(uexp)
                self.info.append(s)
                uexp.seek(2,1)

        self.font_size=read_uint32(uexp)
        self.outline=read_uint32(uexp)
        self.unknown=uexp.read(4)
        self.foot = uexp.read(4)

        if self.foot[-4:]!=GlyphUexp.FOOT:
            raise RuntimeError("Not .uexp!")

        if uexp.tell()!=self.size:
            raise RuntimeError("Parse failed (.uexp)")

        uexp.close()

        if self.vorbose:
            self.print()

    #update or add glyph data
    def import_glyph(self, glyph_file_data, replace_pages=True):
        if replace_pages:
            a,b = glyph_file_data.get_page_range()
            for i in range(a,b+1):
                self.remove_page(i)

        added=0
        updated=0
        for g in glyph_file_data.glyphs:
            unicode = g.unicode
            same = self.get_same_code_glyph(unicode)
            if same is None:
                self.glyphs.append(g)
                added+=1
            else:
                same.update(g)
                updated+=1

        if self.vorbose:
            print('Glyph data has been imported.')
            print(' updated: {}, added: {}'.format(updated,added))

    #save as .uexp
    def save_as(self, file):
        if self.vorbose:
            print('Saving as '+file+'...')
            self.print()
        f = open(file, 'wb')
        f.write(self.head)
        write_uint32(f,0)
        write_uint32(f, len(self.glyphs))
        for g in self.glyphs:
            g.write(f)

        if self.head==GlyphUexp.HEAD:
            f.write(self.null)
            write_uint32(f, len(self.info))
            for i in range(len(self.info)):
                s = self.info[i]
                write_str(f, s)
                write_uint8(f, i)
                f.write(b'\xE0')

        write_uint32(f, self.font_size)
        write_uint32(f, self.outline)
        f.write(self.unknown)
        f.write(self.foot)
        size = f.tell()

        f.close()

        uasset_file = self.file[:-4] + 'uasset'
        new_uasset_file = file[:-4] + 'uasset'
        if not os.path.exists(uasset_file):
            raise RuntimeError('File not found. .uasset should be in the same directory as .uexp. ('+ uasset_file +')')
        with open(uasset_file, 'rb') as f:
            bin = f.read()
        with open(new_uasset_file, 'wb') as f:
            f.write(bin[:-92])
            write_uint32(f, size-4)
            f.write(bin[-88:])

        if self.vorbose:
            print('Done!')
            print('')
