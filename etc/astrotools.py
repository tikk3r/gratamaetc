import math

c = 299792458 * 1e2 # cm * s^-1
h = 6.626e-34 * 1e7 # erg * s

class Filter():
    ''' Create a filter for a telescope. The following properties are available:
    - name (str) : name of the filter.
    - lambda_eff (float) : effective  wavelength in angstrom.
    - width (float) : width of the filter.
    - zero_mag_flux (float) : flux producing a magnitude of 0 at the top of the atmosphere in erg * s^-1 * cm^-2 * A^-1 from http://www.stsci.edu/instruments/observatory/PDF/scs8.rev.pdf 
    '''
    def __init__(self, name, leff, eqw, zmf):
        self.name = name
        self.lambda_eff = leff
        self.width = eqw
        self.zero_mag_flux = zmf
        
    @property
    def to_angstrom(self):
        lcm = self.lambda_eff * 1e-8
        return lcm

# List of filters with their properties: effective wavelenght, bandwidth, flux producing m=0 at top of atomosphere.
filters = {'U':Filter('U', 3735, 485, 4.34e-9),
            'B':Filter('B', 4443, 831, 6.40e-9),
            'V':Filter('V', 5483, 827, 3.67e-9),
            'R':Filter('R', 6855, 1742, 1.92e-9),
            'I':Filter('I', 8637, 1970, 9.39e-10)}

def convert_magnitude(mag, zero_flux, Ta, t, A, Tt, qe):
    ''' Convert a magnitude into [erg * A^-1].
    
    Args:
        mag (float) : magnitude of the object.
        zero_flux (float) : flux resulting in magnitude 0 at the top of the atmosphere [erg * s^-1 * cm^-2 * A^-1].
        Ta (float) :  transmission of the atmosphere.
        t (float) : exposure time [s].
        A (float) : geometric area of the main mirror [cm^2].
        Tt (float) : transmission of the telescope.
        qe (float) : quantum efficiency of the detector.
        
    Returns:
        rate (float) : signal rate in [erg * A^-1].
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
    
def signal_to_noise(band, mag_obj, mag_sky, fwhm, scale, t, extended=False, rdn=11):
    ''' Calculate the signal to noise for an observation.
    
    Args:
        band (str) : observing band (U, B, V, R).
        mag_obj (float) : object apparent magnitude.
        mag_sky (float) : sky apparent magnitude [mag * arcsec^-2].
        fwhm (float) : object FWHM [arcsec].
        scale (float) : plate scale of the CCD [arcsec/px].
        t (float) : exposure time [s].
        extended (bool) : whether the object is extended or not. Default is False.
        rdn (float) : readout noise of the CCD [e-]. Default is 11.
        
    Returns:
        sn (float) : the signal to noise ratio.
    '''
    # Filter width and m=0 flux.
    ew, zf = filters[band].width, filters[band].zero_mag_flux
    # Average photon energy in given band.
    E = (h * c) / filters[band].to_angstrom
    Nobj = convert_magnitude(mag=mag_obj, zero_flux=zf, Ta=1., t=t, A=(math.pi * 400), Tt=1., qe=1.) / E
    Nsky = convert_magnitude(mag=mag_sky, zero_flux=zf, Ta=1., t=t, A=(math.pi * 400), Tt=1., qe=1.) / E
    
    print Nobj
    print Nsky

    if not extended:
        # Point source.
        N = Nobj * ew
        S = Nsky * ew * scale**2
        P = math.pi * (fwhm / scale)**2
    else:
        # Extended source.
        N = Nobj * ew * scale**2
        S = Nsky * ew * scale**2
        P = 1
    num = N
    denom = math.sqrt(N + P * (S + rdn**2))
    sn = num / denom
    return sn