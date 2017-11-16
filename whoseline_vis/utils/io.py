
from astropy.io import fits
import numpy as np
from .spectrum import Spectrum

__all__ = ['read_file']

accepted_extensions = ['fits', 'csv', 'txt']

def read_file(path, wavelength_key='wavelength', flux_key='flux'):
    """

    Parameters
    ----------
    path : str
        File path

    Returns
    -------
    ~Spectrum
    """
    ext = path.strip().split('.')[-1]

    if ext.lower() == 'fits':
        fitsrec = fits.getdata(path)

        fitsrecnames = [i.lower() for i in fitsrec.names]

        if wavelength_key not in fitsrecnames or flux_key not in fitsrecnames:
            raise ValueError("Your wavelength or flux header key is not "
                             "available in the FITS file {}.".format(path))

        wavelength=fitsrec[wavelength_key]
        flux=fitsrec[flux_key]

    elif ext.lower() == 'csv':
        data = np.loadtxt(path)
        wavelength, flux = data[:, 0], data[:, 1]
    else:
        raise NotImplementedError("Files with this file type are not currently "
                                  "supported (file: {0})".format(path))

    spectrum = Spectrum(wavelength=wavelength, flux=flux)
    return spectrum
