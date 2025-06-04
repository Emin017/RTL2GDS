# SPDX-FileCopyrightText: 2020 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# SPDX-License-Identifier: Apache-2.0

# This script expects 4 arguments: <input_gds_path> <top_module_name> <output_drc_report_path> <output_drc_mag_path>
# And 2 environment variables: <TECH_LEF> <CELL_LEFS>

set top_name [lindex $argv [expr {$argc - 4}]]
set gds_file [lindex $argv [expr {$argc - 3}]]
# set def_file [lindex $argv [expr {$argc - 3}]]
set drc_rpt  [lindex $argv [expr {$argc - 2}]]
set drc_mag  [lindex $argv [expr {$argc - 1}]]

set pdk_tech_lef $::env(TECH_LEF)
set pdk_cell_lefs $::env(CELL_LEFS)

# magic will not return false even if the gds file is not found
if {![file exists $gds_file]} {
    puts stderr "\[ERROR\]: GDS file not found: $gds_file"
    exit 1
} else {
    gds read $gds_file
	puts "\[INFO\]: gds read $gds_file"
}

# if {![file exists $def_file]} {
# 	puts stderr "\[ERROR\]: DEF file not found: $def_file"
#     exit 1
# } else {
#     def read $def_file
# 	puts "\[INFO\]: def read $def_file"
# 	# read_tech_lef
# 	lef read $pdk_tech_lef
# 	puts "\[INFO\]: lef read $pdk_tech_lef"
# 	# read_pdk_lef
# 	foreach lef_file $pdk_cell_lefs {
# 		lef read $lef_file
# 		puts "\[INFO\]: lef read $lef_file"
# 	}
# 	# # read_macro_lef
# 	# if { [info exist ::env(MACRO_LEFS)] } {
# 	#     foreach lef_file $::env(MACRO_LEFS) {
# 	#         lef read $lef_file
# 	#         puts "\[INFO\]: lef read $lef_file"
# 	#     }
# 	# }
# }

set fout [open $drc_rpt w]
set oscale [cif scale out]
set cell_name $top_name
magic::suspendall
puts stdout "\[INFO\]: Loading $cell_name\n"
flush stdout
load $cell_name
select top cell
expand
drc euclidean on
# `drc(full)`: Complete set of DRC rules. Fine for use with small layouts.
# `drc(fast)`: Limited set of DRC rules, good for reasonably quick checking of large layouts.
# `drc(routing)`: DRC rules limited to metal layer rules only. Good for working with large digital standard cell layouts.
drc style drc(fast) 
drc check
set drc_result [drc listall why]

set count 0
puts $fout "$cell_name"
puts $fout "----------------------------------------"
foreach {errtype coordlist} $drc_result {
	puts $fout $errtype
	puts $fout "----------------------------------------"
	foreach coord $coordlist {
	    set bllx [expr {$oscale * [lindex $coord 0]}]
	    set blly [expr {$oscale * [lindex $coord 1]}]
	    set burx [expr {$oscale * [lindex $coord 2]}]
	    set bury [expr {$oscale * [lindex $coord 3]}]
	    set coords [format " %.3f %.3f %.3f %.3f" $bllx $blly $burx $bury]
	    puts $fout "$coords"
	    set count [expr {$count + 1} ]
	}
	puts $fout "----------------------------------------"
}

puts $fout "\[INFO\]: COUNT: $count"
puts $fout "\[INFO\]: Should be divided by 3 or 4"

puts $fout ""
close $fout

puts stdout "\[INFO\]: DRC Checking DONE ($drc_rpt)"
flush stdout

if {$count > 0} {
    puts stderr "\[ERROR\]: $count DRC errors found"
    puts stdout "\[INFO\]: Saving mag view with DRC errors($drc_mag)"
    # WARNING: changes the name of the cell; keep as last step
    save $drc_mag
    puts stdout "\[INFO\]: Saved"
    flush stdout
    exit -1
} else {
    exit 0
}
