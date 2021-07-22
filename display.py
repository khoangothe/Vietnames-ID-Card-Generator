import json
import numpy as np
from PIL import Image, ImageFont, ImageDraw 

def display(img, edit, label, font_name, name,x = 350, y = 205, name_margin = 2,
        noise = 0, fullname = False, key ='', id = 0, spacing = 4):
    name_x = x
    name_y = y

    name_y += noise

    label[key] = {'value': name}
    label[key]['id'] = id
    edit.text((name_x,name_y), name, (0,0,0), font=font_name, spacing = spacing)
    label[key]['box'] = [name_x-name_margin, name_y-name_margin, name_x+name_margin + font_name.getsize(name)[0], name_y+name_margin + font_name.getsize(name)[1]]
    box = label[key]['box']
    #  edit.rectangle([(box[0], box[1]), (box[2], box[3])], outline = (0,0,0))

    return label

def display_name(img, edit, label, font_name, name,name_x = 350, name_y = 205,
        name_x1 =340 , name_y1 = 205, name_x2 = 370, name_y2 = 242, name_margin
        = 2, noise = 0, fullname = False):

    name_y += noise
    name_y1 += noise
    name_y2 += noise
    if len(name) < 20 or fullname:
        label['name1'] = {'value': name}
        label['name2'] = {}
        edit.text((name_x,name_y), name.upper(), (0,0,0), font=font_name)
        label['name1']['box'] = [name_x-name_margin,
                                name_y-name_margin,
                                name_x+name_margin + font_name.getsize(name.upper())[0],
                                name_y+name_margin + font_name.getsize(name.upper())[1]]
        box = label['name1']['box']
        #  edit.rectangle([(box[0], box[1]), (box[2], box[3])], outline = (0,0,0))

    else:
        name1 = " ".join(name.split(" ")[:3])
        name2 = " ".join(name.split(" ")[3:])
        label['name1'] = {'value': name1}
        label['name2'] = {'value': name2}
        edit.text((name_x1,name_y1), name1.upper(), (0,0,0), font=font_name)
        edit.text((name_x2,name_y2), name2.upper(), (0,0,0), font=font_name)
        label['name1']['box'] = [name_x1-name_margin,
                                name_y1-name_margin,
                                name_x1+name_margin + font_name.getsize(name1.upper())[0],
                                name_y1+name_margin + font_name.getsize(name1.upper())[1]]
        label['name2']['box'] = [name_x2-name_margin,
                                    name_y2-name_margin,
                                    name_x2+name_margin + font_name.getsize(name2.upper())[0],
                                    name_y2+name_margin + font_name.getsize(name2.upper())[1]]

        box = label['name1']['box']
        #  edit.rectangle([(box[0], box[1]), (box[2], box[3])], outline = (0,0,0))
        box = label['name2']['box']
        #  edit.rectangle([(box[0], box[1]), (box[2], box[3])], outline = (0,0,0))

    label['name1']['id'] = 2
    label['name2']['id'] = 10

    return label

def display_loc(img, edit, label, font_loc, loc, loc_x1 = 523, loc_y1 = 405,
        loc_x2 = 366, loc_y2 = 445,loc_margin = 0, noise = 0):
    loc_y1 += noise
    loc_y2 += noise
    loc1 = loc.split(",")[0].strip(' ')
    loc2 = ", ".join(loc.split(",")[1:]).strip(" ")
    if loc1 == "":
        loc1 = loc.split(",")[1].strip(' ')
        loc2 = ", ".join(loc.split(",")[2:]).strip(" ")


    loc_x1 += np.random.randint(-50,40)

    if loc_x1 < 486:
        loc_x1 = 486

    if 486 + font_loc.getsize(loc1)[0] > img.size[0]:
        label['address_line_1'] = {}
        label['address_line_2'] = {'value': loc}
        loc_x2 = 87
        loc_x2 += np.random.randint(50,150)

        if loc_x2 + font_loc.getsize(loc)[0] > img.size[0]:
            loc_x2 = img.size[0] - np.random.randint(50,150) - font_loc.getsize(loc)[0]
        if loc_x2  < 0:
            loc_x2 = 30
        label['address_line_2']['box'] = [loc_x2-loc_margin,
                                loc_y2-loc_margin,
                                loc_x2+loc_margin + font_loc.getsize(loc)[0],
                                loc_y2+loc_margin + font_loc.getsize(loc)[1]]
        edit.text((loc_x2,loc_y2), loc, (0,0,0), font= font_loc)
        box = label['address_line_2']['box']
        #  edit.rectangle([(box[0], box[1]), (box[2], box[3])], outline = (0,0,0))
        
    else:
        label['address_line_1'] = {'value': loc1}
        label['address_line_2'] = {'value': loc2}
        if loc_x1 + font_loc.getsize(loc1)[0] > img.size[0]:
            loc_x1 = img.size[0] - np.random.randint(50,150) - font_loc.getsize(loc1)[0]

        if loc_x1 < 486:
            loc_x1 = 486

        loc_x2 -= np.random.randint(0,300)

        if loc_x2 + font_loc.getsize(loc2)[0] > img.size[0]:
            loc_x2 = img.size[0] - np.random.randint(50,150) - font_loc.getsize(loc2)[0]

        #  loc_x2 = img.size[0] - np.random.randint(60, 150) - font_loc.getsize(loc2)[0]
        label['address_line_1']['box'] = [loc_x1-loc_margin,
                                loc_y1-loc_margin,
                                loc_x1+loc_margin + font_loc.getsize(loc1)[0],
                                loc_y1+loc_margin + font_loc.getsize(loc1)[1]]
        label['address_line_2']['box'] = [loc_x2-loc_margin,
                                loc_y2-loc_margin,
                                loc_x2+loc_margin + font_loc.getsize(loc2)[0],
                                loc_y2+loc_margin + font_loc.getsize(loc2)[1]]
        box = label['address_line_1']['box']
        #  edit.rectangle([(box[0], box[1]), (box[2], box[3])], outline = (0,0,0))
        box = label['address_line_2']['box']
        #  edit.rectangle([(box[0], box[1]), (box[2], box[3])], outline = (0,0,0))
        edit.text((loc_x1,loc_y1), loc1, (0,0,0), font= font_loc)
        edit.text((loc_x2,loc_y2), loc2, (0,0,0), font= font_loc)

    label['address_line_1']['id'] = 8
    label['address_line_2']['id'] = 9

    return label


def display_dist(img, edit, label, font_loc, dist, dist_x1 = 437,
        dist_y1 = 327, dist_x2 = 366, dist_y2 = 370, dist_margin= 0, noise = 0):

    dist_y1 += noise
    dist_y2 += noise

    dist1 = dist.split(",")[0]
    dist2 = ", ".join(dist.split(",")[1:]).strip(" ")
    if dist1 == "":
        dist1 = dist.split(",")[1].strip(' ')
        dist2 = ", ".join(dist.split(",")[2:]).strip(" ")
    #  dist_x1 = img.size[0] - 60 - font_loc.getsize(dist1)[0]
    #  dist_x2 = img.size[0] - 60 - font_loc.getsize(dist2)[0]

    dist_x1 += np.random.randint(-30,30)
    dist_x2 -= np.random.randint(-100,100)

    if dist_x1 < 405:
        dist_x1 = 405

    if dist_x2 < 252:
        dist_x2 = 252

    if dist_x1 + font_loc.getsize(dist1)[0] > img.size[0]:
        dist_x1 = img.size[0] - font_loc.getsize(dist1)[0] - 10

    if dist_x2 + font_loc.getsize(dist2)[0] > img.size[0]:
        dist_x2 = img.size[0] - font_loc.getsize(dist2)[0] - 10

    label['hometown_line_1'] = {'value': dist1}
    label['hometown_line_2'] = {'value': dist2}

    label['hometown_line_1']['box'] = [dist_x1-dist_margin,
                            dist_y1-dist_margin,
                            dist_x1+dist_margin + font_loc.getsize(dist1)[0],
                            dist_y1+dist_margin + font_loc.getsize(dist1)[1]]
    label['hometown_line_2']['box'] = [dist_x2-dist_margin,
                            dist_y2-dist_margin,
                            dist_x2+dist_margin + font_loc.getsize(dist2)[0],
                            dist_y2+dist_margin + font_loc.getsize(dist2)[1]]
    box = label['hometown_line_1']['box']
    #  edit.rectangle([(box[0], box[1]), (box[2], box[3])], outline = (0,0,0))
    box = label['hometown_line_2']['box']
    #  edit.rectangle([(box[0], box[1]), (box[2], box[3])], outline = (0,0,0))
    edit.text((dist_x1,dist_y1), dist1, (0,0,0), font= font_loc)
    edit.text((dist_x2,dist_y2), dist2, (0,0,0), font= font_loc)
    label['hometown_line_1']['id'] = 6
    label['hometown_line_2']['id'] = 7

    return label

def display_dob(edit, label, font_name, DOB,
        dob_x = 470, dob_y = 288,dob_margin = 0, noise = 0 ):

    noise_x = np.random.randint(-80,80)

    if noise != 0:
        dob_x += noise_x
        dob_y += noise

    label['birthday'] = {'value': DOB}

    label['birthday']['box'] = [dob_x-dob_margin,
                            dob_y-dob_margin,
                            dob_x+dob_margin + font_name.getsize(DOB)[0],
                            dob_y+dob_margin + font_name.getsize(DOB)[1]]

    box = label['birthday']['box']
    #  edit.rectangle([(box[0], box[1]), (box[2], box[3])], outline = (0,0,0))
    edit.text((dob_x,dob_y), DOB, (0,0,0), font= font_name)
    
    label['birthday']['id'] = 3
    return label

def display_id(edit, label, font_id, idnum, id_x = 413, id_y = 150, id_margin =0, noise = 0, red = False):
    id_x += np.random.randint(-8,3)
    id_y += np.random.randint(-8,8)
    if red:
        edit.text((id_x,id_y), idnum, font= font_id, fill ='#b6528f')
    else:
        edit.text((id_x,id_y), idnum, (0,0,0),  font= font_id)

    label['id'] = {'value': idnum}
    label['id']['box'] = [id_x-id_margin,
                            id_y-id_margin,
                            id_x+id_margin + font_id.getsize(idnum)[0],
                            id_y+id_margin + font_id.getsize(idnum)[1]]
    box = label['id']['box']
    #  edit.rectangle([(box[0], box[1]), (box[2], box[3])], outline = (0,0,0))
    label['id']['id'] = 0
    return label

