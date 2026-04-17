import statistics
from cmath import inf

from scipy import *

from md_template import loq
from qctype import QCType


# test if string is numeric
def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


# return the blank value at the 99th percentile
def mdl_b_99(lst):
    return statistics.quantiles(lst, n=100)[98]


# return MDLb using students t value
def mdl_b_stud_t(lst):
    df = len(lst) - 1
    t_value = stats.t.ppf(0.99, df)
    std_dev = statistics.stdev(lst)
    return std_dev * t_value


# return the lesser of two MDLb calculations
def mdl_b(array):
    index = 1
    qc_values = []
    for item in array:
        if item[index] and is_number(item[index]):
            qc_values.append(float(item[index]))
    mdl_b_99_value = float(inf)
    if len(qc_values) >= 100:
        mdl_b_99_value = mdl_b_99(qc_values)
    mdl_b_stud_t_value = mdl_b_stud_t(qc_values)
    if mdl_b_99_value < mdl_b_stud_t_value:
        return mdl_b_99_value
    else:
        return mdl_b_stud_t_value


# return MDLs
def mdl_s(array):
    index = 1
    qc_values = []
    for item in array:
        if item[index] and is_number(item[index]):
            qc_values.append(float(item[index]))
    std_dev = statistics.stdev(qc_values)
    df = len(qc_values) - 1
    t_value = stats.t.ppf(0.99, df)
    return std_dev * t_value


# return LCL, UCL for either LFB or LFM QCType
def lfb_lfm_controls(array, qc_type):
    index = 0
    qc_values = []
    if qc_type == QCType.LFB:
        index = 2
    elif qc_type == QCType.LFM:
        index = 1
    else:
        raise ValueError("Invalid QCType: s/b LFB or LFM.")
    for item in array:
        if item[index] and is_number(item[index]):
            qc_values.append(float(item[index]))
    mean = statistics.mean(qc_values)
    st_dev = statistics.stdev(qc_values)
    return mean - (3 * st_dev), mean + (3 * st_dev)


# return DUP RPD limit
def dup_control(array):
    index = 1
    qc_values = []
    for item in array:
        if item[index] and is_number(item[index]) and float(item[index + 1]) >= loq:
            qc_values.append(float(item[index]))
    mean = statistics.mean(qc_values)
    st_dev = statistics.stdev(qc_values)
    return mean + (3 * st_dev)
