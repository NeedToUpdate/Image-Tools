import argparse
import os
from PIL import Image
import eel
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from src.models.modnet import MODNet
import sys

class ImageToolbox():

    def __init__(self, input_path='./input',output_path='./output'):
        self.max_res = None
        self.compression = 95
        self.output_path = output_path
        self.input_path = input_path
        self.strip_exif = True
        self.filetype = "PNG"
        self.remove_bg = False
        self.modnet = None
        self.im_transform = None

    def get_extension(self, image_ext):
        if image_ext == 'JPEG':
            return '.jpg'
        else:
            return '.' + image_ext.lower()

    def convert(self, file):
        im = Image.open(os.path.join(self.input_path, file)).convert(
            "RGBA" if self.filetype in ['WEBP', 'PNG'] else 'RGB')
        f, e = os.path.splitext(file)
        name = (f.split('\\')[-1])
        new_height, new_width = im.height, im.width
        if self.max_res and (im.width > self.max_res or im.height > self.max_res):
            ratio = im.width/im.height
            if im.width > im.height:
                new_width = round(self.max_res)
                new_height = round(self.max_res/ratio)
            else:
                new_height = round(self.max_res)
                new_width = round(self.max_res*ratio)
        imResize = im.resize((new_width, new_height), Image.Resampling.LANCZOS)
        new_name = name + (self.get_extension(self.filetype) if self.filetype is not None else e)
        if self.strip_exif:
            imResize = self.remove_exif(imResize)
        if self.remove_bg:
            imResize = self.remove_background(imResize)
        imResize.save(os.path.join(self.output_path, new_name),
                      self.filetype, quality=self.compression)

    def remove_exif(self, image):
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        return image_without_exif

    def combined_display(self, image, matte):
        image = np.asarray(image)
        if len(image.shape) == 2:
            image = image[:, :, None]
        if image.shape[2] == 1:
            image = np.repeat(image, 3, axis=2)
        elif image.shape[2] == 4:
            image = image[:, :, 0:3]
        if self.filetype == 'JPEG':
            foreground = image*np.stack([np.asarray(matte).astype(np.uint8)>0]*3,2)
        else:
            foreground = np.dstack((image, np.asarray(matte).astype(np.uint8)))
        if self.filetype is None:
            self.filetype = 'PNG'
        return Image.fromarray(np.uint8(foreground))

    def remove_background(self, image):

        # unify image channels to 3
        im = np.asarray(image)
        if len(im.shape) == 2:
            im = im[:, :, None]
        if im.shape[2] == 1:
            im = np.repeat(im, 3, axis=2)
        elif im.shape[2] == 4:
            im = im[:, :, 0:3]

        # convert image to PyTorch tensor
        im = Image.fromarray(im)
        im = self.im_transform(im)

        # add mini-batch dim
        im = im[None, :, :, :]

        # resize image for input
        im_b, im_c, im_h, im_w = im.shape
        if max(im_h, im_w) < ref_size or min(im_h, im_w) > ref_size:
            if im_w >= im_h:
                im_rh = ref_size
                im_rw = int(im_w / im_h * ref_size)
            elif im_w < im_h:
                im_rw = ref_size
                im_rh = int(im_h / im_w * ref_size)
        else:
            im_rh = im_h
            im_rw = im_w

        im_rw = im_rw - im_rw % 32
        im_rh = im_rh - im_rh % 32
        im = F.interpolate(im, size=(im_rh, im_rw), mode='area')

        # inference
        _, _, matte = modnet(
            im.cuda() if torch.cuda.is_available() else im, True)

        # resize and save matte
        matte = F.interpolate(matte, size=(im_h, im_w), mode='area')
        matte = matte[0][0].data.cpu().numpy()
        matte = Image.fromarray(((matte * 255).astype('uint8')), mode='L')
        return self.combined_display(image, matte)


TOOLBOX = None



@eel.expose
def set_param(param:str, value):
    global TOOLBOX
    print(param, value)
    if param == 'max_res':
        if value == 'None':
            TOOLBOX.max_res = None
        else:
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
    elif param == 'filetype':
        if value == 'webp':
            TOOLBOX.filetype = 'WEBP'
        elif value == 'jpg':
            TOOLBOX.filetype = 'JPEG'
        elif value == 'png':
            TOOLBOX.filetype = 'PNG'
        elif value == 'no conversion':
            TOOLBOX.filetype = None
    elif param == 'remove_bg':
        TOOLBOX.remove_bg = bool(value)


@eel.expose
def create_folder(path):
    os.mkdir(path)

@eel.expose
def get_images():
    global TOOLBOX
    return [im for im in os.listdir(TOOLBOX.input_path) if im.lower().endswith(('png','webp','jpg','jpeg'))]
    
@eel.expose
def convert(image):
    global TOOLBOX
    print(image)
    TOOLBOX.convert(image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', type=str,
                        help='path of input images', default="./input")
    parser.add_argument('--output-path', type=str,
                        help='path of output images', default='./output')
    args = parser.parse_args()
    if not os.path.exists(args.input_path):
        print('Cannot find input path: {0}'.format(args.input_path))
        os.mkdir(args.input_path)
    if not os.path.exists(args.output_path):
        print('Cannot find output path: {0}. Creating...'.format(
            args.output_path))
        os.mkdir(args.output_path)
    TOOLBOX = ImageToolbox(args.output_path)
    TOOLBOX.input_path = args.input_path

    eel.init('web')

    

    #torch MODNet Stuff
    # define hyper-parameters
    ref_size = 512

    # define image to tensor transform
    im_transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ]
    )

    # create MODNet and load the pre-trained ckpt
    modnet = MODNet(backbone_pretrained=False)
    modnet = nn.DataParallel(modnet)

    if torch.cuda.is_available():
        modnet = modnet.cuda()
        if getattr(sys, 'frozen', False):
            weights = torch.load(os.path.join(sys._MEIPASS,'pretrained/modnet_photographic_portrait_matting.ckpt'))
        else:
            weights = torch.load('pretrained/modnet_photographic_portrait_matting.ckpt')
    else:
        if getattr(sys, 'frozen', False):
            weights = torch.load(os.path.join(sys._MEIPASS,'pretrained/modnet_photographic_portrait_matting.ckpt'), map_location=torch.device('cpu'))
        else:
            weights = torch.load('pretrained/modnet_photographic_portrait_matting.ckpt', map_location=torch.device('cpu'))

    modnet.load_state_dict(weights)
    modnet.eval()

    TOOLBOX.im_transform = im_transform
    TOOLBOX.modnet = modnet

    eel.start('./ui/index.html', size=(600,600))