from PIL import Image, ImageSequence

im = Image.open("src/Invicon_Gear.gif")

def iter_frames(im):
    try:
        i = 0
        while 1:
            im.seek(i)
            imframe = im.copy()
            yield imframe
            i += 1
    except EOFError:
        pass

for i, frame in enumerate(iter_frames(im)):
    frame.save('src/gear/%d.png' % i,**frame.info)