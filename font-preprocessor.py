import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageChops
from string import ascii_lowercase
from string import ascii_uppercase
import numpy as np
from os import listdir
from os.path import isfile, join
# font = ImageFont.truetype("Arial-Bold.ttf",14)

def main():
    font_dir = "fonts/"
    font_files = [f for f in listdir(font_dir) if isfile(join(font_dir, f))]
    train_data = []
    for i in font_files:
        print (i)
        train_data += gen_data(font_dir + i)
    write_data("data/input.data", train_data, 400, 62)


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
def identity(size):
    matrix = []
    for i in range(size):
        line = "0 "*size
        line = line[:-2]
        line = line[:i*2] + "1 " + line[i*2:]
        matrix.append(line)

    return matrix

def gen_data(font_file):
    font = ImageFont.truetype(font_file,20)
    maxsize = (20, 20)
    letters = ascii_uppercase + ascii_lowercase + '0123456789'

    character_maps = []

    for char in letters:
        img=Image.new("RGBA", (20,50),(255,255,255))

        draw = ImageDraw.Draw(img)
        draw.text((0, 0),char,(0,0,0),font=font)
        draw = ImageDraw.Draw(img)

        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] > 50 and item[1] > 50 and item[2] > 50:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)



        img=trim(img)
        #img = img.resize((20, 20))

        bg = Image.new("RGB", img.size, (255,255,255))
        bg.paste(img,img)
        bg.save("img/"+font_file[:-4]+"-"+char+".png")

        data = bg.getdata()

        pixellist = ""
        for pixel in data:
            if pixel == (255, 255, 255):
                val = 1
            else:
                val = 0
            pixellist += str(val) + " "
        pixellist = pixellist[:-1]


        character_maps.append(pixellist)

    data =[]
    correct = identity(len(letters))

    for x in range(len(character_maps)):
        data.append(character_maps[x])
        data.append(correct[x])

    return data

def write_data(filename, data, num_in, num_out):
    to_write = "%i %i %i\n" % (len(data) / 2, num_in, num_out)
    to_write += "\n".join(data)
    f = open(filename, "w")
    f.write(to_write)
    f.close





main()
