#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

import torch
import torchvision
import torchaudio

from PIL import Image


def load_image_from_disk(absolute_path: str
                         ) -> torch.Tensor:
    try:
        image = torchvision.io.read_image(path=absolute_path,
                                          mode=torchvision.io.image.ImageReadMode.RGB)
    except RuntimeError:
        image = torchvision.transforms.ToTensor()(Image.open(absolute_path))

    if image.shape[0] == 1:
        image = image.repeat(3, 1, 1)

    if image.dtype == torch.float32:
        assert image.max() <= 1. and image.min() >= 0.0, f'{image=} values must be in [0,1)'
        pass

    elif image.dtype == torch.uint8:
        image = image.float() / 255.0

    elif image.dtype == torch.int16:
        image = image.float() / 65535.0

    else:
        raise Exception(f'Unknown image type {image.type()} for {absolute_path=}')

    # at this point, image must be in the shape of [C, W, H]
    # and values must be between [0, 1]
    image -= 0.5
    image /= 0.25
    # Now the value distribution is shifted to approximately N~(mu=0, sigma=1)
    # So we don't need to normalize the image itself

    return image


def load_audio_from_disk(absolute_path: str,
                         default_sample_rate: int = 16000
                         ) -> torch.Tensor:
    try:
        audio, sample_rate = torchaudio.backend.sox_io_backend.load(filepath=absolute_path,
                                                                    normalize=True,
                                                                    channels_first=True)
        audio = audio.mean(axis=0)
    except RuntimeError as runtime_error:
        print(f'problem loading {absolute_path=}')
        raise runtime_error
    if not sample_rate == default_sample_rate:
        # TODO make sure resample gives the best quality
        audio = torchaudio.functional.resample(waveform=audio,
                                               orig_freq=sample_rate,
                                               new_freq=default_sample_rate)

    return audio
