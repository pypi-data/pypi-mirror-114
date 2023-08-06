import numpy as np
import logging

from ..constants import int_, float_, complex_, fp_eps, ETA_0, C_0
from ..mode import dot_product, Mode
from ..utils.log import log_and_raise, SourceError
from .Source import VolumeSource, ModeSource, PlaneWave, PlaneSource

def _compute_modes_source(self, source, Nmodes, target_neff=None,
        pml_layers=(0, 0)):
    src_data = self._src_data(source)
    if isinstance(source, PlaneSource):
        mplane = src_data.mode_plane
        eps = np.real(mplane._get_eps_cent(self, mplane.freqs[0]))
        src_data._compute_modes_plane_source(eps)
    elif isinstance(source, PlaneWave):
        mplane = src_data.mode_plane
        if mplane.eps_e1 is None:
            mplane._set_yee_sim(self)
        eps = np.stack([e[0].real for e in [mplane.eps_e1, mplane.eps_e2, mplane.eps_en]])
        src_data._compute_modes_plane_wave(eps)
    elif isinstance(source, ModeSource):
        # Set the Yee permittivity if not yet set
        mplane = src_data.mode_plane
        if mplane.eps_e1 is None:
            mplane._set_yee_sim(self)
        # Compute the mode plane modes
        mplane.compute_modes(Nmodes, target_neff, pml_layers)

def _src_data(self, source):
    """Get the source data object from a source, if it is in the simulation.
    """
    try:
        src_data = self._source_ids[id(source)]
        return src_data
    except KeyError:
        log_and_raise("Source has not been added to Simulation!", SourceError)

def spectrum(self, source, freqs):
    """Returns the spectrum of a :class:`.Source`.
    
    Parameters
    ----------
    source : Source
        A source in the simulation.
    freqs : array_like
        (Hz) Array of frequencies to evaluate the spectrum over.
    """
    src_data = self._src_data(source)
    return src_data._get_spectrum(freqs)

def set_mode(self, source, mode_ind, Nmodes=None, target_neff=None):
    """Set the index of the mode to be used by the mode source. To choose 
    which mode to set use :meth:`.compute_modes` and :meth:`.viz_modes`. If
    provided as input, ``Nmodes`` number of modes with effective index closest
    to ``target_neff`` are computed, and the mode with index ``mode_ind`` is
    used. Otherwise, the modes are simply computed in order of decreasing
    effective index.
    
    Parameters
    ----------
    source : ModeSource
        A mode source in the simulation.
    mode_ind : int
        Index of the mode to use.
    Nmodes : None or int, optional
        Number of modes to compute, usually only necessary if ``target_neff``
        is also provided.
    target_neff : None or float, optional
        Look for modes with effective index closest to ``target_neff``.
    """

    src_data = self._src_data(source)
    mplane = src_data.mode_plane

    if isinstance(source, PlaneWave) or isinstance(source, PlaneSource):
        if mode_ind > 0:
            log_and_raise(
                "Plane wave mode index can only be set to 0, "
                "denoting the plane wave with a specified polarization.",
                RuntimeError
            )

    elif isinstance(source, ModeSource):

        src_data.mode_ind = mode_ind
        if Nmodes is None:
            src_data.Nmodes = mode_ind + 1
        else:
            src_data.Nmodes = Nmodes
        src_data.target_neff = target_neff

        logging.info("Mode set, recommend verifying using viz_modes.")

    else:
        log_and_raise(
            "Input 0 must be an instance of a ModeSource.", SourceError
        )