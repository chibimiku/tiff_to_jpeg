#一个简单的程序，用于自动寻找目录下所有的.tif文件，将其按允许的最大体积转化为jpg。
#方案是先尝试100%质量，如果超过需求体积

import os
from PIL import Image

convert_path = 'data/'
#max_size = '20971520' #最大字节数，这里设置的是20M
max_size = 512000

#TIF to JPG的代码 原型来自 https://stackoverflow.com/questions/28870504/converting-tiff-to-jpeg-in-python

def try_save_image(in_im, target_path, max_size = 20971520, max_quality = 98):
    using_quality = max_quality
    while (True):
        in_im.save(target_path, "JPEG", quality=using_quality)
        new_size = os.path.getsize(target_path)
        print ("checking ... new size is:" + str(new_size) + " for file:" + target_path + ", with quality " + str(using_quality))
        if(new_size <= max_size or using_quality < 5):
            break
        using_quality = using_quality - 1 #降低一档再重新来过

for root, dirs, files in os.walk(convert_path, topdown=False):
    for name in files:
        print(os.path.join(root, name))
        file_ext_name = os.path.splitext(os.path.join(root, name))[1].lower()
        if (file_ext_name == ".tif" or file_ext_name == '.tiff'):
            if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
                print ("A jpeg file already exists for %s" % name)
            # If a jpeg is *NOT* present, create one from the tiff.
            else:
                outfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
                try:
                    im = Image.open(os.path.join(root, name))
                    #针对alpha通道进行处理，混合体
                    #https://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil
                    
                    if (len(im.split()) == 4):
                        print ("It seems an RGBA image, remove alpha data.")
                        '''
                        background = Image.new("RGB", im.size, (255, 255, 255))
                        background.paste(im, mask=im.split()[3]) # 3 is the alpha channel
                        im = background
                        '''
                        im = im.convert("RGB") #在输出的时候会完全打乱
                    print (im.mode)
                    print ("Generating jpeg for %s" % name)
                    im.thumbnail(im.size)
                    print (im.info)
                    #im.save(outfile, "JPEG", quality=100)
                    try_save_image(im, outfile, max_size)
                except Exception as e:
                    print (e)
                    
