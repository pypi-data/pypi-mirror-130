#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Module for testing structure factor"""

import pytest

from cdftpy.cdft1d.rsdft import rsdft_1d

from cdftpy.cdft1d.solvent import Solvent, solvent_model_locate


def test_rsdft_cation():

    # load solvent model
    solvent_name = "s2"

    filename = solvent_model_locate(solvent_name)

    solvent = Solvent.from_file(filename)

    solute = dict(name="Na", charge=1.0, sigma=2.16, eps=1.4755)

    params = dict(diis_iterations=2, tol=1.0E-7, max_iter=200)

    rsdft = rsdft_1d(solute, solvent, params=params)

    fe = rsdft.fe_tot
    fe_ref = -318.3690861027192

    assert fe == pytest.approx(fe_ref, rel=1e-4)


def test_rsdft_anion():

    # load solvent model
    solvent_name = "s2"

    filename = solvent_model_locate(solvent_name)

    solv = Solvent.from_file(filename)

    solute = dict(name="Cl", charge=-1.0, sigma=4.83, eps=0.05349244)

    params = dict(diis_iterations=2, tol=1.0E-7, max_iter=200)

    rsdft = rsdft_1d(solute, solv, params=params)

    fe = rsdft.fe_tot

    fe_ref = -296.3113532110815

    assert fe == pytest.approx(fe_ref, abs=1e-3)
