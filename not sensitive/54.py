def profile_model(model_name):
    model = open_clip.create_model(model_name, force_custom_text=True, pretrained_hf=False)
    model.eval()
    if torch.cuda.is_available():
        model = model.cuda()

    if isinstance(model.visual.image_size, (tuple, list)):
        image_input_size = (3,) + tuple(model.visual.image_size[-2:])
    else:
        image_input_size = (3, model.visual.image_size, model.visual.image_size)
    text_input_size = (77,)

    results = {}
    results['model'] = model_name
    results['image_size'] = image_input_size[1]

    model_cfg = open_clip.get_model_config(model_name)
    if model_cfg:
        vision_cfg = open_clip.CLIPVisionCfg(**model_cfg['vision_cfg'])
        text_cfg = open_clip.CLIPTextCfg(**model_cfg['text_cfg'])
        results['image_width'] = int(vision_cfg.width)
        results['text_width'] = int(text_cfg.width)
        results['embed_dim'] = int(model_cfg['embed_dim'])
    else:
        results['image_width'] = 0
        results['text_width'] = 0
        results['embed_dim'] = 0

    retries = 2
    while retries:
        retries -= 1
        try:
            macs, acts = profile_fvcore(
                model, image_input_size=image_input_size, text_input_size=text_input_size, force_cpu=not retries)

            image_macs, image_acts = profile_fvcore_image(
                model.visual, image_input_size=image_input_size, force_cpu=not retries)

            text_macs, text_acts = profile_fvcore_text(
                model.text, text_input_size=text_input_size, force_cpu=not retries)

            results['gmacs'] = round(macs / 1e9, 2)
            results['macts'] = round(acts / 1e6, 2)
            results['mparams'] = round(count_params(model) / 1e6, 2)
            results['image_gmacs'] = round(image_macs / 1e9, 2)
            results['image_macts'] = round(image_acts / 1e6, 2)
            results['image_mparams'] = round(count_params(model.visual) / 1e6, 2)
            results['text_gmacs'] = round(text_macs / 1e9, 2)
            results['text_macts'] = round(text_acts / 1e6, 2)
            results['text_mparams'] = round(count_params(model.text) / 1e6, 2)
        except RuntimeError as e:
            pass
    return results
