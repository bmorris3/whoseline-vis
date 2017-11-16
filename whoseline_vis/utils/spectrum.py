
__all__ = ['Spectrum']


class Spectrum(object):
    """
    Container for a 1D spectrum.
    """
    def __init__(self, wavelength, flux, meta=None):
        self.wavelength = wavelength
        self.flux = flux
        self.meta = meta
