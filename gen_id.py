import argparse
import cv2
import os
import json
import imgaug.augmenters as iaa
import numpy as np
from PIL import Image, ImageFont, ImageDraw 
#  from pascal_voc_writer import Writer 
from display import *

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', default =os.path.join('src', 'cmt.jpg'), help='img path')
    parser.add_argument('--num', type=int, default=1, help='num img to gen')
    parser.add_argument('--out', default ='dataset', help='output folder')
    parser.add_argument('--mode', default ='train', help='output folder')
    args = parser.parse_args()
    return args


def gen_image(num, img, out, card, mode):
    aug = iaa.OneOf([ iaa.GaussianBlur((0, 3.0)),
                iaa.WithBrightnessChannels(iaa.Add((-75, 75))),
                #  iaa.pillike.Autocontrast((10, 20), per_channel=True),
                iaa.MultiplyAndAddToBrightness(mul=(0.5, 1.5), add=(-40, 40)),
                iaa.pillike.EnhanceColor(),
                iaa.pillike.EnhanceBrightness(),
                iaa.pillike.FilterBlur(),
                iaa.imgcorruptlike.Fog(severity=2),
                #  iaa.AverageBlur(k=(4, 7)),
                #  iaa.MedianBlur(k=(3, 5)),
                iaa.MotionBlur(k=(5, 8)),
                iaa.imgcorruptlike.DefocusBlur(severity=(1,2)),
                #  iaa.AveragePooling(kernel_size = (1,3)),
                #  iaa.MedianPooling(kernel_size = (1,3)),
                iaa.JpegCompression(compression=(70, 99)),
                iaa.imgcorruptlike.Pixelate(severity=(1,3)),
                #  iaa.AdditiveGaussianNoise(scale=(0, 0.2*255)),
                #  iaa.Cutout(nb_iterations=(2,6), size = 0.1),
                #  iaa.CoarseDropout((0.0, 0.05), size_percent=(0.02, 0.25)),
                #  iaa.imgcorruptlike.Contrast(severity=(2,3)),
                iaa.imgcorruptlike.Brightness(severity=(3,5)),
                #  iaa.imgcorruptlike.Saturate(severity=(2,3)),
                #  iaa.imgcorruptlike.ElasticTransform(severity=(1,2))
                ])
    img = Image.open(img)
    
    with open(os.path.join('name','uit_member.json')) as json_file:
        name_dict = json.load(json_file)

    for i in range(num):
        id_type  = np.random.randint(2)
        if id_type:
            font_name = ImageFont.truetype(os.path.join('font','pala.ttf'), 30)
            font_loc = ImageFont.truetype(os.path.join('font','pala.ttf'), 28)
            font_id = ImageFont.truetype(os.path.join('font','pala.ttf'), 35)
        else:
            #  if card 
            font_name = ImageFont.truetype(os.path.join('font','trixi','Trixi Pro Regular.ttf'), 41)
            font_loc = None
            font_id = ImageFont.truetype(os.path.join('font','trixi','Trixi Pro Regular.ttf'), 43)



        label = {}
        name = np.random.choice(name_dict)['full_name']
        idnum = str(np.random.randint(999999999)).zfill(9)
        if not id_type:
            new_pattern = u'\u2009'
            idnum = new_pattern.join(list(idnum))
        gender = np.random.choice(['Nam', u'Nữ'])
        DOB = str(np.random.randint(1,32)).zfill(2) + "-" + str(np.random.randint(1,13)).zfill(2) + "-" + str(np.random.randint(1900, 2021))
        nat = "Việt Nam"
        src = os.path.join(os.path.join('src', 'xa-phuong'),np.random.choice(os.listdir(os.path.join('src', 'xa-phuong'))))
        print(src)

        with open(src) as diachi:
            dist_data = (json.load(diachi))
            dist = dist_data[np.random.choice(list(dist_data))]
            dist = dist['path']

        src = os.path.join(os.path.join('src', 'xa-phuong'),np.random.choice(os.listdir(os.path.join('src', 'xa-phuong'))))
        with open(src) as xaphuong:
            loc_data = (json.load(xaphuong))
            loc = loc_data[np.random.choice(list(loc_data))]
            loc = loc['path']

        edit_img = img.copy()
        edit = ImageDraw.Draw(edit_img)
        if id_type:

            noise = np.random.randint(3,17)
            margin = 2
            label = display_name(img, edit, label, font_name, name, name_margin = 7, noise = noise )
            label = display_id(edit, label, font_id, idnum, noise = noise )
            label = display_dob(edit, label, font_name, DOB, noise = noise )
            label = display_dist(img, edit, label, font_loc, dist, dist_margin = margin, noise = noise)
            label = display_loc(img, edit, label, font_loc, loc,loc_margin = margin, noise = noise)

        else:
            noise = np.random.randint(3,17)
                
            label = display_name(img, edit, label, font_name, name,name_margin = 6, name_x = 360, name_y = 195, name_y1 = 195, name_y2 = 232, noise= noise)
            label = display_id(edit, label, font_id, idnum, noise = noise, red = True)
            label = display_dob(edit, label, font_name, DOB, dob_y = 278, noise = noise )
            label = display_dist(img, edit, label, font_name, dist,dist_x1 = 410,
                    dist_y1 = 317, dist_x2 = 321, dist_y2 = 360, noise = noise)
            label = display_loc(img, edit, label, font_name, loc, loc_x1 = 513,
                    loc_y1 = 395, loc_x2 = 316, loc_y2 = 435, noise = noise)


        if not os.path.exists(os.path.join(out, 'json', mode)):
            os.makedirs(os.path.join(out,'json', mode))

        if not os.path.exists(os.path.join(out, 'images', mode)):
            os.makedirs(os.path.join(out,'images', mode))

        if not os.path.exists(os.path.join(out, 'labels', mode)):
            os.makedirs(os.path.join(out,'labels', mode))



        img_path = os.path.join(out, 'images',mode,  '{}.jpg'.format(str(i).zfill(5)))
        json_path = os.path.join(out, 'json',mode,  '{}.json'.format(str(i).zfill(5)))
        edit_img.save('tmp.jpg')
        edit_img = cv2.imread('tmp.jpg')
        #  face = cv2.imread("src/face.png")
        #  #  face = cv2.resize(face, (178,240))
        #  edit_img[221:461, 71: 249, :] = face
        edit_img = aug(image = edit_img)
        #  scale = np.random.uniform(1, 1.8)
        scale = np.random.uniform(0.7, 3)
        edit_img = cv2.resize(edit_img, (int(edit_img.shape[1]/scale), int(edit_img.shape[0]/scale)))
        #  edit_img = cv2.resize(edit_img, (int(edit_img.shape[1]*scale), int(edit_img.shape[0])))
        cv2.imwrite(img_path, edit_img)

        f = open(os.path.join(out, 'labels', mode, '{}.txt'.format(str(i).zfill(5))), "w")
        with open(json_path, 'w') as fp:
            json.dump(label, fp)

        for key in label.keys():
            if 'box' in label[key]:
                idx = label[key]['id']
                box = label[key]['box']
                #  writer.addObject(key, box[0], box[1], box[2], box[3])
                center_x = str((box[0] + box[2])/2/img.size[0])
                #  center_x = str((box[0] + box[2])/2/img.size[0] * scale)
                center_y = str((box[1] + box[3])/2/img.size[1])
                #  w = str((box[2] - box[0])/img.size[0] * scale)
                w = str((box[2] - box[0])/img.size[0])
                h = str((box[3] - box[1])/img.size[1])
                yolo_label = ' '.join([str(idx), center_x, center_y, w,h]) + '\n'
                f.write(yolo_label)
        f.close()


if __name__ == "__main__":
    arg = parse_args()
    gen_image(arg.num, arg.img,arg.out, None, arg.mode)
