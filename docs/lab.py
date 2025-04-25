import json
from pprint import pprint

from rtl2gds import Chip, StepName, flow

# 配置输入信息
design_base = "/home/user/RTL2GDS/design_zoo/spm"
design_result = f"{design_base}/spm_result"

configs = {
    "top_name": "spm",
    "rtl_file": f"{design_base}/spm.v",
    "netlist_file": f"{design_result}/spm_nl.v",
    "result_dir": f"{design_result}",
    "clk_port_name": "clk",
    "clk_freq_mhz": 100,
    "core_util": 0.5,
}

spm = Chip(
    config_dict=configs
)


# # 预览模块结构
# from IPython.display import SVG, display
# from rtl2gds import step

# diagram_file = "csadd.svg"
# step.synthesis.dump_module_preview(
#     verilog_file=spm.path_setting.rtl_file,
#     module_name="CSADD",
#     output_svg=diagram_file
# )

# display(SVG(filename=diagram_file))

# ---------------------------------------------------------------- #
# 1. RTL综合

synth_res_files = flow.single_step.run(spm, expect_step=StepName.SYNTHESIS)

spm.dump_config_yaml()
pprint(synth_res_files)
r2g_print_log = f"{design_result}/r2g_print.log"
with open(r2g_print_log, 'w') as f:
    # write pprint(synth_res_files) result to log file
    f.write("RTL2GDS flow result:\n")
    f.write("============ Synthesis ============\n")
    f.write("Synthesis result files:\n")
    f.write(json.dumps(synth_res_files, indent=4))
    f.write("\n===================================\n")

# # 格式化输出，查看综合结果：
# from rtl2gds.step.synth_util import SynthStatParser

# synth_stat_file = synth_res_files[0]
# parser = SynthStatParser(synth_stat_file)
# parser.print_summary(detail_level=0)

# # 也可直接查看yosys的统计报告：
# from IPython.display import Markdown, display

# with open(synth_stat_file, 'r') as f:
#     contents = f.read()
# display(Markdown(f"```text\n{contents}\n```"))
# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 2: 布图规划
fp_res_files = flow.single_step.run(
    chip=spm,
    expect_step=StepName.FLOORPLAN,
    take_snapshot=True
)

spm.dump_config_yaml()
pprint(fp_res_files)
# append to log file
with open(r2g_print_log, 'a') as f:
    f.write("============ Floorplan ============\n")
    f.write("Floorplan result files:\n")
    f.write(json.dumps(fp_res_files, indent=4))
    f.write("\n-----------------------------------\n")

# 预览布图规划结果
import json

with open(fp_res_files["design_stat_json"], 'r') as f:
    contents = f.read()
    fp_stat_file = json.loads(contents)
pprint(json.dumps(fp_stat_file, indent=4))
with open(r2g_print_log, 'a') as f:
    f.write("Floorplan stat:\n")
    f.write(json.dumps(fp_stat_file, indent=4))
    f.write("\n====================================\n")
# from IPython.display import display
# display(fp_res_files[2])
# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 3: 网表优化
no_res_files = flow.single_step.run(
    chip=spm,
    expect_step=StepName.NETLIST_OPT,
)

spm.dump_config_yaml()
pprint(no_res_files)
with open(r2g_print_log, 'a') as f:
    f.write("============ Netlist opt ============\n")
    f.write("Netlist opt result files:\n")
    f.write(json.dumps(no_res_files, indent=4))
    f.write("\n-----------------------------------\n")

# 预览网表优化结果
with open(no_res_files["design_stat_json"], 'r') as f:
    contents = f.read()
    no_stat_file = json.loads(contents)
pprint(json.dumps(no_stat_file, indent=4))
with open(r2g_print_log, 'a') as f:
    f.write("Netlist opt stat:\n")
    f.write(json.dumps(no_stat_file, indent=4))
    f.write("\n====================================\n")
# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 4、布局
pl_res_files = flow.single_step.run(
    chip=spm,
    expect_step=StepName.PLACEMENT,
    take_snapshot=True
)

spm.dump_config_yaml()
pprint(pl_res_files)
with open(r2g_print_log, 'a') as f:
    f.write("============ Placement ============\n")
    f.write("Placement result files:\n")
    f.write(json.dumps(pl_res_files, indent=4))
    f.write("\n-----------------------------------\n")
# 预览布局结果
with open(pl_res_files["design_stat_json"], 'r') as f:
    contents = f.read()
    pl_stat_file = json.loads(contents)
pprint(json.dumps(pl_stat_file, indent=4))
with open(r2g_print_log, 'a') as f:
    f.write("Placement stat:\n")
    f.write(json.dumps(pl_stat_file, indent=4))
    f.write("\n====================================\n")
# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 5、时钟树综合
cts_res_files = flow.single_step.run(
    chip=spm,
    expect_step=StepName.CTS
)

spm.dump_config_yaml()
pprint(cts_res_files)
with open(r2g_print_log, 'a') as f:
    f.write("============ CTS ============\n")
    f.write("CTS result files:\n")
    f.write(json.dumps(cts_res_files, indent=4))
    f.write("\n-----------------------------------\n")
# 预览时钟树结果
with open(cts_res_files["design_stat_json"], 'r') as f:
    contents = f.read()
    cts_stat_file = json.loads(contents)
pprint(json.dumps(cts_stat_file, indent=4))
with open(r2g_print_log, 'a') as f:
    f.write("CTS stat:\n")
    f.write(json.dumps(cts_stat_file, indent=4))
    f.write("\n====================================\n")
# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 6、时序优化drv
drv_res_files = flow.single_step.run(
    chip=spm,
    expect_step=StepName.DRV_OPT
)

spm.dump_config_yaml()
pprint(drv_res_files)
with open(r2g_print_log, 'a') as f:
    f.write("============ DRV ============\n")
    f.write("DRV result files:\n")
    f.write(json.dumps(drv_res_files, indent=4))
    f.write("\n-----------------------------------\n")
# 预览drv优化结果
with open(drv_res_files["design_stat_json"], 'r') as f:
    contents = f.read()
    drv_stat_file = json.loads(contents)
pprint(json.dumps(drv_stat_file, indent=4))
with open(r2g_print_log, 'a') as f:
    f.write("DRV stat:\n")
    f.write(json.dumps(drv_stat_file, indent=4))
    f.write("\n====================================\n")
# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 7、时序优化hold
hold_res_files = flow.single_step.run(
    chip=spm,
    expect_step=StepName.HOLD_OPT
)

spm.dump_config_yaml()
pprint(hold_res_files)
with open(r2g_print_log, 'a') as f:
    f.write("============ HOLD ============\n")
    f.write("HOLD result files:\n")
    f.write(json.dumps(hold_res_files, indent=4))
    f.write("\n-----------------------------------\n")
# 预览hold优化结果
with open(hold_res_files["design_stat_json"], 'r') as f:
    contents = f.read()
    hold_stat_file = json.loads(contents)
pprint(json.dumps(hold_stat_file, indent=4))
with open(r2g_print_log, 'a') as f:
    f.write("HOLD stat:\n")
    f.write(json.dumps(hold_stat_file, indent=4))
    f.write("\n====================================\n")
# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 7、增量式布局合法化（合法化cts/timing优化时插入的新单元）
hold_res_files = flow.single_step.run(
    chip=spm,
    expect_step=StepName.LEGALIZATION
)

spm.dump_config_yaml()
pprint(hold_res_files)
with open(r2g_print_log, 'a') as f:
    f.write("============ LEGALIZATION ============\n")
    f.write("LEGALIZATION result files:\n")
    f.write(json.dumps(hold_res_files, indent=4))
    f.write("\n-----------------------------------\n")
# 预览布局结果
with open(hold_res_files["design_stat_json"], 'r') as f:
    contents = f.read()
    hold_stat_file = json.loads(contents)
pprint(json.dumps(hold_stat_file, indent=4))
with open(r2g_print_log, 'a') as f:
    f.write("LEGALIZATION stat:\n")
    f.write(json.dumps(hold_stat_file, indent=4))
    f.write("\n====================================\n")
# ----------------------------------------------------

# ---------------------------------------------------------------- #
# 8: 布线
rt_res_files = flow.single_step.run(
    chip=spm,
    expect_step=StepName.ROUTING,
    take_snapshot=True
)

spm.dump_config_yaml()
pprint(rt_res_files)
with open(r2g_print_log, 'a') as f:
    f.write("============ ROUTING ============\n")
    f.write("ROUTING result files:\n")
    f.write(json.dumps(rt_res_files, indent=4))
    f.write("\n-----------------------------------\n")
# 预览布线结果
with open(rt_res_files["design_stat_json"], 'r') as f:
    contents = f.read()
    rt_stat_file = json.loads(contents)
pprint(json.dumps(rt_stat_file, indent=4))
with open(r2g_print_log, 'a') as f:
    f.write("ROUTING stat:\n")
    f.write(json.dumps(rt_stat_file, indent=4))
    f.write("\n====================================\n")
# ----------------------------------------------------

# ---------------------------------------------------------------- #
# 9: 填充单元
fill_res_files = flow.single_step.run(
    chip=spm,
    expect_step=StepName.FILLER,
    take_snapshot=True
)

spm.dump_config_yaml()
pprint(fill_res_files)
with open(r2g_print_log, 'a') as f:
    f.write("============ FILLER ============\n")
    f.write("FILLER result files:\n")
    f.write(json.dumps(fill_res_files, indent=4))
    f.write("\n-----------------------------------\n")
# 预览最终结果
with open(fill_res_files["design_stat_json"], 'r') as f:
    contents = f.read()
    fill_stat_file = json.loads(contents)
pprint(json.dumps(fill_stat_file, indent=4))
with open(r2g_print_log, 'a') as f:
    f.write("ROUTING stat:\n")
    f.write(json.dumps(fill_stat_file, indent=4))
    f.write("\n====================================\n")
# ----------------------------------------------------

# ---------------------------------------------------------------- #
# 10: sta
from rtl2gds.step import sta

_, sta_res_files = sta.run(
    top_name=spm.top_name,
    input_def=spm.path_setting.def_file,
    result_dir=spm.path_setting.result_dir,
    clk_port_name=spm.constrain.clk_port_name,
    clk_freq_mhz=spm.constrain.clk_freq_mhz,
)

pprint(sta_res_files)
with open(r2g_print_log, 'a') as f:
    f.write("============ STA ============\n")
    f.write("STA result files:\n")
    f.write(json.dumps(sta_res_files, indent=4))
    f.write("\n-----------------------------------\n")
# 预览时序结果
with open(f"{sta_res_files['sta_report_dir']}/spm.rpt", 'r') as f:
    contents = f.read()
    sta_report_file = contents
pprint(contents)
with open(r2g_print_log, 'a') as f:
    f.write("Static Timing Analysis:\n")
    f.write(sta_report_file)
    f.write("\n====================================\n")

# ---------------------------------------------------------------- #
# # 11: drc
# from rtl2gds.step import drc

# _, drc_res_files = drc.run(
#     top_name=spm.top_name,
#     gds_file=fill_res_files["gds_file"],
#     result_dir=spm.path_setting.result_dir,
# )

# pprint(drc_res_files)
# with open(r2g_print_log, 'a') as f:
#     f.write("============ DRC ============\n")
#     f.write("DRC result files:\n")
#     f.write(json.dumps(drc_res_files, indent=4))
#     f.write("\n-----------------------------------\n")
# # 预览drc结果
# with open(drc_res_files["drc_report_text"], 'r') as f:
#     contents = f.read()
#     pprint(contents)
# display(Markdown(f"```text\n{contents}\n```"))