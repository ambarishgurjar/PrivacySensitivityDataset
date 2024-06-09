def setup_task(cls, args, **kwargs):
        import urllib.request
        import io            

        if getattr(args, "dict_path_or_url", None) is not None:
            if args.dict_path_or_url.startswith('http'):
                logger.info('Load dictionary from {}'.format(args.dict_path_or_url))  
                dict_content = urllib.request.urlopen(args.dict_path_or_url).read().decode()
                dict_file_like = io.StringIO(dict_content)
                target_dict = Dictionary.load(dict_file_like)
            else:
                target_dict = Dictionary.load(args.dict_path_or_url)      
        elif getattr(args, "decoder_pretrained", None) is not None:
            if args.decoder_pretrained == 'unilm':            
                url = 'https://layoutlm.blob.core.windows.net/trocr/dictionaries/unilm3.dict.txt'
                logger.info('Load unilm dictionary from {}'.format(url))            
                dict_content = urllib.request.urlopen(url).read().decode()
                dict_file_like = io.StringIO(dict_content)
                target_dict = Dictionary.load(dict_file_like)
            elif args.decoder_pretrained.startswith('roberta'):
                url = 'https://layoutlm.blob.core.windows.net/trocr/dictionaries/gpt2_with_mask.dict.txt'
                logger.info('Load gpt2 dictionary from {}'.format(url))            
                dict_content = urllib.request.urlopen(url).read().decode()
                dict_file_like = io.StringIO(dict_content)
                target_dict = Dictionary.load(dict_file_like)
            else:
                raise ValueError('Unknown decoder_pretrained: {}'.format(args.decoder_pretrained))
        else:
            raise ValueError('Either dict_path_or_url or decoder_pretrained should be set.')
          
        logger.info('[label] load dictionary: {} types'.format(len(target_dict)))

        return cls(args, target_dict)
