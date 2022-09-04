from PIL import Image
import os

dir = os.getcwd()

finished_files = list(map(lambda x: x[:-4],os.listdir(dir + "\\png\\")))

filetypes = ['webp']

for file in os.listdir(dir):
    if file.split('.')[-1] in filetypes:
        if ''.join(file.split('.')[:-1]) in finished_files:
            continue
        print(f"found {file}")
        im = Image.open(file).convert("RGBA")
        im.save("./png/" + ''.join(file.split('.')[:-1]) + ".png", "png")
print("finished.")
