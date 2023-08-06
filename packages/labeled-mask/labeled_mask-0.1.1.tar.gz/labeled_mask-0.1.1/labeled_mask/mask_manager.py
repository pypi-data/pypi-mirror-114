import numpy as np
import numpy.ma as ma

class MaskManager():

    def __init__(self, mask_dict={}, fill_value=9999):
        self.fill_value = fill_value
        self.mask_dict = {key: np.array(mask) for key, mask in mask_dict.items()}
        self._validate_mask()

        ## 0: valid, other value: invalid, 
        # example of mask that fot to get only elements in center block: 
        # 
        # [[1,1,1,1],
        #  [1,0,0,1],
        #  [1,0,0,1].
        #  [1,1,1,1]]

    def get_all(self, target):
        return MaskedAll(target, self.mask_dict, self.fill_value)

    def mask(self, target, mask_name):
        masked = ma.array(target, mask=self.mask_dict[mask_name], fill_value=self.fill_value)
        return masked

    def _validate_mask(self):
        shape = self.mask_dict[self.mask_dict.keys()[0]].shape
        for key, mask in self.mask_dict.items():
            assert mask.shape == shape

    def add_mask(self, name, mask):
        self.mask_dict[name] = mask
        self._validate_mask()

class MaskedAll():
    def __init__(self, target, mask_dict, fill_value):
        self.target = target
        self.mask_dict = mask_dict
        self.fill_value = fill_value
        self.masked_arrays = {key: ma.array(target, mask=mask, fill_value=fill_value) for key,mask in mask_dict.items()}

    def __getitem__(self, name):
        return self.masked_arrays[name].filled()