import argparse
import os
from PIL import Image
import eel


class ImageToolbox():

    def __init__(self, input_path='./input',output_path='./output'):
        self.max_res = 10000
        self.compression = 95
        self.output_path = output_path
        self.input_path = input_path
        self.strip_exif = True
        pass

    def get_extension(self, image_ext):
        if image_ext == 'JPEG':
            return '.jpg'
        else:
            return '.' + image_ext.lower()

    def convert_to(self, file, image_ext='WEBP'):
        if image_ext not in ['WEBP', 'PNG', 'JPEG']:
            raise TypeError(
                image_ext + ' is not a valid image extension. Allowed: WEBP PNG JPEG')
        im = Image.open(file).convert(
            "RGBA" if image_ext in ['WEBP', 'PNG'] else 'RGB')
        f, e = os.path.splitext(file)
        name = (f.split('\\')[-1])
        new_height, new_width = im.height, im.width
        if im.width > self.max_res or im.height > self.max_res:
            ratio = im.width/im.height
            if im.width > im.height:
                new_height = round(self.max_res)
                new_width = round(self.max_res*ratio)
            else:
                new_width = round(self.max_res)
                new_height = round(self.max_res/ratio)
        imResize = im.resize((new_width, new_height), Image.Resampling.LANCZOS)
        new_name = name + self.get_extension(image_ext)
        if self.strip_exif:
            imResize = self.remove_exif(imResize)
        imResize.save(os.path.join(self.output_path, new_name),
                      image_ext, quality=self.compression)

    def remove_exif(self, image):
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        return image_without_exif


TOOLBOX = None


@eel.expose
def set_param(param:str, value):
    global TOOLBOX
    if param == 'max_res':
        TOOLBOX.max_res = int(value)
    elif param == 'compression':
        TOOLBOX.compression = int(value)
    elif param == 'output_path':
        if not os.path.exists(value):
            raise Exception(f'Cannot find output path: {value}')
        TOOLBOX.output_path = value
    elif param == 'strip_exif':
        TOOLBOX.strip_exif = bool(value)
    elif param == 'input_path':
        if not os.path.exists(value):
            raise Exception(f'Cannot find output path: {value}')
        TOOLBOX.input_path = str(value)


@eel.expose
def create_folder(path):
    os.mkdir(path)

@eel.expose
def get_images():
    global TOOLBOX
    return [os.path.join('../input/',im).replace('\\','/') for im in os.listdir(TOOLBOX.input_path) if im.lower().endswith(('png','webp','jpg','jpeg'))]
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', type=str,
                        help='path of input images', default="./input")
    parser.add_argument('--output-path', type=str,
                        help='path of output images', default='./output')
    args = parser.parse_args()
    if not os.path.exists(args.input_path):
        print('Cannot find input path: {0}'.format(args.input_path))
        exit()
    if not os.path.exists(args.output_path):
        print('Cannot find output path: {0}. Creating...'.format(
            args.output_path))
        os.mkdir(args.output_path)
        exit()
    TOOLBOX = ImageToolbox(args.output_path)
    TOOLBOX.input_path = args.input_path

    eel.init('./build/')

    eel.start('./ui/index.html', size=(1000,600))