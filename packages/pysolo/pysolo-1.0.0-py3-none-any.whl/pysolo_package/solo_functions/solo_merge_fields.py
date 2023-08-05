import ctypes

from ..c_wrapper.run_solo import run_solo_function
from ..c_wrapper import DataPair, masked_op
from ..c_wrapper.function_alias import aliases

se_merge_fields = aliases['merge_fields']

def merge_fields(input_list_data_1, input_list_data_2, bad, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Replaces bad values from input_list_data_1 from values in input_list_data2
        
        Args:
            input_list_data_1: The list of floats to be modified,
            input_list_data_2: The list of floats that replaces values from input_list_data_1,
            bad: A float that represents a missing/invalid data point,
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True).

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,

    """

    args = {
        "data1" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data_1),
        "data2" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data_2),
        "newData" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_merge_fields, args)


def merge_fields_masked(masked_array, reference_masked_array, boundary_mask=None):
    """ 
        Replaces bad values from input_list_data_1 from values in input_list_data2
        
        Args:
            masked_array: A numpy masked array that is to be modified.
            reference_masked_array: A numpy masked array with values that replace masked_array on bad entries.

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """
    return masked_op.masked_func(merge_fields, masked_array,  boundary_mask = boundary_mask, second_masked_array=reference_masked_array)
