from scipy.optimize import curve_fit, optimize

from cdftpy.cdft1d.rdf import analyze_rdf_peaks_sim
from cdftpy.cdft1d.rism_new import rism_1d
from cdftpy.cdft1d.solvent import solvent_model_locate, Solvent
import numpy as np
import panel as pn
from bokeh.resources import INLINE
from scipy.optimize import minimize
from scipy import optimize

import holoviews as hv

from cdftpy.utils.rad_fft import RadFFT

hv.extension('bokeh')
hv.opts.defaults(hv.opts.Curve(show_grid=True, tools=['hover']))
pn.extension()

def rad_integral(r,f):
     return 4.0 * np.pi * np.cumsum(f * r ** 2)

def rad_integral_linear_fit(nf, r, f):

     kbr = rad_integral(r,f)
     rfit = r[-nf:]
     kbrfit = kbr[-nf:]
     coef, covariance = curve_fit(lambda x, a, b: a + b * x, rfit, kbrfit)
     return coef

def compute_norm_factor(nf,r,f):
     _, b = rad_integral_linear_fit(nf, r, f - 1)
     _, b1 = rad_integral_linear_fit(nf, r, f)
     return 1.0-b/b1

def rdf_norm_factor(nf, r, f):

     def objective_function(x):
          _, y = rad_integral_linear_fit(nf, r, (x * f - 1))
          return y

     res = optimize.root_scalar(objective_function, bracket=[0,2], method='brentq')
     return res.root


nf = 200
# filepath = "/Users/marat/codes/cdft/cdft-sfp/cdftsfp/gennady_data/rdf-oo.dat"
filepath = "/Users/marat/codes/cdft/cdft-sfp/cdftsfp/s2_data-large-box/rdf-oo.dat"
r, gr = np.loadtxt(filepath, unpack=True, usecols=(0, 1))

c = rdf_norm_factor(nf, r, gr)
gr_new = gr * c
kbr = rad_integral(r, gr - 1)
kbr2 = rad_integral(r,gr_new-1)
rfit = r
a,b = rad_integral_linear_fit(nf, r, gr_new - 1)

rdf_plot = hv.Scatter((r,kbr),  label="Original KBR", shared_axis=False)*\
     hv.Curve((r,kbr2), label="Modified KBR", shared_axis=False)*\
     hv.Curve((rfit,a+b*rfit), label=F"Linear Fit (slope={b:<.2e})", shared_axis=False)
rdf_plot.opts(xlabel="r", ylabel="KB integral", shared_axes=False, responsive=True)
# rdf_plot.opts(responsive=True,xlabel="r", ylabel="KB integral")

ifft = RadFFT.from_rgrid(r)
kgrid = ifft.kgrid

hk = ifft.to_kspace(gr-1)
hk_new = ifft.to_kspace(gr_new-1)

hk_plot = hv.Curve((kgrid,hk),"k","S(k)", label="Original H(k)", shared_axis=False).redim.range(k=(0,20))*\
     hv.Curve((kgrid, hk_new), label="Modified H(k)", shared_axis=False)
hk_plot.opts(xlabel="k", ylabel="H(k)", shared_axes=False, responsive=True)
# hk_plot.opts(responsive=True,xlabel="k", ylabel="S(k)")
pn.GridBox("# RDF Normalization for Lammps OO rdf",rdf_plot, hk_plot).servable().save("kb-hadi.html")
