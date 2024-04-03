import numpy as np

formats = ['super_pixel', 'bilinear']

def deBayer(img, format='super_pixel'):
    """
    DeBayering of the Bayer pattern image

    Args:
        img : Bayer pattern image
        format : output format of the image
    
    Supported formats:
    - 'super_pixel' - output image has 1/4 of the original resolution
    - 'bilinear' - output image has the same resolution as the input image
    
    img = [
        [G, R, G, R, G, R, ...],
        [B, G, B, G, B, G, ...],
        ...
    ]

    Returns:
        img_out: height, width, channel = frame.shape
    """

    def super_pixel(img):
        G1 = img[0::2, 0::2]
        G2 = img[1::2, 1::2]
        B = img[0::2, 1::2]
        R = img[1::2, 0::2]

        G = G1/2 + G2/2

        img_out = np.zeros((img.shape[0]//2, img.shape[1]//2, 3), dtype=np.uint8)
        img_out[..., 0] = R
        img_out[..., 1] = G
        img_out[..., 2] = B
        return img_out

    print(img.shape)

    if format == 'super_pixel':
        img_out = super_pixel(img)
    elif format == 'bilinear':
        raise NotImplementedError

    return img_out