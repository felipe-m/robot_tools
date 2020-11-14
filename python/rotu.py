# ----------------------------------------------------------------------------
# -- ABB IRB 120 Marker holder
# ----------------------------------------------------------------------------
# -- (c) Felipe Machado
# -- Area of Electronic Technology. Rey Juan Carlos University (urjc.es)
# -- https://github.com/felipe-m/abb_markerholder
# -- February-2019
# -- End tool to hold a marker for ABB IRB120 robot.
# -- This holder is attached to the robot flange
# --
# -- Excecute inside the FreeCAD python console using:
# --   exec(open("./rotu.py").read())
# ----------------------------------------------------------------------------
# --- LGPL Licence
# ----------------------------------------------------------------------------


import os
import sys
import inspect
import logging
import math
import FreeCAD
import FreeCADGui
import Part
import DraftVecUtils

# to get the current directory. Freecad has to be executed from the same
# directory this file is
filepath = os.getcwd()
# to get the components
# In FreeCAD can be added: Preferences->General->Macro->Macro path
sys.path.append(filepath) 
#sys.path.append(filepath + '/' + 'comps')
sys.path.append(filepath + '/../../' + 'comps')

# path to save the FreeCAD files
fcad_path = filepath + '/../freecad/'

# path to save the STL files
stl_path = filepath + '/../stl/'

import kcomp   # import material constants and other constants
import fcfun   # import my functions for freecad. FreeCad Functions
import shp_clss # import my TopoShapes classes 
import fc_clss # import my freecad classes 
import comps   # import my CAD components
import partset 

from fcfun import V0, VX, VY, VZ, V0ROT
from fcfun import VXN, VYN, VZN

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)




axis_punta = VZ
axis_punta_n = DraftVecUtils.scale(axis_punta,-1)
axis_brida = VX
axis_lateral = VY
axis_lateral_n = DraftVecUtils.scale(axis_lateral,-1)
brida_r_out = 20.
brida_r_bolt2cen = 31.5/2.
brida_d_bolt = 5+0.5
brida_h = 6.

union_l = []
cut_l = []

# brida
shp_brida = fcfun.shp_cylhole_bolthole (r_out = brida_r_out , r_in = 0,
                     h=brida_h,
                     n_bolt = 4, d_bolt = brida_d_bolt,
                     r_bolt2cen = brida_r_bolt2cen,
                     axis_h = axis_brida, axis_ra = axis_punta, axis_rb = None,
                     bolt_axis_ra = 0,
                     pos_h = 1, pos_ra = 3, pos_rb = 0,
                     xtr_top=0, xtr_bot=0,
                     xtr_r_out=0, xtr_r_in=0,
                     pos = V0)
union_l.append(shp_brida)

shp_base_brida = fcfun.shp_box_dir_xtr(
                       box_w = 2*brida_r_bolt2cen-2,
                       box_d = brida_h, 
                       box_h = brida_r_out - brida_r_bolt2cen +1.8,
                       fc_axis_h = axis_punta, 
                       fc_axis_d = axis_brida, 
                       fc_axis_w = axis_lateral, 
                       cw= 1, cd=0, ch=0, pos=V0)

union_l.append(shp_base_brida)


#r_rotu_in = 11.
#r_rotu_out = 14.
#h_rotu_in = 100.
#rotu_sep = 50.

#shp_cylrotu = fcfun.shp_cylholedir (r_out = r_rotu_out,
#                                        r_in  = r_rotu_in,
#                                        h =  h_rotu_in,
#                                        normal = axis_punta,
#                                        pos = FreeCAD.Vector(rotu_sep,0,0))
#Part.show(shp_cylrotu)

#  
#    top_dent :1
#      ::
#          rotu_top_d : 20
#        :           :
#         _____________................                     A
#       ||_____________|............... top_l : 8           B
#        |             |
#        |             |
#        |             |
#        |             |
#        |             |              body_l : 92
#         |           | 
#         |           | 
#         |           | 
#         |           | 
#         |           | 
#         |           |  cone_bot_d : 18
#         |_         _| ..................                  C-D
#           |       |    lid_up_top_d :15   :                  
#           \       /                     + lid_up_l: 10
#            |     |    lid_up_bot_d : 14   :
#            |     | .....................                 E  
#             \   / ......9.
#              |_|....... 5.5
#               # tip
#              : :
#             end_d 7.5
#
#


tol = 0.5
rotu_spring_l= 15.
rotu_top_d = 20.
rotu_top_l = 8.
rotu_top_dent = 1. # it has a dent
rotu_body_l = 92.  #100. for second version
rotu_cone_bot_d = 18.
rotu_lid_up_top_d = 15.
rotu_lid_up_bot_d = 14.
rotu_end_tip_d = 7.5
rotu_lid_up_l = 10.

rotu_top_r = rotu_top_d/2.
rotu_cone_bot_r = rotu_cone_bot_d/2.

rotu_pos_axis_brida = 35.  #45. for second version


# point at base:
orotu_base_pos = DraftVecUtils.scale(axis_brida, rotu_pos_axis_brida)
# extra tu cut:
rotu_base_pos = orotu_base_pos +  DraftVecUtils.scale(axis_punta,-1)

# B same for inner and outer
# includes the spring and the top
rotu_b_pos = rotu_base_pos + DraftVecUtils.scale(axis_punta,
                                                 rotu_spring_l+rotu_top_l)


# C same for inner and outer
rotu_c_pos = rotu_b_pos + DraftVecUtils.scale(axis_punta, rotu_body_l)

# C same for inner and outer
orotu_e_pos = rotu_c_pos + DraftVecUtils.scale(axis_punta, rotu_lid_up_l +1)
# +1 to cut
rotu_e_pos = rotu_c_pos + DraftVecUtils.scale(axis_punta, rotu_lid_up_l +1+1)

cir_rotu_a = Part.makeCircle (rotu_top_r+1, rotu_base_pos, axis_punta)
w_cir_rotu_a = Part.Wire(cir_rotu_a)

# includes the spring and the top

cir_rotu_b = Part.makeCircle (rotu_top_r+1, rotu_b_pos, axis_punta)
w_cir_rotu_b = Part.Wire(cir_rotu_b)

cir_rotu_c = Part.makeCircle (rotu_cone_bot_r+tol, rotu_c_pos, axis_punta)
w_cir_rotu_c = Part.Wire(cir_rotu_c)

#rotu_d_pos = rotu_d_pos
#cir_rotu_d = Part.makeCircle (rotu_cone_bot_r+tol, rotu_d_pos, axis_punta)
#w_cir_rotu_d = Part.Wire(cir_rotu_d)

# no tolerance to fit
cir_rotu_e = Part.makeCircle (rotu_lid_up_bot_d/2, rotu_e_pos, axis_punta)
w_cir_rotu_e = Part.Wire(cir_rotu_e)

wire_cir_l = [w_cir_rotu_a, w_cir_rotu_b, w_cir_rotu_c, w_cir_rotu_e]

#shp_rotu_in = Part.makeLoft(wire_cir_l,True,False);
shp_rotu_in = Part.makeLoft(wire_cir_l,True,True);
cut_l.append(shp_rotu_in)
                              


# outer part of the rotu
orotu_xtr_r = 3. # extra radius for the outer part of the marker holder


cir_orotu_a = Part.makeCircle (rotu_top_r+1+orotu_xtr_r,
                               orotu_base_pos, axis_punta)
w_cir_orotu_a = Part.Wire(cir_orotu_a)


cir_orotu_b = Part.makeCircle (rotu_top_r+1+orotu_xtr_r, rotu_b_pos, axis_punta)
w_cir_orotu_b = Part.Wire(cir_orotu_b)

cir_orotu_c = Part.makeCircle (rotu_cone_bot_r+orotu_xtr_r,
                               rotu_c_pos, axis_punta)
w_cir_orotu_c = Part.Wire(cir_orotu_c)

# no tolerance to fit
cir_orotu_e = Part.makeCircle (rotu_lid_up_bot_d/2+orotu_xtr_r-0.2,
                               orotu_e_pos, axis_punta)
w_cir_orotu_e = Part.Wire(cir_orotu_e)

wire_ocir_l = [w_cir_orotu_a, w_cir_orotu_b, w_cir_orotu_c, w_cir_orotu_e]
shp_rotu_out = Part.makeLoft(wire_ocir_l,True,True);
union_l.append(shp_rotu_out)


# union from brida to marker:

brida_marker_union_pos =  DraftVecUtils.scale(axis_brida, brida_h)
shp_brida_marker_union = fcfun.shp_box_dir_xtr(
                       box_w = 10.,
                       box_d = rotu_pos_axis_brida - brida_h, 
                       box_h = 30.,
                       xtr_nd = 1,
                       fc_axis_h = axis_punta, 
                       fc_axis_d = axis_brida, 
                       fc_axis_w = axis_lateral, 
                       cw= 1, cd=0, ch=0, pos=brida_marker_union_pos)

union_l.append(shp_brida_marker_union)
#Part.show(shp_brida_marker_union)

# metric of the lock
lock_m = 3
lock_dict = kcomp.D912[lock_m]
rim_r = rotu_top_r+1+orotu_xtr_r + 3*lock_dict['head_r']

r_bolt2cen = rim_r - 1.5*lock_dict['head_r']
rim_h = 4.

shp_rim = fcfun.shp_cylhole_bolthole (r_out = rim_r , r_in = 0,
                     h=rim_h,
                     n_bolt = 2, d_bolt = 2*lock_dict['head_r_tol'],
                     r_bolt2cen = r_bolt2cen,
                     axis_h = axis_punta, axis_ra = axis_lateral,
                     axis_rb = None,
                     bolt_axis_ra = 1,
                     pos_h = 1, pos_ra = 0, pos_rb = 0,
                     xtr_top=0, xtr_bot=0,
                     xtr_r_out=0, xtr_r_in=0,
                     pos = orotu_base_pos)
union_l.append(shp_rim)
#Part.show(shp_rim)

rail_r_out = r_bolt2cen + lock_m/2. + tol/2.
rail_r_in = r_bolt2cen - lock_m/2. - tol/2.

end_angle = 45
end_radangle = end_angle * math.pi/180

shp_rim_rail1 = fcfun.shp_cylhole_arc (r_out = rail_r_out, r_in= rail_r_in,
                     h = rim_h,
                     axis_h = axis_punta, axis_ra = axis_lateral,
                     axis_rb = None,
                     end_angle = end_angle,
                     pos_h = 1, pos_ra = 0, pos_rb = 0,
                     xtr_top=1, xtr_bot=1,
                     xtr_r_out=0, xtr_r_in=0,
                     pos = orotu_base_pos)
#Part.show(shp_rim_rail1)
cut_l.append(shp_rim_rail1)


shp_rim_rail2 = fcfun.shp_cylhole_arc (r_out = rail_r_out, r_in= rail_r_in,
                     h = rim_h,
                     axis_h = axis_punta, axis_ra = axis_lateral_n,
                     axis_rb = None,
                     end_angle = end_angle,
                     pos_h = 1, pos_ra = 0, pos_rb = 0,
                     xtr_top=1, xtr_bot=1,
                     xtr_r_out=0, xtr_r_in=0,
                     pos = orotu_base_pos)
#Part.show(shp_rim_rail2)
cut_l.append(shp_rim_rail2)


rail_d = rail_r_out - rail_r_in
lock_d = (2*lock_dict['head_r'] + (rail_d))/2.

lock_pos_1_dir =  DraftVecUtils.rotate(axis_lateral,
                                                   end_radangle, axis_punta)
lock_pos_1 = orotu_base_pos + DraftVecUtils.scale(lock_pos_1_dir, r_bolt2cen) 

shp_lock_1 = fcfun.shp_cyl_gen (r = lock_d/2., h = rim_h, axis_h = axis_punta,
                                xtr_top =1, xtr_bot =1, pos = lock_pos_1,
                                pos_h =1)

#Part.show(shp_lock_1)
cut_l.append(shp_lock_1)


lock_pos_2_dir =  DraftVecUtils.rotate(axis_lateral_n,
                                                   end_radangle, axis_punta)
lock_pos_2 = orotu_base_pos + DraftVecUtils.scale(lock_pos_2_dir, r_bolt2cen) 

shp_lock_2 = fcfun.shp_cyl_gen (r = lock_d/2., h = rim_h, axis_h = axis_punta,
                                xtr_top =1, xtr_bot =1, pos = lock_pos_2,
                                pos_h =1)

#Part.show(shp_lock_2)
cut_l.append(shp_lock_2)

shp_union = fcfun.fuseshplist(union_l)
shp_cut = fcfun.fuseshplist(cut_l)

shp_rotu_tool = shp_union.cut(shp_cut)
Part.show(shp_rotu_tool)

# TAPA

shp_tapa_cir =  fcfun.shp_cyl_gen (r = rim_r ,
                     h=rim_h,
                     axis_h = axis_punta_n, 
                     pos_h = 1,
                     pos = orotu_base_pos)
#Part.show(shp_tapa_cir)


tapa_bolt_top_h = 2+ lock_dict['head_r'] - (rail_d/2)

tapa_bolt1_circ1_pos = lock_pos_1 + DraftVecUtils.scale(axis_punta, -1)
tapa_bolt1_circ1 = Part.makeCircle (rail_d/2.-tol/2., tapa_bolt1_circ1_pos ,
                                    axis_punta)
w_bolt1_circ1 = Part.Wire(tapa_bolt1_circ1)
tapa_bolt1_circ2_pos = lock_pos_1 + DraftVecUtils.scale(axis_punta, rim_h + 0.5)
tapa_bolt1_circ2 = Part.makeCircle (rail_d/2.-tol/2., tapa_bolt1_circ2_pos,
                                    axis_punta)
w_bolt1_circ2 = Part.Wire(tapa_bolt1_circ2)
tapa_bolt1_circ3_pos =  ( tapa_bolt1_circ2_pos
                       + DraftVecUtils.scale(axis_punta,tapa_bolt_top_h ))
tapa_bolt1_circ3 = Part.makeCircle (lock_dict['head_r'], tapa_bolt1_circ3_pos,
                                    axis_punta)

w_bolt1_circ3 = Part.Wire(tapa_bolt1_circ3)

wire_tapa_bolt1 = [w_bolt1_circ1, w_bolt1_circ2, w_bolt1_circ3]

shp_tapa_bolt1 = Part.makeLoft(wire_tapa_bolt1,True,True)
#Part.show(shp_tapa_bolt1)


tapa_bolt2_circ1_pos = lock_pos_2 + DraftVecUtils.scale(axis_punta, -1)
tapa_bolt2_circ1 = Part.makeCircle (rail_d/2.-tol/2., tapa_bolt2_circ1_pos ,
                                    axis_punta)
w_bolt2_circ1 = Part.Wire(tapa_bolt2_circ1)
tapa_bolt2_circ2_pos = lock_pos_2 + DraftVecUtils.scale(axis_punta, rim_h + 0.5)
tapa_bolt2_circ2 = Part.makeCircle (rail_d/2.-tol/2., tapa_bolt2_circ2_pos,
                                    axis_punta)
w_bolt2_circ2 = Part.Wire(tapa_bolt2_circ2)
tapa_bolt2_circ3_pos =  ( tapa_bolt2_circ2_pos
                       + DraftVecUtils.scale(axis_punta,tapa_bolt_top_h ))
tapa_bolt2_circ3 = Part.makeCircle (lock_dict['head_r'], tapa_bolt2_circ3_pos,
                                    axis_punta)

w_bolt2_circ3 = Part.Wire(tapa_bolt2_circ3)

wire_tapa_bolt2 = [w_bolt2_circ1, w_bolt2_circ2, w_bolt2_circ3]

shp_tapa_bolt2 = Part.makeLoft(wire_tapa_bolt2,True,True)


shp_tapa = shp_tapa_cir.multiFuse([shp_tapa_bolt1, shp_tapa_bolt2])
Part.show(shp_tapa)
