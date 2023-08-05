import numpy as np
import os.path
import torch
import vapoursynth as vs
from .network_ffdnet import FFDNet as net


def FFDNet(clip: vs.VideoNode, strength: float=5.0, device_type: str='cuda', device_index: int=0) -> vs.VideoNode:
    '''
    FFDNet: Toward a Fast and Flexible Solution for CNN based Image Denoising

    Parameters:
        clip: Clip to process. Only planar format with float sample type of 32 bit depth is supported.
        
        strength: Strength for denoising. Must be greater than 0.
        
        device_type: Device type on which the tensor is allocated. Must be 'cuda' or 'cpu'.
        
        device_index: Device ordinal for the device type.
    '''
    if not isinstance(clip, vs.VideoNode):
        raise vs.Error('FFDNet: This is not a clip')

    if clip.format.id != vs.RGBS:
        raise vs.Error('FFDNet: Only RGBS format is supported')

    if strength <= 0:
        raise vs.Error('FFDNet: strength must be greater than 0')

    device_type = device_type.lower()

    if device_type not in ['cuda', 'cpu']:
        raise vs.Error("FFDNet: device_type must be 'cuda' or 'cpu'")

    if device_type == 'cuda' and not torch.cuda.is_available():
        raise vs.Error('FFDNet: CUDA is not available')

    strength /= 255

    model_path = os.path.join(os.path.dirname(__file__), 'ffdnet_color.pth')

    device = torch.device(device_type, device_index)
    if device_type == 'cuda':
        torch.backends.cudnn.enabled = True
        torch.backends.cudnn.benchmark = True

    model = net(in_nc=3, out_nc=3, nc=96, nb=12, act_mode='R')
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    for _, v in model.named_parameters():
        v.requires_grad = False
    model = model.to(device)

    torch.cuda.empty_cache()

    def denoise(n: int, f: vs.VideoFrame) -> vs.VideoFrame:
        img_L = np.stack([np.asarray(f.get_read_array(plane)) for plane in range(f.format.num_planes)])
        img_L = torch.from_numpy(img_L).unsqueeze(0)
        img_L = img_L.to(device)

        sigma = torch.full((1,1,1,1), strength).type_as(img_L)

        img_E = model(img_L, sigma)
        img_E = img_E.data.squeeze().cpu().numpy()

        fout = f.copy()
        for plane in range(fout.format.num_planes):
            np.copyto(np.asarray(fout.get_write_array(plane)), img_E[plane, ...])
        return fout

    return clip.std.ModifyFrame(clips=clip, selector=denoise)
