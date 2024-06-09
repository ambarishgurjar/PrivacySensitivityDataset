def read_txt_and_tokenize(txt_path: str, bpe, target_dict):
    annotations = []
    with open(txt_path, 'r', encoding='utf8') as fp:
        for line in fp.readlines():
            line = line.rstrip()
            if not line:
                continue
            line_split = line.split(',', maxsplit=8)
            quadrangle = list(map(int, line_split[:8]))
            content = line_split[-1]

            if bpe:
                encoded_str = bpe.encode(content)
            else:
                encoded_str = content

            xs = [quadrangle[i] for i in range(0, 8, 2)]
            ys = [quadrangle[i] for i in range(1, 8, 2)]
            bbox = [min(xs), min(ys), max(xs), max(ys)]
            annotations.append({'bbox': bbox, 'encoded_str': encoded_str, 'category_id': 0, 'segmentation': [quadrangle]})  # 0 for text, 1 for background

    return annotations

def SROIETask2(root_dir: str, bpe, target_dict, crop_img_output_dir=None):
    data = []
    img_id = -1

    crop_data = []
    crop_img_id = -1

    image_paths = natsorted(list(glob.glob(os.path.join(root_dir, '*.jpg'))))
    for jpg_path in tqdm(image_paths):
        im = Image.open(jpg_path).convert('RGB')
        
        img_w, img_h = im.size
        img_id += 1

        txt_path = jpg_path.replace('.jpg', '.txt')
        annotations = read_txt_and_tokenize(txt_path, bpe, target_dict) 
        img_dict = {'file_name': jpg_path, 'width': img_w, 'height': img_h, 'image_id':img_id, 'annotations':annotations}
        data.append(img_dict)

        for ann in annotations:
            crop_w = ann['bbox'][2] - ann['bbox'][0]
            crop_h = ann['bbox'][3] - ann['bbox'][1]

            if not (crop_w > 0 and crop_h > 0):
                logger.warning('Error occurs during image cropping: {} has a zero area bbox.'.format(os.path.basename(jpg_path)))
                continue
            crop_img_id += 1
            crop_im = im.crop(ann['bbox'])
            if crop_img_output_dir:
                crop_im.save(os.path.join(crop_img_output_dir, '{:d}.jpg'.format(crop_img_id)))
            crop_img_dict = {'img':crop_im, 'file_name': jpg_path, 'width': crop_w, 'height': crop_h, 'image_id':crop_img_id, 'encoded_str':ann['encoded_str']}
            crop_data.append(crop_img_dict)

    return data, crop_data