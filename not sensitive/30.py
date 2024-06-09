class Receipt53KDataset(FairseqDataset):
    def __init__(self, gt_path, tfm, bpe_parser, target_dict):
        self.gt_path = gt_path
        self.tfm = tfm            
        self.target_dict = target_dict
        self.bpe_parser = bpe_parser
        self.data = Receipt53K(gt_path)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_dict = self.data[idx]
        
        try:
            image = Image.open(img_dict['img_path']).convert('RGB')
        except Exception as e:
            logger.warning('Failed to load image: {}, since {}'.format(img_dict['img_path'], str(e)))
            return None    
        encoded_str = self.bpe_parser.encode(img_dict['text'])
        input_ids = self.target_dict.encode_line(encoded_str, add_if_not_exist=False)

        tfm_img = self.tfm(image)   # h, w, c
        return {'id': idx, 'tfm_img':tfm_img, 'label_ids':input_ids}

    def size(self, idx):
        img_dict = self.data[idx]
        return len(img_dict['text'])
        # item = self[idx]
        # return len(item['label_ids'])

    def num_tokens(self, idx):
        return self.size(idx)

    def collater(self, samples):
        return default_collater(self.target_dict, samples)