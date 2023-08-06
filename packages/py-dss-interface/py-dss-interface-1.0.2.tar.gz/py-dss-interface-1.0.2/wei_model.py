# -*- coding: utf-8 -*-
# @Time    : 11/12/2021 1:56 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : wei_model.py
# @Software: PyCharm


import py_dss_interface


dss = py_dss_interface.DSSDLL()

dss_file = r"C:\Users\ppra005\Box\Documents_PC\Help\Wei\Model_forPaulo\Model_forPaulo\master_054102 _Profiles.dss"
dss.text(f"compile [{dss_file}]")

dss.text("? load.0512364401_0.kw")
dss.text("? load.0512364401_0.yearly")

dss.circuit_set_active_element("load.0512364401_0")
dss.cktelement_name()
dss.cktelement_powers()

print("here")
