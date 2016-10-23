import math

class Filter():
    ''' Create a filter for a telescope. The following properties are available:
    - name (str) : name of the filter.
    - lambda_eff (float) : effective  wavelength in angstrom.
    - width (float) : width of the filter.
    - zero_mag_Flux (float) : flux producing a magnitude of 0 at the top of the atmosphere in erg * s^-1 * cm^-2 * A^-1.
    '''
    def __init__(self, name, leff, eqw, zmf):
        self.name = name
        self.lambda_eff = leff
        self.width = eqw
        self.zero_mag_flux = zmf

# List of filters with their properties.
filters = {'U':Filter('U', 3735, 485, 4.34e-9),
            'B':Filter('B', 4443, 831, 6.40e-9),
            'V':Filter('V', 5483, 827, 3.67e-9),
            'R':Filter('R', 6855, 1742, 1.92e-9)}

def convert_magnitude(mag, zero_flux, Ta, t, A, Tt, qe):
    ''' Convert a magnitude into [photons * s^-1 * A^-1].
    
    Args:
        mag (float) : magnitude of the object.
        zero_flux (float) : flux resulting in magnitude 0 at the top of the atmosphere.
        Ta (float) :  transmission of the atmosphere.
        t (float) : exposure time [s].
        Tt (float) : transmission of the telescope.
        qe (float) : quantum efficiency of the detector.
        
    Returns:
        rate (float) : signal rate in [photons * s^-1 * A^-1].
    '''
    signal = 10**(-mag / 2.5) * zero_flux * Ta * t * A * Tt * qe
    return signal

def exposure_time():
    ''' Calculate the required exposure time.
    '''
    pass

def limiting_magnitude():
    ''' Calculate the limiting magnitude for an observation.
    '''
    pass
    
def signal_to_noise(band, Nobj, Nsky, rdn, fwhm, scale, extended=False):
    ''' Calculate the signal to noise for an observation.
    
    Args:
        band (str) : observing band (U, B, V, R).
        Nobj (float) : counts from the object in [photons * A^-1 (* arcsec^-2 if extended)].
        Nsky (float) : counts from the sky in [photons * A^-1 * arcsec^-2].
        rdn (float) : readout noise of the CCD.
        fwhm (float) : object FWHM [arcsec].
        scale (float) : plate scale of the CCD [arcsec/px].
        extended (bool) : whether the object is extended or not.
        
    Returns:
        sn (float) : the signal to noise ratio.
    '''
    N = Nobj * ew
    S = Nsky * ew * scale**2
    if not extended:
        # Point source.
        P = math.pi * (fwhm / scale)**2
    else:
        # Extended source.
        P = 1
    num = N
    denom = math.sqrt(N + P * (S + rdn**2)
    sn = num / denom
    return sn