import argparse
import imgaug.augmenters as iaa
import cv2
import os
import json
import numpy as np
from PIL import Image, ImageFont, ImageDraw 
#  from pascal_voc_writer import Writer 
from display import *

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', default = os.path.join('src', 'passport.png'), help='img path')
    parser.add_argument('--num', type=int, default=1, help='num img to gen')
    parser.add_argument('--out', default ='output', help='output folder')
    args = parser.parse_args()
    return args


def gen_image(num, img, out, card):
    aug = iaa.OneOf([
                iaa.GaussianBlur((0, 1.0)),
                iaa.WithBrightnessChannels(iaa.Add((-75, 75))),
                #  iaa.pillike.Autocontrast((10, 20), per_channel=True),
                iaa.MultiplyAndAddToBrightness(mul=(0.5, 1.5), add=(-40, 40)),
                iaa.pillike.EnhanceColor(),
                iaa.pillike.EnhanceBrightness(),
                #  iaa.pillike.FilterBlur(),
                iaa.imgcorruptlike.Fog(severity=2),
                #  iaa.AverageBlur(k=(4, 7)),
                #  iaa.MedianBlur(k=(3, 5)),
                #  iaa.MotionBlur(k=(3, 3)),
                iaa.imgcorruptlike.DefocusBlur(severity=(1,1)),
                #  iaa.AveragePooling(kernel_size = (1,3)),
                #  iaa.MedianPooling(kernel_size = (1,3)),
                #  iaa.JpegCompression(compression=(70, 99)),
                #  iaa.imgcorruptlike.Pixelate(severity=(1,2)),
                #  iaa.AdditiveGaussianNoise(scale=(0, 0.2*255)),
                #  iaa.Cutout(nb_iterations=(2,6), size = 0.1),
                #  iaa.CoarseDropout((0.0, 0.05), size_percent=(0.02, 0.25)),
                #  iaa.imgcorruptlike.Contrast(severity=(2,3)),
                iaa.imgcorruptlike.Brightness(severity=(3,5)),
                #  iaa.imgcorruptlike.Saturate(severity=(2,3)),
                #  iaa.imgcorruptlike.ElasticTransform(severity=(1,2))
                ])
    #  aug = iaa.OneOf([ iaa.GaussianBlur((0, 3.0)),
                #  iaa.WithBrightnessChannels(iaa.Add((-75, 75))),
                #  iaa.pillike.Autocontrast((10, 20), per_channel=True),
                #  iaa.MultiplyAndAddToBrightness(mul=(0.5, 1.5), add=(-40, 40)),
                 #  iaa.pillike.EnhanceColor(),
                 #  iaa.pillike.EnhanceBrightness(),
                 #  iaa.pillike.FilterBlur(),
                 #  iaa.imgcorruptlike.Fog(severity=2),
                #  iaa.AverageBlur(k=(4, 6)),
                #  iaa.MedianBlur(k=(3, 5)),
                #  iaa.MotionBlur(k=(5, 7)),
                #  iaa.imgcorruptlike.DefocusBlur(severity=(1,2)),
                #  #  iaa.AveragePooling(kernel_size = (1,2)),
                #  #  iaa.MedianPooling(kernel_size = (1,2)),
                #  iaa.JpegCompression(compression=(70, 99)),
                #  iaa.imgcorruptlike.Pixelate(severity=(1,3)),
                #  iaa.AdditiveGaussianNoise(scale=(0, 0.15*255)),
                #  #  iaa.Cutout(nb_iterations=(2,6), size = 0.1),
                #  iaa.imgcorruptlike.Contrast(severity=(2,3)),
                #  iaa.imgcorruptlike.Brightness(severity=(3,5)),
                #  iaa.imgcorruptlike.Saturate(severity=(2,3)),
                #  iaa.imgcorruptlike.ElasticTransform(severity=(1,2))
                #  ])
    img = Image.open(img)
    
    with open(os.path.join('name','uit_member.json')) as json_file:
        name_dict = json.load(json_file)

    #  if card 
    font_name = ImageFont.truetype(os.path.join('font','tnr.ttf'), 19)



    for i in range(num):
        label = {}
        name = np.random.choice(name_dict)['full_name']
        idnum = str(np.random.randint(999999999)).zfill(9)
        gender = np.random.choice(['Nam / M', u'Nữ / F'])
        DOB = str(np.random.randint(1,32)).zfill(2) + " / " + str(np.random.randint(1,13)).zfill(2) + " / " + str(np.random.randint(1900, 2021))
        pp_num = 'C' + str(np.random.randint(9999999)).zfill(7)
        src = os.path.join('src', 'tinh_tp.json')


        with open(src) as diachi:
            dist_data = (json.load(diachi))
            dist = dist_data[np.random.choice(list(dist_data))]
            dist = dist['name']

        edit_img = img.copy()
        edit = ImageDraw.Draw(edit_img)

        #  noise = np.random.randint(12)
        noise =0 
            
        label = display(img, edit, label, font_name, name.upper(), noise = noise, x
                = 232, y = 71, fullname = True, key = 'name1', id = 2)
        label = display(img, edit, label, font_name, gender.upper(), noise = noise,
                x = 232, y = 172, fullname = True, key = 'sex', id = 4)
        label = display(img, edit, label, font_name, dist.upper(), noise = noise,
                x = 430, y = 134, fullname = True, key = 'address_line_1', id = 6)
        label = display(img, edit, label, font_name, pp_num.upper(), noise = noise,
                x = 465, y = 34, fullname = True, key = 'passport_id', id = 1)
        label = display(img, edit, label, font_name, idnum.upper(), noise = noise, x =
                430, y = 174, key = 'id', id = 0)
        label = display(img, edit, label, font_name, DOB.upper(), noise = noise, x =
                232, y = 132, key = 'birthday', id = 3)

        if not os.path.exists(os.path.join(out, 'labels')):
            os.makedirs(os.path.join(out,'labels'))

        if not os.path.exists(os.path.join(out, 'json')):
            os.makedirs(os.path.join(out,'json'))

        if not os.path.exists(os.path.join(out, 'img')):
            os.makedirs(os.path.join(out,'img'))

        #  edit_img.show()
        #  with open(os.path.join(out,"json", "{}.json".format(str(i).zfill(5))), "w") as outfile: 
            #  json.dump(label, outfile)

        img_path = os.path.join(out, 'img', '{}.png'.format(str(i).zfill(5)))
        
        #  edit_img = edit_img.convert('RGB')

        edit_img.save('tmp.png')
        edit_img = cv2.imread('tmp.png')
        edit_img = aug(image = edit_img)
        scale = np.random.uniform(0.7, 1)
        #  scale = 2.5
        edit_img = cv2.resize(edit_img, (int(edit_img.shape[1]/scale), int(edit_img.shape[0]/scale)))
        cv2.imwrite(img_path, edit_img)
        #  writer = Writer(img_path, edit_img.size[0], edit_img.size[1])
        f = open(os.path.join(out, 'labels',  '{}.txt'.format(str(i).zfill(5))), "w")
        json_path = os.path.join(out, 'json',  '{}.json'.format(str(i).zfill(5)))
        with open(json_path, 'w') as fp:
            json.dump(label, fp)

        for key in label.keys():
            if 'box' in label[key]:
                idx = label[key]['id']
                box = label[key]['box']
                label[key]['box'] = [str((box[0])/img.size[0]),
                        str(box[1]/img.size[1]), box[2]/img.size[0],
                        box[3]/img.size[1]]
                #  #  writer.addObject(key, box[0], box[1], box[2], box[3])
                center_x = str((box[0] + box[2])/2/img.size[0])
                center_y = str((box[1] + box[3])/2/img.size[1])
                w = str((box[2] - box[0])/img.size[0])
                h = str((box[3] - box[1])/img.size[1])
                yolo_label = ' '.join([str(idx), center_x, center_y, w,h]) + '\n'
                f.write(yolo_label)
        c_x = (425 + 620) / 2 / img.size[0]
        c_y = (92 + 112) / 2 / img.size[1]
        w = (620 - 425) / img.size[0]
        h = (112 - 92) / img.size[1]
        f.write('5 ' + str(c_x) + ' ' + str(c_y) + ' ' + str(w)+ ' ' + str(h))
        f.close()


if __name__ == "__main__":
    arg = parse_args()
    gen_image(arg.num, arg.img,arg.out, None)
