from functions import dup_control, lfb_lfm_controls, mdl_b, mdl_s
from qctype import QCType


# accepts a csv string and returns a formatted string with calculated control limits
def data_parse(csv, md_template):
    # split into lines
    csv_lines = csv.split("\n")
    # initialize lists to be passed to calc functions
    lrb_lines = []
    lfb_lines = []
    dup_lines = []
    lfm_lines = []
    mdl_lines = []
    # look at each line, determine the valid QC type and add it to the correct list
    for csv_line in csv_lines:
        csv_line = csv_line.split(",")
        if csv_line[0] and csv_line[0] in QCType:
            match csv_line[0]:
                case QCType.LRB:
                    lrb_lines.append(csv_line)
                case QCType.LFB:
                    lfb_lines.append(csv_line)
                case QCType.DUP:
                    dup_lines.append(csv_line)
                case QCType.LFM:
                    lfm_lines.append(csv_line)
                case QCType.MDL:
                    mdl_lines.append(csv_line)
                case _:
                    raise ValueError("Invalid QCType")
    # send lists to calc functions and store values
    mdl_b_value = mdl_b(lrb_lines)
    lfb_lcl, lfb_ucl = lfb_lfm_controls(lfb_lines, QCType.LFB)
    lfm_lcl, lfm_ucl = lfb_lfm_controls(lfm_lines, QCType.LFM)
    dup_rpd = dup_control(dup_lines)
    mdl_s_value = mdl_s(mdl_lines)
    # sub in values to AMrkdown template and return
    md = (
        md_template.replace("{METHOD}", "Total Phos")
        .replace("{LFB_LCL}", lfb_lcl)
        .replace("{LFB_UCL}", lfb_ucl)
        .replace("{DUP_RPD}", dup_rpd)
        .replace("{LFM_LCL}", lfm_lcl)
        .replace("{LFM_UCL}", lfm_lcl)
        .replace("{MDL_B}", mdl_b_value)
        .replace("{MDL_S}", mdl_s_value)
    )
    return md
