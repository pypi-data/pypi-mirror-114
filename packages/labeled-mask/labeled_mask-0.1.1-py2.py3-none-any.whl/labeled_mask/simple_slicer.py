from collections import OrderedDict

class SimpleSlicer():
    def __init__(self, len_dict):
        '''
        Requirement `len_dict` as orderd dict
        '''
        self.len_dict = OrderedDict(len_dict)
        self.slice_dict = self.create_slice_dict(self.len_dict)

    def apply_element_state(self, key, length):
        self.len_dict[key] = length
        self.slice_dict = self.create_slice_dict(self.len_dict)

    def get_len(self, key):
        assert key in self.len_dict.keys(), 'Not registered "{}". Valid keys for len_dict are {}.'.format(key, self.len_dict.keys())
        return self.len_dict[key]

    def get_slice(self, key):
        assert key in self.slice_dict.keys(), 'Not registered "{}". Valid keys for slice_dict are {}.'.format(key, self.slice_dict.keys())
        return self.slice_dict[key]

    def get_total_len(self):
        '''
        Returns the total length of state excluding variable length.
        '''
        return sum([x for x in self.len_dict.values() if x > 0])

    @staticmethod
    def create_slice_dict(len_dict):
        assert len([x for x in len_dict.values() if x <= 0]) <= 1
        
        start = 0
        slice_dict = OrderedDict()
        for key in len_dict:
            end = start+len_dict[key] if len_dict[key] > 0 else None
            slice_dict[key] = slice(start, end)
            start += len_dict[key]
            
        return slice_dict

    def get(self, rs_state, key):
        assert key in self.slice_dict.keys()
        return rs_state[self.slice_dict[key]]