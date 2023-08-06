# -*- coding: utf-8 -*-
# @Time    : 11/18/2021 3:42 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : generator_dynamics.py
# @Software: PyCharm


import py_dss_interface
import math
import cmath
import numpy as np


def deg_to_rad(ang):
    return math.pi / 180 * ang


def rad_to_deg(ang):
    return 180 / math.pi * ang


def complex_polar(mod, ang, ang_mode="deg"):

    if ang_mode == "deg":
        ang = deg_to_rad(ang)

    return mod * math.e ** (complex(0, 1) * ang)


def read_mod_ang_deg(complex_number):
    mod = abs(complex_number)
    ang = rad_to_deg(cmath.phase(complex_number))

    return mod, ang


def read_mod_ang_rad(complex_number):
    mod = abs(complex_number)
    ang = cmath.phase(complex_number)

    return mod, ang


def string_volts(indice, mod, ang):
    return f"V{indice} = {mod} /_ {ang} V"


def string_current(indice, mod, ang):
    return f"I{indice} = {mod} /_ {ang} A"


alfa = complex_polar(1, 120)

operador_seq_pos = np.array([1, alfa ** 2, alfa])
operador_seq_neg = np.array([1, alfa, alfa ** 2])

T = np.matrix([[1, 1, 1],
               [1, alfa ** 2, alfa],
               [1, alfa, alfa ** 2]])


dss = py_dss_interface.DSSDLL()

dss_file = r"C:\Users\ppra005\Box\Documents_PC\Projects\2021\solid_state_trans\OpenDSS\Generator\master_1.dss"
dss.text(f"compile [{dss_file}]")

dss.text("solve")
#
# dss.text("solve mode=dynamics number=1 stepsize=0.0002")
#
# dss.text("edit line.line x1=0.1")
#
# dss.text("Solve number=10")
#
# dss.text("solve mode=dynamics ")
#
# Theta = 13.4692 / 180 * math.pi
#
# dss.circuit_set_active_element("generator.gen")
# variable_names = dss.cktelement_all_variables_names()
#
# variable_values = dss.cktelement_all_variables_values()

dss.circuit_set_active_element("generator.gen")


pu_xdp = float(dss.dssproperties_read_value(str(dss.cktelement_all_property_names().index("Xdp") + 1)))
xdp = pu_xdp * 1000.0 * dss.generators_read_kv() ** 2 / dss.generators_read_kva_rated()

pu_xdpp = float(dss.dssproperties_read_value(str(dss.cktelement_all_property_names().index("Xdpp") + 1)))
xdpp = pu_xdpp * 1000.0 * dss.generators_read_kv() ** 2 / dss.generators_read_kva_rated()


xrdp = float(dss.dssproperties_read_value(str(dss.cktelement_all_property_names().index("XRdp") + 1)))

z_thev = complex(xdp/xrdp, xdp)

y_eq = 1 / z_thev

i_terminal = dss.cktelement_currents()
I_Term = np.matrix([[complex(i_terminal[0], i_terminal[1])],
                    [complex(i_terminal[2], i_terminal[3])],
                    [complex(i_terminal[4], i_terminal[5])]])

# Not sure
I012 = np.linalg.inv(T) * I_Term

Vabc = dss.cktelement_voltages()

VABC = np.matrix([[complex(Vabc[0], Vabc[1])],
                  [complex(Vabc[2], Vabc[3])],
                  [complex(Vabc[4], Vabc[5])]])

V012 = np.linalg.inv(T) * VABC

Edp = V012[1] - z_thev * I012[1]

VThevMag, Theta = read_mod_ang_rad(Edp)

w0 = 2 * math.pi * dss.solution_read_frequency()

H = float(dss.dssproperties_read_value(str(dss.cktelement_all_property_names().index("H") + 1)))
Dpu = float(dss.dssproperties_read_value(str(dss.cktelement_all_property_names().index("D") + 1)))


M = 2 * H * dss.generators_read_kva_rated() * 1000.0 / w0
D = Dpu * dss.generators_read_kva_rated() * 1000.0 / w0

Pshaft = - sum(dss.cktelement_powers()[0:5:2]) * 1000.0


dss.text(f"compile [{dss_file}]")
dss.text("edit generator.gen enabled=no")

dss.text(f"new Vsource.VThev "
         f"bus1=B "
         f"phases=3 "
         f"z1=[{z_thev.real}, {z_thev.imag}] "
         f"z2=[0, {xdpp}] "
         # f"z0=[0, 0] "
         # f"z2=[{z_thev.real}, {z_thev.imag}] "
         # f"z2=[0.0000001, 0.000000001] "
         f"basekv=12.47 "
         f"pu={math.sqrt(3) * float(VThevMag) / 12.47 / 1000.0} "
         f"angle={rad_to_deg(Theta)}")

dss.text("new fault.f1 phases=1 bus1=B.1")

dss.text("solve")


dss.circuit_set_active_element("Vsource.VThev")

trace_power_real = - sum(dss.cktelement_powers()[0:5:2]) * 1000.0
trace_power_imag = - sum(dss.cktelement_powers()[1:6:2]) * 1000.0



print("here")
