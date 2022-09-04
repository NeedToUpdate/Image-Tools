from PIL import Image

import sys



image = Image.open(sys.argv[-1])

# next 3 lines strip exif
data = list(image.getdata())
image_without_exif = Image.new(image.mode, image.size)
image_without_exif.putdata(data)

image_without_exif.save(sys.argv[-1])