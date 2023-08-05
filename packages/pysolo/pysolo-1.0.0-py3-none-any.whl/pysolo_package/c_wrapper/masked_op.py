'''
    This module is a wrapper for run_solo. Allows use of run_solo with 2D masked arrays rather than 1D arrays.
'''

import numpy as np


def masked_func(func, masked_array, *args, boundary_mask=None, second_masked_array=None, usesBadFlags=False):
    """ 
        Performs a solo function on a 2D masked array.
        
        Args:
            masked_array: A numpy masked array data structure with input data (usually this contains info on a single field),
            args: A list of args, listed in order, as required by the solo function
            (optional) boundary_mask: A boolean list designating which region to perform the operation. (Default = all True, so entire region is operated on.)
            (optional) second_masked_array: Some solo functions do operations on two fields. If so, assign this parameter to the masked array of that other field.
            (optional) usesBadFlags: Some solo functions do operations on masks rather than data. If so, set to true.

        Returns:
            Numpy masked array

        Throws:
            AttributeError: if masked_array arg is not a numpy masked array.
    """
    try:
        # decompose masked array to lists
        missing = masked_array.fill_value
        mask = masked_array.mask.tolist()
        data_list = masked_array.tolist(missing)

        # if using a second masked array, obtain the lists for it as well
        second_data_list = None
        if (second_masked_array is not None):
            second_missing = second_masked_array.fill_value
            second_data_list = second_masked_array.tolist(second_missing)

    except AttributeError as e:
        print("Expected a numpy masked array.")
        print(e)
    
    # initialize lists with data/masks. These will become lists of lists
    output_data = []
    output_mask = []

    # if function uses bad flags, add a new parameter for the flag array. Initially set to None.
    argsLength = len(args)
    if (usesBadFlags):
        # in pysolo, the last required arg is for the bad flags.
        argsList = list(args)
        argsList.append(None)
        args = tuple(argsList)

    # iterate through each ray
    for i in range(len(data_list)):
        input_data = data_list[i] # gates
        input_mask = mask[i] # mask for gates
        if second_data_list != None: # if using second masked array, obtain gates for that
            second_input_data = second_data_list[i]
            # in pysolo, second parameter of functions always designates data list for secondary masked list, for functions that have secondary masked arrays.
            func_ma = func(input_data, second_input_data, missing, *args, boundary_mask=boundary_mask)
        else:
            if (usesBadFlags):
                argsList = list(args)
                argsList[argsLength] = input_mask # fill the input_mask for bad flags args.
                args = tuple(argsList)
            func_ma = func(input_data, missing, *args, boundary_mask=boundary_mask)
        output_data.append(np.ma.getdata(func_ma)) # add data to output list of lists
        output_mask.append(np.ma.getdata(func_ma.mask)) # add mask as well

    # convert the list of lists, to a 2D masked array
    output_masked_array = np.ma.masked_array(data=output_data, mask=output_mask, fill_value=missing)
    return output_masked_array