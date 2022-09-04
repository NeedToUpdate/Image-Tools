from PIL import Image
import os

dir = os.path.dirname(os.path.abspath(__file__))


# finished_files = list(map(lambda x: x[:-4],os.listdir(dir + "\\png\\")))


for file in os.listdir(dir):
    if file.split('.')[-1] in ['jpg','png']:
        print(f"found {file}")
        try:
            im = Image.open(dir + '\\' + file).convert("RGBA")
            f, e = os.path.splitext(file)
            ratio = im.width/im.height
            name = (f.split('\\')[-1])
            if im.width>im.height:
                new_width = round(1200)
                new_height = round(1200*ratio)
            else:
                new_height = round(1200)
                new_width = round(1200/ratio)
            imResize = im.resize((new_height,new_width), Image.ANTIALIAS)
            imResize.save(dir + '\\resized\\' + name + '.webp', 'WEBP', quality=95)
        except Exception as e:
            print(e)
            
print("finished.")
