import os 
import glob
import xml.etree.ElementTree as ET

names_dict = {'background':0, 'plate':1}

def parse_xml(path):
    tree = ET.parse(path)
    img_name = path.split('/')[-1][:-4]
    
    height = tree.findtext("./size/height")
    width = tree.findtext("./size/width")

    objects = [img_name, width, height]

    for obj in tree.findall('object'):
        difficult = obj.find('difficult').text
        if difficult == '1':
            continue
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = bbox.find('xmin').text
        ymin = bbox.find('ymin').text
        xmax = bbox.find('xmax').text
        ymax = bbox.find('ymax').text

        name = str(names_dict[name])
        objects.extend([name, xmin, ymin, xmax, ymax])
    if len(objects) > 1:
        return objects
    else:
        return None
    

def gen_txt(txt_path, imgs_path):
    cnt = 0
    img_names = glob.glob(imgs_path)
    f = open(txt_path, 'w')
    for img_name in img_names:
        img_name = '.' + img_name.split('.')[1]
        xml_path = img_name + '.xml'
        objects = parse_xml(xml_path)
        if objects:
            objects[0] = img_name + '.jpg'
            if os.path.exists(objects[0]):
                objects.insert(0, str(cnt))
                cnt += 1
                objects = ' '.join(objects) + '\n'
                f.write(objects)
    f.close()

train_imgs_path = './train/*.jpg'
val_imgs_path = './val/*.jpg'
gen_txt('train.txt', train_imgs_path)
gen_txt('val.txt', val_imgs_path)