def __init__(self, args, target_dict):

        super().__init__(args)
        self.args = args
        self.data_dir = args.data            
        self.target_dict = target_dict
        if 'LOCAL_RANK' in os.environ and os.environ['LOCAL_RANK'] != '0':
            torch.distributed.barrier()
        self.bpe = self.build_bpe(args)
        if 'LOCAL_RANK' in os.environ and os.environ['LOCAL_RANK'] == '0':
            torch.distributed.barrier()

    def load_dataset(self, split, **kwargs):

        input_size = self.args.input_size         
        if isinstance(input_size, list):
            if len(input_size) == 1:
                input_size = (input_size[0], input_size[0])
            else:
                input_size = tuple(input_size)
        elif isinstance(input_size, int):
            input_size = (input_size, input_size)

        logger.info('The input size is {}, the height is {} and the width is {}'.format(input_size, input_size[0], input_size[1]))

        if self.args.preprocess == 'DA2':            
            tfm = build_data_aug(input_size, mode=split)     
        elif self.args.preprocess == 'RandAugment':
            opt = OptForDataAugment(eval= (split != 'train'), isrand_aug=True, imgW=input_size[1], imgH=input_size[0], intact_prob=0.5, augs_num=3, augs_mag=None)
            tfm = DataAugment(opt)
        else:
            raise Exception('Undeined image preprocess method.')        
        
        # load the dataset
        if self.args.data_type == 'SROIE':
            root_dir = os.path.join(self.data_dir, split)
            self.datasets[split] = SROIETextRecognitionDataset(root_dir, tfm, self.bpe, self.target_dict)        
        elif self.args.data_type == 'Receipt53K':
            gt_path = os.path.join(self.data_dir, 'gt_{}.txt'.format(split))            
            self.datasets[split] = Receipt53KDataset(gt_path, tfm, self.bpe, self.target_dict)
        elif self.args.data_type == 'STR':
            gt_path = os.path.join(self.data_dir, 'gt_{}.txt'.format(split))            
            self.datasets[split] = SyntheticTextRecognitionDataset(gt_path, tfm, self.bpe, self.target_dict)
        else:
            raise Exception('Not defined dataset type: ' + self.args.data_type)