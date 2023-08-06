#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Module for testing structure factor"""

import pytest

from cdftpy.cdft1d.rism import rism_1d
from cdftpy.cdft1d.rism_new import rism_1d as rism_1d_new
from cdftpy.cdft1d.solvent import solvent_model_locate, Solvent


def test_rism():

    # load solvent model
    solvent_name = "s2"
    filename = solvent_model_locate(solvent_name)

    solvent = Solvent.from_file(filename, rism_patch=True)

    solute = dict(name="Na", charge=1.0, sigma=2.16, eps=1.4755)
    params = dict(diis_iterations=2, tol=1.0E-7, max_iter=200)

    sim = rism_1d(solute, solvent, params=params)
    fe_ref = -315.64395375311017

    assert sim.fe_tot == pytest.approx(fe_ref, rel=1e-9)

def test_rism_new():

    # load solvent model
    solvent_name = "s2"
    filename = solvent_model_locate(solvent_name)

    solv = Solvent.from_file(filename, rism_patch=True)

    solute = dict(name="Na", charge=1.0, sigma=2.16, eps=1.4755)
    params = dict(diis_iterations=2, tol=1.0E-7, max_iter=200)

    sim = rism_1d_new(solute, solv, params=params)
    fe_ref = -315.65631175156324

    assert sim.fe_tot == pytest.approx(fe_ref, rel=1e-12)