
import numpy as np

def per_size(lis,size):
    init = float(lis[-(size)])
  # print(init)
    end = float(lis[-1])
  # print(end)
    return float((end-init)/init) * 100


def percent_basic(list_,size):
    #log(list_)
    diff = (int(list_[-1]) - int(list_[-size]))
    per_basic = diff/int(list_[-size])
    per_basic = round(per_basic*100,2)
    return per_basic


def mov_average(data:np.array, smaPeriod) -> np.array:
    j = next(i for i, x in enumerate(data) if x is not None)
    our_range = range(len(data))[j + smaPeriod - 1:]
    empty_list = [None] * (j + smaPeriod - 1)
    sub_result = [np.mean(data[i - smaPeriod + 1: i + 1]) for i in our_range]
    
    return np.array(empty_list + sub_result)

