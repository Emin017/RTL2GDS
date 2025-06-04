import logging
from pprint import pprint

from rtl2gds import Chip, StepName, flow
from rtl2gds.utils import MDLogger

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s - %(name)s]: %(message)s",
    level=logging.INFO,
)


# 配置输入信息
design_base = "/opt/rtl2gds/demo/spm"
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

spm = Chip(config_dict=configs)


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

logger = MDLogger(f"{design_result}/r2g_log.md")
# ---------------------------------------------------------------- #
# 1. RTL综合

synth_res_files = flow.single_step.run(chip=spm, expect_step=StepName.SYNTHESIS)

spm.dump_config_yaml()
pprint(synth_res_files)
logger.add_header(StepName.SYNTHESIS)
logger.add_result_files(synth_res_files)
logger.add_report_txt(synth_res_files["synth_stat_txt"])

# # 格式化输出，查看综合结果：
# from rtl2gds.step.synth_util import SynthStatParser

# synth_stat_file = synth_res_files["synth_stat_txt"]
# parser = SynthStatParser(synth_stat_file)
# parser.print_summary(detail_level=0)

# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 2: 布图规划
fp_res_files = flow.single_step.run(chip=spm, expect_step=StepName.FLOORPLAN, take_snapshot=True)

spm.dump_config_yaml()
logger.add_pr_res_all(StepName.FLOORPLAN, fp_res_files)

# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 3: 网表优化
no_res_files = flow.single_step.run(
    chip=spm,
    expect_step=StepName.NETLIST_OPT,
)

spm.dump_config_yaml()
logger.add_pr_res_all(StepName.NETLIST_OPT, no_res_files)

# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 4、布局
pl_res_files = flow.single_step.run(chip=spm, expect_step=StepName.PLACEMENT, take_snapshot=True)

spm.dump_config_yaml()
logger.add_pr_res_all(StepName.PLACEMENT, pl_res_files)
# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 5、时钟树综合
cts_res_files = flow.single_step.run(chip=spm, expect_step=StepName.CTS)

spm.dump_config_yaml()
logger.add_pr_res_all(StepName.CTS, cts_res_files)
# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 6、时序优化drv
drv_res_files = flow.single_step.run(chip=spm, expect_step=StepName.DRV_OPT)

spm.dump_config_yaml()
logger.add_pr_res_all(StepName.DRV_OPT, drv_res_files)
# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 7、时序优化hold
hold_res_files = flow.single_step.run(chip=spm, expect_step=StepName.HOLD_OPT)

spm.dump_config_yaml()
logger.add_pr_res_all(StepName.HOLD_OPT, hold_res_files)
# ---------------------------------------------------------------- #

# ---------------------------------------------------------------- #
# 7、增量式布局合法化（合法化cts/timing优化时插入的新单元）
lg_res_files = flow.single_step.run(chip=spm, expect_step=StepName.LEGALIZATION)

spm.dump_config_yaml()
logger.add_pr_res_all(StepName.LEGALIZATION, lg_res_files)
# ----------------------------------------------------

# ---------------------------------------------------------------- #
# 8: 布线
rt_res_files = flow.single_step.run(chip=spm, expect_step=StepName.ROUTING, take_snapshot=True)

spm.dump_config_yaml()
logger.add_pr_res_all(StepName.ROUTING, rt_res_files)
# ----------------------------------------------------

# ---------------------------------------------------------------- #
# 9: 填充单元
fill_res_files = flow.single_step.run(chip=spm, expect_step=StepName.FILLER, take_snapshot=True)

spm.dump_config_yaml()
logger.add_pr_res_all(StepName.FILLER, fill_res_files)
# ----------------------------------------------------

# ---------------------------------------------------------------- #
# 10: sta
from rtl2gds.step import sta

sta_metrics, sta_res_files = sta.run(
    top_name=spm.top_name,
    input_def=spm.path_setting.def_file,
    result_dir=spm.path_setting.result_dir,
    clk_port_name=spm.constrain.clk_port_name,
    clk_freq_mhz=spm.constrain.clk_freq_mhz,
)

logger.add_header(StepName.STA)
logger.add_result_files(sta_res_files)
logger.add_report_txt(f"{sta_res_files['sta_report_dir']}/spm.rpt")
logger.add_metrics_dict(sta_metrics)

# ---------------------------------------------------------------- #
# # 11: drc (IHP130)
# from rtl2gds.step import drc

# drc_metrics, drc_res_files = drc.run(
#     top_name=spm.top_name,
#     gds_file=fill_res_files["gds_file"],
#     result_dir=spm.path_setting.result_dir,
# )

# logger.add_header(StepName.DRC)
# logger.add_result_files(drc_res_files)
# logger.add_metrics_dict(drc_metrics)

# logger.end_log()
