# Copyright (c) 2021 Patricio Cubillos
# Pyrat Bay is open-source software under the GNU GPL-2.0 license (see LICENSE)

import os
from scipy.ndimage.filters import gaussian_filter1d as gaussf
import pathlib
import tempfile

from conftest import make_config

import pyratbay as pb
import pyratbay.constants as pc
import pyratbay.io as io
from pyratbay.constants import ROOT

tmp_path = tempfile.TemporaryDirectory()
tmp_path = pathlib.Path(tmp_path.name)
tmp_path.mkdir()

INPUTS = f'{ROOT}tests/inputs/'
OUTPUTS = f'{ROOT}tests/outputs/'

os.chdir(tmp_path)
# Expected spectra:
keys = [
    'lec', 'cia', 'alkali', 'deck', 'tli', 'patchy', 'patchy_clear',
    'patchy_cloudy', 'all', 'etable',
    'tmodel', 'vert', 'scale', 'fit1', 'fit2', 'fit3', 'fit4',
    'bandflux4', 'resolution', 'odd_even']
expected = {
    key:np.load(f"{ROOT}tests/expected/"
                f"expected_spectrum_transmission_{key}_test.npz")['arr_0']
    for key in keys}


key = 'fit4'

# Run test from tests/test_transmission.py, e.g.:
"""
cfg = make_config(tmp_path,
    ROOT+'tests/configs/spectrum_transmission_test.cfg',
    remove=['tlifile', 'csfile', 'rayleigh', 'clouds'],
    reset={'wllow':'0.45 um', 'wlhigh':'1.0 um'})
pyrat = pb.run(cfg)
np.testing.assert_allclose(
    pyrat.spec.spectrum, expected['alkali'], rtol=rtol)
"""

plt.figure(1)
plt.clf()
plt.plot(1e4/pyrat.spec.wn, pyrat.spec.spectrum, c='b')
#plt.plot(1e4/pyrat.spec.wn, expected[key], c='orange', alpha=0.6)
plt.tight_layout()

plt.figure(2)
plt.clf()
plt.plot(1e4/pyrat.spec.wn, 100*(1-pyrat.spec.spectrum/expected[key]))
plt.ylabel('Diff (%)')
plt.tight_layout()


np.savez(
    f'{ROOT}tests/expected/expected_spectrum_transmission_{key}_test.npz',
    pyrat.spec.spectrum)

np.savez(f'{ROOT}tests/expected/expected_spectrum_transmission_bandflux4_test.npz', model4[1])


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Emission

keys = [
    'lec', 'cia', 'alkali', 'deck', 'tli', 'all',
    'resolution', 'etable',
    'odd_even',
    'tmodel',
    #'vert', 'scale', 'fit1', 'fit2', 'fit3', 'fit4',
    #'bandflux4',
    ]
expected = {
    key:np.load(f"{ROOT}tests/expected/"
                f"expected_spectrum_emission_{key}_test.npz")['arr_0']
    for key in keys}


key = 'two_stream'

spectrum = ps.bbflux(pyrat.spec.wn, pyrat.atm.temp[-2])

plt.figure(1)
plt.clf()
plt.plot(1e4/pyrat.spec.wn, pyrat.spec.spectrum, c='b')
plt.plot(1e4/pyrat.spec.wn, expected[key], c='orange', alpha=0.6)
plt.plot(1e4/pyrat.spec.wn, spectrum, c='r', alpha=0.75)
plt.tight_layout()

plt.figure(2)
plt.clf()
plt.plot(1e4/pyrat.spec.wn, 100*(1-pyrat.spec.spectrum/expected[key]))
plt.ylabel('Diff (%)')
plt.tight_layout()

np.savez(
    f'{ROOT}tests/expected/expected_spectrum_emission_{key}_test.npz',
    pyrat.spec.spectrum)


