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
        match csv_line[0]:
            case QCType.LRB.value:
                lrb_lines.append(csv_line)
            case QCType.LFB.value:
                lfb_lines.append(csv_line)
            case QCType.DUP.value:
                dup_lines.append(csv_line)
            case QCType.LFM.value:
                lfm_lines.append(csv_line)
            case QCType.MDL.value:
                mdl_lines.append(csv_line)
            case _:
                continue
    # send lists to calc functions and store values
    mdl_b_value = mdl_b(lrb_lines)
    lfb_lcl, lfb_ucl = lfb_lfm_controls(lfb_lines, QCType.LFB)
    lfm_lcl, lfm_ucl = lfb_lfm_controls(lfm_lines, QCType.LFM)
    dup_rpd = dup_control(dup_lines)
    mdl_s_value = mdl_s(mdl_lines)
    # sub in values to AMrkdown template and return
    md = (
        md_template.replace("{METHOD}", "Total Phos")
        .replace("{LFB_LCL}", str(round(lfb_lcl, 4)))
        .replace("{LFB_UCL}", str(round(lfb_ucl, 4)))
        .replace("{DUP_RPD}", str(round(dup_rpd, 2)))
        .replace("{LFM_LCL}", str(round(lfm_lcl, 2)))
        .replace("{LFM_UCL}", str(round(lfm_ucl, 2)))
        .replace("{MDL_B}", str(round(mdl_b_value, 4)))
        .replace("{MDL_S}", str(round(mdl_s_value, 4)))
    )
    return md
