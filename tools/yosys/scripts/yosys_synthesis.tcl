# Copyright (c) 2022 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Authors:
# - Philippe Sauter <phsauter@iis.ee.ethz.ch>

# This flows assumes it is beign executed in the yosys/ directory
# but just to be sure, we go there
if {[info script] ne ""} {
    cd "[file dirname [info script]]/../"
}
source global_var.tcl

# process ABC script and write to temporary directory
proc processAbcScript {abc_script} {
    global tmp_dir
    set src_dir [file join [file dirname [info script]] ../src]
    set abc_out_path $tmp_dir/[file tail $abc_script]

    set raw [read -nonewline [open $abc_script r]]
    set abc_script_recaig [string map -nocase [list "{REC_AIG}" [subst "$src_dir/lazy_man_synth_library.aig"]] $raw]
    set abc_out [open $abc_out_path w]
    puts -nonewline $abc_out $abc_script_recaig

    flush $abc_out
    close $abc_out
    return $abc_out_path
}

# ABC logic optimization script
set abc_script [processAbcScript scripts/abc-opt.script]

# read liberty files and prepare some variables
source scripts/init_tech.tcl

foreach file $verilog_files {
    yosys read_verilog $file
}

# -----------------------------------------------------------------------------
# this section heavily borrows from the yosys synth command:
# synth - check
yosys hierarchy -top $top_design
yosys check
yosys proc
yosys tee -q -o "${tmp_dir}/rpt_${top_design}_elaborated.rpt" stat
yosys write_verilog -norename -noexpr -attr2comment ${tmp_dir}/${top_design}_yosys_elaborated.v

# synth - coarse:
# similar to yosys synth -run coarse -noalumacc
yosys opt_expr
yosys opt -noff
yosys fsm
yosys tee -q -o "${tmp_dir}/rpt_${top_design}_initial_opt.rpt" stat
yosys wreduce 
yosys peepopt
yosys opt_clean
yosys opt -full
yosys booth
yosys share
yosys opt
yosys memory -nomap
yosys tee -q -o "${tmp_dir}/rpt_${top_design}_memories.rpt" stat
yosys write_verilog -norename -noexpr -attr2comment ${tmp_dir}/${top_design}_yosys_memories.v
yosys memory_map
yosys opt -fast

yosys opt_dff -sat -nodffe -nosdff
yosys share
yosys opt -full
yosys clean -purge

yosys write_verilog -norename ${tmp_dir}/${top_design}_yosys_abstract.v
yosys tee -q -o "${tmp_dir}/rpt_${top_design}_abstract.rpt" stat -tech cmos

yosys techmap
yosys opt -fast
yosys clean -purge


# -----------------------------------------------------------------------------
yosys tee -q -o "${tmp_dir}/rpt_${top_design}_generic.rpt" stat -tech cmos
yosys tee -q -o "${tmp_dir}/rpt_${top_design}_generic.json" stat -json -tech cmos

# flatten all hierarchy except marked modules
yosys flatten

yosys clean -purge


# -----------------------------------------------------------------------------
# Preserve flip-flop names as far as possible
# split internal nets
yosys splitnets -format __v
# rename DFFs from the driven signal
yosys rename -wire -suffix _reg t:*DFF*
yosys select -write ${tmp_dir}/rpt_${top_design}_registers.rpt t:*DFF*
# rename all other cells
yosys autoname t:*DFF* %n
yosys clean -purge

# print paths to important instances (hierarchy and naming is final here)
# yosys select -write ${tmp_dir}/rpt_${top_design}_registers.rpt t:*DFF*
# yosys tee -q -o ${tmp_dir}/rpt_${top_design}_instances.rpt  select -list "t:RM_IHPSG13_*"
# yosys tee -q -a ${tmp_dir}/rpt_${top_design}_instances.rpt  select -list "t:tc_clk*$*"


# -----------------------------------------------------------------------------
# mapping to technology

# set don't use cells
set dfflibmap_args ""
foreach cell $dont_use_cells {
  lappend dfflibmap_args -dont_use $cell
}
# first map flip-flops
yosys dfflibmap {*}$tech_cells_args {*}$dfflibmap_args

# then perform bit-level optimization and mapping on all combinational clouds in ABC
# pre-process abc file (written to tmp directory)
set abc_comb_script   [processAbcScript scripts/abc-opt.script]
# call ABC
yosys abc {*}$tech_cells_args -D $clk_period_ps -script $abc_comb_script -constr src/abc.constr -showtmp

yosys clean -purge


# -----------------------------------------------------------------------------
# prep for openROAD
# yosys write_verilog -norename -noexpr -attr2comment ${tmp_dir}/${top_design}_yosys_debug.v

yosys splitnets -ports -format __v
yosys setundef -zero
yosys clean -purge
# map constants to tie cells
yosys hilomap -singleton -hicell {*}$tech_cell_tiehi -locell {*}$tech_cell_tielo

# final reports
# yosys tee -q -o "${tmp_dir}/rpt_${top_design}_area.rpt" stat -top $top_design {*}$liberty_args
# yosys tee -q -o "${tmp_dir}/rpt_${top_design}_area_logic.rpt" stat -top $top_design {*}$tech_cells_args
yosys tee -q -o "${synth_stat_json}" stat -json {*}$liberty_args
yosys tee -q -o "${synth_stat_json}.rpt" stat {*}$liberty_args
yosys tee -q -o "${synth_check_txt}" check

# final netlist
yosys write_verilog -noattr -noexpr -nohex -nodec ${final_netlist_file}
