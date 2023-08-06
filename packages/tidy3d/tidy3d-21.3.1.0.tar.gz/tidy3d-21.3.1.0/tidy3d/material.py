import numpy as np
import logging

from .utils import listify, log_and_raise
from .utils.misc import eps_input
from .utils.log import Tidy3DError
from .constants import int_, float_, EPSILON_0, C_0
from .dispersion import DispersionModel, Sellmeier


class Medium(object):
    """
    Base class for a custom defined material.
    """

    def __init__(self, name=None, **kwargs):
        """Define a material. Various input artuments are possible which
        define either frequency-independent material parameters, or a
        dispersive, frequency-dependent model.

        Parameters
        ----------
        epsilon : float, array_like or DispersionModel, optional
            If numeric, real part of the dimensionless relative permittivity.
            For anisotropic materials an array of three elements giving the
            main diagonal values of the permittivity tensor can be provided.
            If a :class:`.DispersionModel` is provided, then the model
            data is copied. Default is ``1.`` (vacuum).
        sigma : float or array_like, optional
            (S/micron) Electric conductivity, s.t.
            ``Im(eps(omega)) = sigma/omega``, where ``eps(omega)`` is the
            complex permittivity at frequency omega. For anisotropic materials
            an array of three elements giving the main diagonal values of the 
            conductivity tensor can be provided. This conductivity is
            added on top of any dispersion model, if used.
        n : float, optional
            Real part of refractive index.
        k : float, optional
            Imaginary part of refractive index, where eps = (n + 1i*k)**2.
        wl : float, optional
            (micron) Wavelength corresponding to n and k values.
        freq : float, optional
            (Hz) Frequency corresponding to n and k values.
        dn : float, optional
            (1/micron) Refractive index dispersion; derivative of
            refractive index with respect to wavelength.

        Note
        ----
        Only the following combinations of arguments are supported:

         * ``Medium(epsilon)``
         * ``Medium(epsilon, sigma)``
         * ``Medium(n)``
         * ``Medium(n, k, wl)``
         * ``Medium(n, k, freq)``
         * ``Medium(n, wl, dn)``
         * ``Medium(n, freq, dn)``

        """
        if "epsilon" in kwargs:
            epsilon = kwargs.pop("epsilon")
            sigma = kwargs.pop("sigma", [0., 0., 0.])
            if isinstance(epsilon, DispersionModel):
                self.eps = epsilon._eps_inf
                self.sigma = eps_input(sigma, "sigma")
                self.poles = epsilon._poles
                self.dispmod = epsilon
            else:
                # Make both epsilon and sigma arrays of size 3
                self.eps = eps_input(epsilon, "epsilon")
                self.sigma = eps_input(sigma, "sigma")

                self.dispmod = None
                self.poles = []

            if kwargs:
                log_and_raise(
                    "Invalid keyword arguments specified with epsilon "
                    "and sigma: %r." % tuple(kwargs.keys()),
                    ValueError,
                )

        elif "n" in kwargs:
            n = kwargs.pop("n")
            lam = None
            freq = None
            k = 0
            dn = 0

            if "k" in kwargs:
                k = kwargs.pop("k")
                if "wl" in kwargs:
                    lam = kwargs.pop("wl")
                if "freq" in kwargs:
                    freq = kwargs.pop("freq")
                if lam is None and freq is None:
                    log_and_raise("wl or freq required when specifying k.", ValueError)
                if lam is not None and freq is not None:
                    log_and_raise("Only wl or freq may be specified", ValueError)

            if "dn" in kwargs:
                dn = kwargs.pop("dn")
                if dn > 0:
                    log_and_raise("dn must be smaller than zero.", NotImplementedError)
                if "wl" in kwargs:
                    lam = kwargs.pop("wl")
                if "freq" in kwargs:
                    freq = kwargs.pop("freq")
                if lam is None and freq is None:
                    log_and_raise("wl or freq required when specifying k.", ValueError)
                if lam is not None and freq is not None:
                    log_and_raise("Only wl or freq may be specified.", ValueError)

            if kwargs:
                log_and_raise(
                    "Invalid keyword arguments specified with n: %r." % tuple(kwargs.keys()),
                    ValueError,
                )

            if freq is not None:
                lam = C_0 / freq
            if lam is not None:
                freq = C_0 / lam



            if dn == 0:
                eps_real = n * n - k * k
                eps_imag = 2 * n * k
                sigma = 0
                if k != 0:
                    sigma = 2 * np.pi * freq * eps_imag * EPSILON_0

                self.eps = eps_input(eps_real, 'n, k')
                self.sigma = eps_input(sigma, 'n, k')
                self.dispmod = None
                self.poles = []
            else:
                if k == 0:
                    self.dispmod = Sellmeier.from_dispersion(lam, n, dn)
                    self.poles = self.dispmod._poles
                    self.eps = self.dispmod._eps_inf
                    self.sigma = eps_input(0., 'sigma')
                else:
                    log_and_raise("Currently k cannot be specified with dn.", NotImplementedError)

        elif len(kwargs) > 0:
            log_and_raise("Either epsilon or n must be specified.", ValueError)

        # If set, this is a tuple (f_lower, f_upper) in Hz of the frequency
        # range of validity of this material model.
        self.frequency_range = None

        self._check_stability()

        self.name = None if name is None else str(name)

    def _check_stability(self):
        if np.any((0 < self.eps) * (self.eps < 1)):
            logging.warning(
                "Permittivity smaller than one could result "
                "in numerical instability. Use Courant stability factor "
                "value lower than the smallest refractive index value."
            )

        elif np.any(self.eps) <= 0:
            err_msg = (
                "Permittivity smaller than zero can result in "
                "numerical instability and should be included as a "
                "dispersive model."
            )

            if np.any(self.eps) < -100:
                err_msg += "For large negative values consider using PEC instead."

            log_and_raise(err_msg, Tidy3DError)

    def epsilon(self, freqs=None, component="average"):
        """Evaluate the (complex) relative permittivity of the medium.

        Parameters
        ----------
        freqs : array_like or None, optional
            (Hz) Array of frequencies at which to query the permittivity. If
            ``None``, the instantaneous :math:`\\epsilon_\\infty` is returned.
        component : str, optional
            One of {'average', 'xx', 'yy', 'zz'}, denoting which component of
            the permittivity to be returned.

        Returns
        -------
        array_like
            The permittivity values, same shape as ``freqs``.
        """

        def return_value(eps):
            """Return requested 'component' for the array 'eps' of shape (Nf, 3).
            """
            val_dict = {'xx': 0, 'yy': 1, 'zz': 2}

            if component == "average":
                return np.mean(eps, axis=1)
            elif component in val_dict.keys():
                return eps[:, val_dict[component]]
            else:
                log_and_raise(f"Unrecognized component {component}.", ValueError)

        if self.dispmod is None:
            if freqs is None:
                return return_value(self.eps[None, :])
            else:
                w = 2*np.pi*np.array(freqs)
                w = w.reshape((w.size, 1))
                eps_im = self.sigma[None, :] / w / EPSILON_0
                return return_value(self.eps[None, :] + 1j * eps_im)
        else:
            return return_value(self.dispmod.epsilon(freqs))

    @staticmethod
    def variants():
        return None


class PEC(object):
    """Perfect electric conductor. All tangential electric fields vanish."""

    def __init__(self, name="PEC"):
        """Construct.

        Parameters
        ----------
        name : str, optional
            Custom name of the material.
        """
        self.name = name
        self.dispmod = None
        self.frequency_range = None


class PMC(object):
    """Perfect magnetic conductor. All tangential magnetic fields vanish."""

    def __init__(self, name="PMC"):
        """Construct.

        Parameters
        ----------
        name : str, optional
            Custom name of the material.
        """
        self.name = name
        self.dispmod = None
        self.frequency_range = None
