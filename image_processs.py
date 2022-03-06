import io
from PIL import Image, ImageCms
def convert_to_srgb(file_path):
        '''Convert PIL image to sRGB color space (if possible)'''
        img = Image.open(file_path)
        icc = img.info.get('icc_profile', '')
        if icc:
            io_handle = io.BytesIO(icc)     # virtual file
            src_profile = ImageCms.ImageCmsProfile(io_handle)
            dst_profile = ImageCms.createProfile('sRGB')
            img_conv = ImageCms.profileToProfile(img, src_profile, dst_profile)
            icc_conv = img_conv.info.get('icc_profile','')
        if icc != icc_conv:
            # ICC profile was changed -> save converted file
            img_conv.save(file_path,
                        format = 'JPEG',
                        quality = 50,
                        icc_profile = icc_conv)