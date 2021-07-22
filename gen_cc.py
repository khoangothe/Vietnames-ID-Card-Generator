import argparse
from tqdm import tqdm
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
    parser.add_argument('--img', default = os.path.join('src', 'cccd2.png'), help='img path')
    parser.add_argument('--num', type=int, default=1, help='num img to gen')
    parser.add_argument('--out', default ='output', help='output folder')
    args = parser.parse_args()
    return args


def gen_image(num, img, out, card):
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
                iaa.imgcorruptlike.DefocusBlur(severity=(1,1)),
                #  iaa.AveragePooling(kernel_size = (1,3)),
                #  iaa.MedianPooling(kernel_size = (1,3)),
                #  iaa.JpegCompression(compression=(70, 99)),
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

    #  if card 
    font_name = ImageFont.truetype(os.path.join('font','arial_reg.ttf'), 26)
    font = ImageFont.truetype(os.path.join('font','arial_reg.ttf'), 22)
    font_id= ImageFont.truetype(os.path.join('font','arialbd.ttf'), 33)
    font_num= ImageFont.truetype(os.path.join('font','arial.ttf'), 15)



    for i in tqdm(range(num)):
        label = {}
        name = np.random.choice(name_dict)['full_name']
        idnum = str(np.random.randint(99999999999)).zfill(12)
        gender = np.random.choice(['Nam', u'Nữ'])
        DOB = str(np.random.randint(1,32)).zfill(2) + "/" + str(np.random.randint(1,13)).zfill(2) + "/" + str(np.random.randint(1900, 2021))
        pp_num = 'C' + str(np.random.randint(9999999)).zfill(7)

        src = os.path.join(os.path.join('src', 'xa-phuong'),np.random.choice(os.listdir(os.path.join('src', 'xa-phuong'))))
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
        edit.text((115,383), "07/12/2024", (0,0,0), font=font_num)

        noise = np.random.randint(-7,12)
        #  noise =0 
            
        label = display(img, edit, label, font_name,name.upper(), noise = 0, x
                = 215, y = 236, fullname = True, key = 'name1', id = 2, spacing
                = 100)
        #  label = display(img, edit, label, font_name, name.upper(), noise = noise, x
                #  = 217, y = 237, fullname = True, key = 'name1', id = 2)
        label = display(img, edit, label, font, gender, noise = noise,
                x = 350, y = 288, fullname = True, key = 'sex', id = 4)
        label = display(img, edit, label, font, "Việt Nam", noise = noise,
                x = 607, y = 288, fullname = True, key = 'nation', id = 5)
        label = display(img, edit, label, font_id, idnum, noise = noise, x =
                306, y = 175, key = 'id', id = 0)
        label = display(img, edit, label, font, DOB, noise = noise, x =
                420, y = 262, key = 'birthday', id = 3)

        loc1 = loc.split(",")[0]
        loc2 = ", ".join(loc.split(",")[1:]).strip(" ")
        label = display(img, edit, label, font, loc1, noise = noise, x = 509, y
                = 363, key = 'address_line_1', id = 8)
        label = display(img, edit, label, font, loc2, noise = noise, x = 215, y
                = 389, key = 'address_line_2', id = 9)

        if font.getsize(dist)[0] > 500:
            dist1 = dist.split(",")[0]
            dist2 = ", ".join(dist.split(",")[1:]).strip(" ")
            label = display(img, edit, label, font, dist1, noise = noise, x =
                    436, y = 314, key = 'hometown_line_1', id = 6)
            label = display(img, edit, label, font, dist2, noise = noise, x =
                    215, y = 337, key = 'hometown_line_2', id = 7)
        else:
            label = display(img, edit, label, font, dist, noise = noise, x =
                    215, y = 337, key = 'hometown_line_2', id = 7)
            


        if not os.path.exists(os.path.join(out, 'json')):
            os.makedirs(os.path.join(out,'json'))


        if not os.path.exists(os.path.join(out, 'labels')):
            os.makedirs(os.path.join(out,'labels'))

        if not os.path.exists(os.path.join(out, 'img')):
            os.makedirs(os.path.join(out,'img'))

        img_path = os.path.join(out, 'img', '{}.png'.format(str(i).zfill(5)))
        json_path = os.path.join(out, 'json', '{}.json'.format(str(i).zfill(5)))
        
        #  edit_img = edit_img.convert('RGB')

        edit_img.save('tmp.png')
        edit_img = cv2.imread('tmp.png')
        edit_img = aug(image = edit_img)

        scale_size = np.random.uniform(0.7, 1.5)
        edit_img = cv2.resize(edit_img, (int(edit_img.shape[1]/scale_size), int(edit_img.shape[0]/scale_size)))

        scale = np.random.uniform(1, 1.8)
        edit_img = cv2.resize(edit_img, (int(edit_img.shape[1]*scale), int(edit_img.shape[0])))

        #  writer = Writer(img_path, edit_img.size[0], edit_img.size[1])
        f = open(os.path.join(out, 'labels',  '{}.txt'.format(str(i).zfill(5))), "w")

        with open(json_path, 'w') as fp:
            json.dump(label, fp)


        for key in label.keys():
            if 'box' in label[key]:
                idx = label[key]['id']
                box = label[key]['box']
                #  label[key]['box'] = [str((box[0])/img.size[0]),
                        #  str(box[1]/img.size[1]), box[2]/img.size[0], box[3]/img.size[1]]
                #  print(box)
                #  edit_img = cv2.rectangle(edit_img, (int(box[0] / scale_size *
                    #  scale),int(box[1]/ scale_size)), (int(box[2]*scale /
                        #  scale_size), int(box[3]/scale_size)), (0,0,0),5)
                #  print([int(box[0])*scale/edit_img.shape[1],
                    #  box[1]/edit_img.shape[0],
                    #  int(box[2]*scale)/edit_img.shape[1],
                    #  box[3]/edit_img.shape[0]])
                
                #  writer.addObject(key, box[0], box[1], box[2], box[3])
                #  center_x = str((box[0] + box[2])/2/img.size[0])
                center_x = str(scale/ scale_size*(box[0] + box[2])/2/edit_img.shape[1])
                center_y = str((box[1] + box[3])/scale_size/2/edit_img.shape[0])
                #  w = str((box[2] - box[0])/img.size[0])
                w = str((box[2] - box[0])/edit_img.shape[1] * scale/scale_size)
                h = str((box[3] - box[1])/edit_img.shape[0] / scale_size)
                yolo_label = ' '.join([str(idx), center_x, center_y, w,h]) + '\n'
                #  print(yolo_label)
                f.write(yolo_label)
        cv2.imwrite(img_path, edit_img)
        f.close()


if __name__ == "__main__":
    #  face = face.resize((171, 224))
    #  my_image.paste(face, (23,144))
    #  my_image.save('out.png')
    arg = parse_args()
    gen_image(arg.num, arg.img,arg.out, None)
