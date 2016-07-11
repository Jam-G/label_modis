from os import path
from pyhdf.SD import SD, SDC
from PIL import Image
import numpy as np
import os

'''
tmp_dir = "tmp"
if not path.exists(tmp_dir):
    os.mkdir(tmp_dir)
'''
def read_band(file_path):
    DATAFIELD_NAME = 'EV_250_RefSB'

    hdf = SD(file_path, SDC.READ)

    file_name = path.splitext(path.basename(file_path))[0]
    band1_path = path.join(tmp_dir, file_name + "_band1.jpg")
    band2_path = path.join(tmp_dir, file_name + "_band2.jpg")

    if path.exists(band1_path) and path.exists(band2_path):
        pass
    else:
        # Read dataset.
        data = hdf.select(DATAFIELD_NAME)
        data2d = data.get().astype("double")

        # Retrieve attributes.
        attrs = data.attributes(full=1)
        aoa = attrs["radiance_offsets"]
        add_offset = aoa[0]
        fva = attrs["_FillValue"]
        _FillValue = fva[0]
        sfa = attrs["radiance_scales"]
        scale_factor = sfa[0]
        vra = attrs["valid_range"]
        valid_min = vra[0][0]
        valid_max = vra[0][1]

        invalid = np.logical_or(data2d > valid_max,
                                data2d < valid_min)
        invalid = np.logical_or(invalid, data2d == _FillValue)
        data2d[invalid] = np.nan

        data2d[0] = (data2d[0] - add_offset[0]) * scale_factor[0]
        data2d[1] = (data2d[1] - add_offset[1]) * scale_factor[1]
        data2d = np.ma.masked_array(data2d, np.isnan(data2d))

        band1_img = Image.fromarray(data2d[0].astype("uint8"))
        band2_img = Image.fromarray(data2d[1].astype("uint8"))

        band1_img.save(band1_path)
        band2_img.save(band2_path)

    return band1_path, band2_path

if __name__ == "__main__":
    from PIL import Image
    file_path = "../1_5/MOD02QKM.A2014047.1510.006.2014218131929.hdf"

    b1_path, b2_path = read_band(file_path)
    band1 = Image.open(b1_path)
    band1.show()
    band2 = Image.open(b2_path)
    band2.show()
