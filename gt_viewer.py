import os
import json
import cv2

save_folder = 'gt_viewer_a_ridge'
if not os.path.exists(save_folder):
    os.makedirs(save_folder+'/train')
    os.makedirs(save_folder+'/val')

def show_gts(anno_dir,t_v_folder):


    gt_json = json.load(open(anno_dir))

    images_dict = dict()

    for img in gt_json['images']:
        images_dict[img['id']] = img

    annos_by_image_id = dict()
    for anno in gt_json['annotations']:
        if not annos_by_image_id.has_key(anno['image_id']):
            annos_by_image_id[anno['image_id']]=[]
        annos_by_image_id[anno['image_id']].append(anno)

    for key in annos_by_image_id.keys():
        if not(not ('train' in os.path.basename(images_dict[key]['file_name']) or 'val' in os.path.basename(images_dict[key]['file_name']))):
            image = cv2.imread(t_v_folder+'2014/'+images_dict[key]['file_name'])
            for anno in annos_by_image_id[key]:
                 
                bbox = [int(anno['bbox'][0]),int(anno['bbox'][1]),int(anno['bbox'][2]),int(anno['bbox'][3])]
                if abs(bbox[2]-bbox[3])<10:
                    print(images_dict[key]['file_name'])
                    print(abs(bbox[2]-bbox[3]))
                cv2.rectangle(image,(bbox[0],bbox[1]),(bbox[0]+bbox[2],bbox[1]+bbox[3]),(0,255,0),1)
                cv2.putText(image,str(anno['category_id']),(bbox[0]+bbox[2]/2,bbox[1]+bbox[3]/2),cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,0),1,cv2.LINE_AA)
                polygon = anno['segmentation'][0]
                
                for i in range(len(polygon)/2-1):
                    cv2.line(image,(polygon[i*2],polygon[i*2+1]),(polygon[(i+1)*2],polygon[(i+1)*2+1]),(255,0,0),2)
                    #print(polygon[i*2],polygon[i*2+1])
                #print(polygon)
                cv2.line(image,(polygon[0],polygon[1]),(polygon[len(polygon)-2],polygon[len(polygon)-1]),(255,0,0),2)
            cv2.imwrite(save_folder+'/'+t_v_folder+'/'+os.path.basename(images_dict[key]['file_name']),image)
            #print(images_dict[key]['file_name'])
    

#show_gts('annotations/instances_train2014.json','train')
#show_gts('annotations/instances_val2014.json','val')
show_gts('annotations/ridge_in_one_instances_val2014.json','val')
show_gts('annotations/ridge_in_one_instances_train2014.json','train')

