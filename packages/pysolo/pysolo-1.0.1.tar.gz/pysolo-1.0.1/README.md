# lrose-solo-python
Python interface to Solo editing functions

# Install 

```shell
pip install pysolo
```
Tested for Windows 10 and Ubuntu 18.04 and 20.04.

Test it on Colab: https://colab.research.google.com/drive/16tsdAjarCjGDoJIqKFDDODaiUnFoQEFP?usp=sharing
Check out the GitHub: https://github.com/NCAR/lrose-solo-python

# Functions

Name | Function 
------------ | -------------
Despeckle | ```despeckle(input_list_data, bad, a_speckle, dgi_clip_gate=None, boundary_mask=None)``` | [Despeckle.cc] (https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/Despeckle.cc)
Ring Zap | ```ring_zap(input_list_data, bad, from_km, to_km, km_between_gates=1, dgi_clip_gate=None, boundary_mask=None)``` [RemoveRing.cc] (https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/RemoveRing.cc)
Threshold | ``` threshold(input_list_data, threshold_list_data, bad, where, scaled_thr1, scaled_thr2, dgi_clip_gate=None, thr_missing=None, first_good_gate=0, boundary_mask=None) ``` [ThresholdField.cc] (https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/ThresholdField.cc)
