from PIL import  Image
import  os
def convert_format(animation,frames,dir):
    im = Image.open(animation)
    for i in range (frames):
        im.seek(i)
        im.save(dir+"frame"+str(i)+".png")
