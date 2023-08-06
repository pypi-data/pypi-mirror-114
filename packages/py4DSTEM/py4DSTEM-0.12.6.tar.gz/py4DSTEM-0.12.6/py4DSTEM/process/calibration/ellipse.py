"""
Methods related to elliptical calibration, coordinates, and transformations.

Typically use of this module will follow a workflow like:
(1) fit an ellipse
(2) define an elliptical coordinate system
(3) perform some analysis using these coordinates

Methods for (1) include fit_ellipse_1d() and fit_ellipse_amorphous_ring().
The former fits a 1D elliptical curve to a 2d arry of data e.g. a
ring of peaks in a Bragg vector map.  The latter function fits a 2d
pattern of ring of amorphous scattering, using a double-sided gaussian
function intended.

(2) is accomlished by feeding the output elliptical parameters of (1)
into a Coordinates instance.

(3) will depend on the dataset.  2d data can be transformed from
carterian (x,y) space to polar-ellitical (r,phi) space.  Detected Bragg
disk positions can be transformed from their elliptically-distorted
cooridinates into a circularly symmetric coordinate system.

The user-facing description of ellipses is in terms of the following 5
parameters:

    x0,y0       the center of the ellipse
    a           the semimajor axis length
    e           the ratio of lengths of the semiminor to semimajor
                axes
    theta       the (positive, right handed) tilt of the a-axis
                to the x-axis, in radians

Internally, fits are performed using the canonical ellipse parameterization,
in terms of the parameters (x0,y0,A,B,C):

    A(x-x0)^2 + B(x-x0)(y-y0) C(y-y0)^2 = 1

It is possible to convert between (a,b,theta) <--> (A,B,C) using
the convert_ellipse_params() methods.

Transformation from cartesian to polar-elliptical space is done using

       x = x0 + a*r*cos(theta)*cos(phi) + b*r*sin(theta)*sin(phi)
       y = y0 + b*r*sin(theta)*sin(phi) - a*r*cos(theta)*cos(phi)

where b = a*e is the semiminor axis length.
"""

import numpy as np
from scipy.optimize import leastsq, least_squares
from scipy.ndimage.filters import gaussian_filter
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
from ..utils import get_CoM
from ...io import PointListArray

###### Fitting a 1d elliptical curve to a 2d array, e.g. a Bragg vector map ######

def fit_ellipse_1d(ar,x0,y0,ri,ro,mask=None,returnABC=False):
    """
    For a 2d array ar, fits a 1d elliptical curve to the data inside an annulus centered
    at (x0,y0) with inner and outer radii ri and ro.  The data to fit make optionally
    be additionally masked with the boolean array mask. See module docstring for more info.

    Args:
        ar (ndarray): array containing the data to fit
        x0,y0 (floats): the center of the annular fitting region
        ri (float): inner radius of the fit region
        ro (float): outer radius of the fit region
        mask (ar-shaped ndarray of bools): ignore data wherever mask==True
        returnABC (bool): if True, returns ellipse params in canonical form

    Returns:
        (5-tuple of floats): A 5-tuple containing the ellipse parameters. The form of
        the returned parameters depends on the input value `returnABC`.

        If ``returnABC==False`` (default), returns:

            * **x0**: the center x-position
            * **y0**: the center y-position
            * **a**: the semimajor axis length
            * **e**: the ratio of lengths of the semiminor to the semimajor axes
            * **theta**: the tilt of the ellipse semimajor axis with respect to the
              x-axis, in radians

        If ``returnABC==True``, returns (x0,y0,A,B,C), where (x0,y0) are as above, and
        (A,B,C) are the ellipse parameters in canonical form.  See the module docstring
        for more info.
    """
    # Get the datapoints to fit
    yy,xx = np.meshgrid(np.arange(ar.shape[1]),np.arange(ar.shape[0]))
    rr = np.sqrt((xx-x0)**2 + (yy-y0)**2)
    _mask = (rr>ri) * (rr<=ro)
    if mask is not None:
        _mask *= mask==False
    xs,ys = np.nonzero(_mask)
    vals = ar[_mask]

    # Get initial parameters guess
    p0 = [x0,y0,(2/(ri+ro))**2,0,(2/(ri+ro))**2]

    # Fit
    x,y,A,B,C = leastsq(ellipse_err, p0, args=(xs,ys,vals))[0]

    # Convert ellipse params
    a,e,theta = convert_ellipse_params(A,B,C)

    if not returnABC:
        return x,y,a,e,theta
    else:
        return x,y,A,B,C

def ellipse_err(p, x, y, val):
    """
    For a point (x,y) in a 2d cartesian space, and a function taking the value
    val at point (x,y), and some 1d ellipse in this space given by
            ``A(x-x0)^2 + B(x-x0)(y-y0) + C(y-y0)^2 = 1``
    this function computes the error associated with the function's value at (x,y)
    given by its deviation from the ellipse times val.
    """
    x,y = x-p[0],y-p[1]
    return (p[2]*x**2 + p[3]*x*y + p[4]*y**2 - 1)*val


###### Fitting from amorphous diffraction rings ######

def fit_ellipse_amorphous_ring(data,x0,y0,ri,ro,p0=None,mask=None):
    """
    Fit the amorphous halo of a diffraction pattern, including any elliptical distortion.

    The fit function is::

        f(x,y; I0,I1,sigma0,sigma1,sigma2,c_bkgd,R,x0,y0,B,C) =
            Norm(r; I0,sigma0,0) +
            Norm(r; I1,sigma1,R)*Theta(r-R)
            Norm(r; I1,sigma2,R)*Theta(R-r) + offset

    where

        * (x,y) are cartesian coordinates,
        * r is the radial coordinate,
        * (I0,I1,sigma0,sigma1,sigma2,c_bkgd,R,x0,y0,B,C) are parameters,
        * Norm(x;I,s,u) is a gaussian in the variable x with maximum amplitude I,
          standard deviation s, and mean u
        * Theta(x) is a Heavyside step function

    The function thus contains a pair of gaussian-shaped peaks along the radial
    direction of a polar-elliptical parametrization of a 2D plane. The first gaussian is
    centered at the origin. The second gaussian is centered about some finite R, and is
    'two-faced': it's comprised of two half-gaussians of different standard deviations,
    stitched together at their mean value of R. This Janus (two-faced ;p) gaussian thus
    comprises an elliptical ring with different inner and outer widths.

    The parameters of the fit function are

        * I0: the intensity of the first gaussian function
        * I1: the intensity of the Janus gaussian
        * sigma0: std of first gaussian
        * sigma1: inner std of Janus gaussian
        * sigma2: outer std of Janus gaussian
        * c_bkgd: a constant offset
        * R: center of the Janus gaussian
        * x0,y0: the origin
        * B,C: The ellipse parameters, in the form 1x^2 + Bxy + Cy^2 = 1

    Args:
        data (2d array): the data
        x0,y0 (numbers): the center
        ri,r0 (numbers): the inner and outer radii of the fitting annulus
        p0 (11-tuple): initial guess parameters. If p0 is None, the function will compute
            a guess at all parameters. If p0 is a 11-tuple it must be populated by some
            mix of numbers and None; any parameters which are set to None will be guessed
            by the function.  The parameters are the 11 parameters of the fit function
            described above, p0 = (I0,I1,sigma0,sigma1,sigma2,c_bkgd,R,x0,y0,B,C).
            Note that x0,y0 are redundant; their guess values are the x0,y0 values passed
            to the main function, but if they are passed as elements of p0 these will
            take precendence.
        mask (2d array of bools): only fit to datapoints where mask is True

    Returns:
        (2-tuple comprised of a 5-tuple and an 11-tuple): Returns a 2-tuple.

        The first element is the ellipse parameters need to elliptically parametrize
        diffraction space, and is itself a 5-tuple:

            * **x0**: x center
            * **y0**: y center,
            * **a**: semimajor axis length
            * **e**: ratio of semiminor/semimajor lengths
            * **theta**: tilt of a-axis w.r.t x-axis, in radians

        The second element is the full set of fit parameters to the double sided gaussian
        function, described above, and is an 11-tuple
    """
    if mask is None:
        mask = np.ones_like(data).astype(bool)
    assert data.shape == mask.shape, "data and mask must have same shapes."

    # Get data mask
    Nx,Ny = data.shape
    yy,xx = np.meshgrid(np.arange(Ny),np.arange(Nx))
    rr = np.hypot(xx-x0,yy-y0)
    _mask = ((rr>ri)*(rr<ro)).astype(bool)
    _mask *= mask

    # Make coordinates, get data values
    x_inds, y_inds = np.nonzero(_mask)
    vals = data[_mask]

    # Get initial parameter guesses
    I0 = np.max(data)
    I1 = np.max(data*mask)
    sigma0 = ri/2.
    sigma1 = (ro-ri)/4.
    sigma2 = (ro-ri)/4.
    c_bkgd = np.min(data)
    B=0
    C=1
    # To guess R, we take a radial integral
    q,radial_profile = radial_integral(data,x0,y0,1)
    R = q[(q>ri)*(q<ro)][np.argmax(radial_profile[(q>ri)*(q<ro)])]

    # Populate initial parameters
    p0_guess = tuple([I0,I1,sigma0,sigma1,sigma2,c_bkgd,R,x0,y0,B,C])
    if p0 is None:
        _p0 = p0_guess
    else:
        assert len(p0)==11
        _p0 = tuple([p0_guess[i] if p0[i] is None else p0[i] for i in range(len(p0))])

    # Perform fit
    p = leastsq(double_sided_gaussian_fiterr, _p0, args=(x_inds, y_inds, vals))[0]

    # Return
    _x0,_y0 = p[7],p[8]
    _A,_B,_C = 1,p[9],p[10]
    _a,_e,_theta = convert_ellipse_params(_A,_B,_C)
    _a *= p[6]
    return (_x0,_y0,_a,_e,_theta),p

def double_sided_gaussian_fiterr(p, x, y, val):
    """
    Returns the fit error associated with a point (x,y) with value val, given parameters p.
    """
    return double_sided_gaussian(p, x, y) - val


def double_sided_gaussian(p, x, y):
    """
    Return the value of the double-sided gaussian function at point (x,y) given parameters p.
    """

    # Unpack parameters
    I0, I1, sigma0, sigma1, sigma2, c_bkgd, R, x0, y0, B, C = p
    r2 = 1 * (x - x0) ** 2 + B * (x - x0) * (y - y0) + C * (y - y0) ** 2
    r = np.sqrt(r2) - R

    return (
        I0 * np.exp(-r2 / (2 * sigma0 ** 2))
        + I1 * np.exp(-r ** 2 / (2 * sigma1 ** 2)) * np.heaviside(-r, 0.5)
        + I1 * np.exp(-r ** 2 / (2 * sigma2 ** 2)) * np.heaviside(r, 0.5)
        + c_bkgd
    )


### Convert between representations

def convert_ellipse_params(A,B,C):
    """
    Converts ellipse parameters from canonical form (A,B,C) into semi-axis lengths and
    tilt (a,e,theta), where e = b/a.
    See module docstring for more info.

    Args:
        A,B,C (floats): parameters of an ellipse in the form:
                             Ax^2 + Bxy + Cy^2 = 1

    Returns:
        (3-tuple): A 3-tuple consisting of:

        * **a**: (float) the semimajor axis length
        * **e**: (float) the ratio of lengths of the semiminor to the semimajor axes
        * **theta**: (float) the tilt of the ellipse semimajor axis with respect to
          the x-axis, in radians
    """
    val = np.sqrt((A-C)**2+B**2)
    b4a = B**2 - 4*A*C
    # Get theta
    if B == 0:
        if A<C:
            theta = 0
        else:
            theta = np.pi/2.
    else:
        theta = np.arctan2((C-A-val),B)
    # Get a,b
    a = - np.sqrt( -2*b4a*(A+C+val) ) / b4a
    b = - np.sqrt( -2*b4a*(A+C-val) ) / b4a
    a,b = max(a,b),min(a,b)
    e = b/a
    return a,e,theta

def convert_ellipse_params_r(a,e,theta):
    """
    Converts from ellipse parameters (a,e,theta) to (A,B,C).
    See module docstring for more info.

    Args:
        A,B,C (floats): parameters of an ellipse in the form:
                             Ax^2 + Bxy + Cy^2 = 1

    Returns:
        (3-tuple): A 3-tuple consisting of:

        * **a**: (float) the semimajor axis length
        * **b**: (float) the semiminor axis length
        * **theta**: (float) the tilt of the ellipse semimajor axis with respect to
          the x-axis, in radians
    """
    sin2,cos2 = np.sin(theta)**2,np.cos(theta)**2
    b = a*e
    a2,b2 = a**2,b**2
    A = sin2/b2 + cos2/a2
    C = cos2/b2 + sin2/a2
    B = 2*(b2-a2)*np.sin(theta)*np.cos(theta)/(a2*b2)
    return A,B,C



### Polar elliptical transformations

def cartesianDataAr_to_polarEllipticalDataAr(
    cartesianData,
    params,
    dr=1,
    dtheta=np.radians(2),
    r_range=None,
    mask=None,
    maskThresh=0.99,
):
    """
    Transforms an array of data in cartesian coordinates into a data array in
    polar-elliptical coordinates.

    If the cartesian coordinates are (qx,qy), then the parametrization for the
    polar-elliptical coordinate system is::

        qx = qx0 + A*r*cos(theta)*cos(phi) - B*r*sin(theta)*sin(phi)
        qy = qy0 + B*r*cos(theta)*sin(phi) + A*r*sin(theta)*cos(phi)

    where the final coordinates are (r,theta), and the parameters are (qx0,qy0,A,B,phi).
    Physically, this corresponds to elliptical coordinates centered at (qx0,qy0),
    stretched by A/B along the semimajor axes, and with those axes tilted by phi with
    respect to the (qx,qy) axes.

    Args:
        cartesianData (2D float array): the data in cartesian coordinates
        params (5-tuple): specifies (qx0,qy0,A,B,phi), the parameters for the
            transformation
        dr (float): sampling of the (r,theta) coords: the width of the bins in r
        dtheta (float): sampling of the (r,theta) coords: the width of the bins in theta,
            in radians
        r_range (number or length 2 list/tuple or None): specifies the sampling of the
            (r,theta) coords.  Precise behavior which depends on the parameter type:
                * if r_range is a number, specifies the maximum r value
                * if r_range is a length 2 list/tuple, specifies the min/max r values
                * if None, autoselects max r value
        mask (2d array of bools): shape must match cartesianData; where mask==False,
            ignore these datapoints in making the polarElliptical data array
        maskThresh (float): the final data mask is calculated by converting mask (above)
            from cartesian to polar elliptical coords.  Due to interpolation, this
            results in some non-boolean values - this is converted back to a boolean
            array by taking polarEllipticalMask = polarTrans(mask) < maskThresh. Cells
            where polarTrans is less than 1 (i.e. has at least one masked NN) should
            generally be masked, hence the default value of 0.99.

    Returns:
        (3-tuple): A 3-tuple, containing:

            * **polarEllipticalData**: *(2D masked array)* a masked array containing
              the data and the data mask, in polarElliptical coordinates
            * **rr**: *(2D array)* meshgrid of the r coordinates
            * **tt**: *(2D array)* meshgrid of the theta coordinates
    """
    if mask is None:
        mask = np.ones_like(cartesianData, dtype=bool)
    assert (
        cartesianData.shape == mask.shape
    ), "Mask and cartesian data array shapes must match."
    assert len(params) == 5, "params must have length 5"

    # Get params
    qx0, qy0, A, B, phi = params

    # Define r_range: 
    if r_range is None: 
        #find corners of image
        corners = np.array([
                            [0,0],
                            [0,cartesianData.shape[0]],
                            [0,cartesianData.shape[1]],
                            [cartesianData.shape[0], cartesianData.shape[1]] 
                            ])
        #find maximum corner distance
        r_min, r_max =0, np.ceil(
                            np.max(
                                np.sqrt(
                                    np.sum((corners -np.broadcast_to(np.array((qx0,qy0)), corners.shape))**2, axis = 1)
                                       )
                                   )
                                ).astype(int)
    else:
        try:
            r_min, r_max = r_range[0], r_range[1]
        except TypeError:
            r_min, r_max = 0, r_range

    Nx, Ny = cartesianData.shape
    # Define the r/theta coords
    r_bins = np.arange(r_min + dr / 2.0, r_max + dr / 2.0, dr)  # values are bin centers
    t_bins = np.arange(-np.pi + dtheta / 2.0, np.pi + dtheta / 2.0, dtheta)
    rr, tt = np.meshgrid(r_bins, t_bins)
    Nr, Nt = rr.shape

    # Get (qx,qy) corresponding to each (r,theta) in the newly defined coords
    xr = rr * np.cos(tt)
    yr = rr * np.sin(tt)
    qx = qx0 + xr * A * np.cos(phi) - yr * B * np.sin(phi)
    qy = qy0 + xr * A * np.sin(phi) + yr * B * np.cos(phi)

    # qx,qy are now shape (Nr,Ntheta) arrays, such that (qx[r,theta],qy[r,theta]) is the point
    # in cartesian space corresponding to r,theta.  We now get the values for the final
    # polarEllipticalData array by interpolating values at these coords from the original
    # cartesianData array.

    transform_mask = (qx > 0) * (qy > 0) * (qx < Nx - 1) * (qy < Ny - 1)

    # Bilinear interpolation
    xF = np.floor(qx[transform_mask])
    yF = np.floor(qy[transform_mask])
    dx = qx[transform_mask] - xF
    dy = qy[transform_mask] - yF
    x_inds = np.vstack((xF, xF + 1, xF, xF + 1)).astype(int)
    y_inds = np.vstack((yF, yF, yF + 1, yF + 1)).astype(int)
    weights = np.vstack(
        ((1 - dx) * (1 - dy), (dx) * (1 - dy), (1 - dx) * (dy), (dx) * (dy))
    )
    transform_mask = transform_mask.ravel()
    polarEllipticalData = np.zeros(Nr * Nt)
    polarEllipticalData[transform_mask] = np.sum(
        cartesianData[x_inds, y_inds] * weights, axis=0
    )
    polarEllipticalData = np.reshape(polarEllipticalData, (Nr, Nt))

    # Transform mask
    polarEllipticalMask = np.zeros(Nr * Nt)
    polarEllipticalMask[transform_mask] = np.sum(mask[x_inds, y_inds] * weights, axis=0)
    polarEllipticalMask = np.reshape(polarEllipticalMask, (Nr, Nt))

    polarEllipticalData = np.ma.array(
        data=polarEllipticalData, mask=polarEllipticalMask < maskThresh
    )
    return polarEllipticalData, rr, tt


### Radial integration

def radial_integral(ar, x0, y0, dr):
    """
    Computes the radial integral of array ar from center (x0,y0) with a step size in r of dr.

    Args:
        ar (2d array): the data
        x0,y0 (floats): the origin

    Returns:
        (2-tuple): A 2-tuple containing:

            * **rbin_centers**: *(1d array)* the bins centers of the radial integral
            * **radial_integral**: *(1d array)* the radial integral
    """
    rmax = int(
        max(
            (
                np.hypot(x0, y0),
                np.hypot(x0, ar.shape[1] - y0),
                np.hypot(ar.shape[0] - x0, y0),
                np.hypot(ar.shape[0] - x0, ar.shape[1] - y0),
            )
        )
    )
    polarAr, rr, tt = cartesianDataAr_to_polarEllipticalDataAr(
        ar, params=(x0, y0, 1, 1, 0), dr=dr, dtheta=np.radians(2), r_range=rmax
    )
    radial_integral = np.sum(polarAr, axis=0)
    rbin_centers = rr[0, :]
    return rbin_centers,radial_integral


def radial_elliptical_integral(ar, dr, ellipse_params):
    """
    Computes the radial integral of array ar from center (x0,y0) with a step size in r of dr.

    Args:
        ar (2d array): the data
        dr (number): the r sampling
        ellipse_params (5-tuple): the parameters (x0,y0,A,B,phi) for the ellipse

    Returns:
        (2-tuple): A 2-tuple containing:

            * **rbin_centers**: *(1d array)* the bins centers of the radial integral
            * **radial_integral**: *(1d array)* the radial integral
        radial_integral (1d array) the radial integral
    """
    x0, y0 = ellipse_params[0], ellipse_params[1]
    rmax = int(
        max(
            (
                np.hypot(x0, y0),
                np.hypot(x0, ar.shape[1] - y0),
                np.hypot(ar.shape[0] - x0, y0),
                np.hypot(ar.shape[0] - x0, ar.shape[1] - y0),
            )
        )
    )
    polarAr, rr, tt = cartesianDataAr_to_polarEllipticalDataAr(
        ar, params=ellipse_params, dr=dr, dtheta=np.radians(2), r_range=rmax
    )
    radial_integral = np.sum(polarAr, axis=0)
    rbin_centers = rr[0, :]
    return rbin_centers,radial_integral



### Correct Bragg peak positions, making a circular coordinate system

def correct_braggpeak_elliptical_distortions(braggpeaks,e,theta,x0=0,y0=0):
    """
    Given some elliptical distortions with ellipse parameters p and some measured
    PointListArray of Bragg peak positions braggpeaks, returns the elliptically corrected
    Bragg peaks.

    Args:
        braggpeaks (PointListArray): the Bragg peaks
        e (number): the length ratio of semiminor/semimajor axes
        theta (number): tilt of the a-axis with respect to the x-axis, in radians
        x0,y0 (number): the ellipse center; if the braggpeaks have been centered, these
            should be zero

    Returns:
        braggpeaks_corrected    (PointListArray) the corrected Bragg peaks
    """
    assert(isinstance(braggpeaks,PointListArray))
    # Get the transformation matrix
    sint, cost = np.sin(theta-np.pi/2.), np.cos(theta-np.pi/2.)
    T = np.array(
            [
                [e*sint**2 + cost**2, sint*cost*(1-e)],
                [sint*cost*(1-e), sint**2 + e*cost**2]
            ]
        )

    # Correct distortions
    braggpeaks_corrected = braggpeaks.copy(name=braggpeaks.name + "_ellipsecorrected")
    for Rx in range(braggpeaks_corrected.shape[0]):
        for Ry in range(braggpeaks_corrected.shape[1]):
            pointlist = braggpeaks_corrected.get_pointlist(Rx, Ry)
            x, y = pointlist.data["qx"] - x0, pointlist.data["qy"] - y0
            xyar_i = np.vstack([x, y])
            xyar_f = np.matmul(T, xyar_i)
            pointlist.data["qx"] = xyar_f[0, :] + x0
            pointlist.data["qy"] = xyar_f[1, :] + y0
    return braggpeaks_corrected



### Fit an ellipse to crystalline scattering with a known angle between peaks

def constrain_degenerate_ellipse(data, x, y, a, b, theta, r_inner, r_outer, phi_known, fitrad=6):
    """
    When fitting an ellipse to data containing 4 diffraction spots in a narrow annulus about the
    central beam, the answer is degenerate: an infinite number of ellipses correctly fit this
    data.  Starting from one ellipse in the degenerate family of ellipses, this function selects
    the ellipse which will yield a final angle of phi_known between a pair of the diffraction
    peaks after performing elliptical distortion correction.

    Note that there are two possible angles which phi_known might refer to, because the angle of
    interest is well defined up to a complementary angle.  This function is written such that
    phi_known should be the smaller of these two angles.

    Args:
        data (ndarray) the data to fit, typically a Bragg vector map
        x (float): the initial ellipse center, x
        y (float): the initial ellipse center, y
        a (float): the initial ellipse first semiaxis
        b (float): the initial ellipse second semiaxis
        theta (float): the initial ellipse angle, in radians
        r_inner (float): the fitting annulus inner radius
        r_outer (float): the fitting annulus outer radius
        phi_known (float): the known angle between a pair of diffraction peaks, in radians
        fitrad (float): the region about the fixed data point used to refine its position

    Returns:
        (2-tuple): A 2-tuple containing:

            * **a_constrained**: *(float)* the first semiaxis of the selected ellipse
            * **b_constrained**: *(float)* the second semiaxis of the selected ellipse
    """
    # Get 4 constraining points
    xs,ys = np.zeros(4),np.zeros(4)
    yy,xx = np.meshgrid(np.arange(data.shape[1]),np.arange(data.shape[0]))
    rr = np.sqrt((xx-x)**2+(yy-y)**2)
    annular_mask = (rr>r_inner)*(rr<=r_outer)
    data_temp = np.zeros_like(data)
    data_temp[annular_mask] = data[annular_mask]
    for i in range(4):
        x_constr,y_constr = np.unravel_index(np.argmax(gaussian_filter(data_temp,2)),(data.shape[0],data.shape[1]))
        rr = np.sqrt((xx-x_constr)**2+(yy-y_constr)**2)
        mask = rr<fitrad
        xs[i],ys[i] = get_CoM(data*mask)
        data_temp[mask] = 0

    # Transform constraining points coordinate system
    xs -= x
    ys -= y
    T = np.squeeze(np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]]))
    xs,ys = np.matmul(T,np.array([xs,ys]))

    # Get symmetrized constraining point
    angles = np.arctan2(ys,xs)
    distances = np.hypot(xs,ys)
    angle = np.mean(np.min(np.vstack([np.abs(angles),np.pi-np.abs(angles)]),axis=0))
    distance = np.mean(distances)
    x_fixed,y_fixed = distance*np.cos(angle),distance*np.sin(angle)

    # Get semiaxes a,b for the specified theta
    t = x_fixed/(a*np.cos(phi_known/2.))
    a_constrained = a*t
    b_constrained = np.sqrt(y_fixed**2/(1-(x_fixed/(a_constrained))**2))

    return a_constrained, b_constrained


## MOVE TO VIS
def compare_double_sided_gaussian(data, p, power=1, mask=None):
    """
    Plots a comparison between a diffraction pattern and a fit, given p.
    """
    if mask is None:
        mask = np.ones_like(data)

    yy, xx = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))
    data_fit = double_sided_gaussian(p, xx, yy)

    theta = np.arctan2(xx - p[7], yy - p[8])
    theta_mask = np.cos(theta * 8) > 0
    data_combined = (data * theta_mask + data_fit * (1 - theta_mask)) ** power
    data_combined = mask * data_combined
    plt.figure(12, clear=True)
    plt.imshow(data_combined)

    return

## Create look up table for background subtraction
def get_1Dbackground(data, qx0, qy0 ,e, phi, 
                    maskUpdateIter=3, 
                    min_relative_threshold = 4,
                    smoothing = False, 
                    smoothingWindowSize = 3, 
                    smoothingPolyOrder = 4, 
                    smoothing_log = True, 
                    min_background_value=1E-3, 
                    return_polararr=False):
    """
    Gets the median polar background for a diffraction pattern

    Accepts: 
    data                    (ndarray) the data for which to find the polar eliptical background, usually a diffraction pattern
    qx0,qy0                 (floats) the ellipse center; if the braggpeaks have been centered,
                            these should be zero
    e                       (float) the length ratio of semiminor/semimajor axes
    phi                     (float) tilt of the major axis with respect  to (qx, qy) axis, in radians 
    maskUpdate_iter         (integer)
    min_relative_threshold  (float)
    smoothing               (bool) if true savgol filter smoothing is applied
    smoothingWindowSize     (integer) size of the smoothing window, must be odd number
    smoothingPolyOrder      (number) order of the polynomial smoothing to be applied
    smoothing_log           (bool) if true log smoothing is performed
    min_background_value    (float) if log smoothing is true, a zero value will be replaced with a small nonzero float
    return_polar_arr        (bool) if True the polar transform with the masked high intensity peaks will be returned 

    Returns: 
    background1D (ndarray) 1D polar elliptical background
    r_bins       (ndarray) the elliptically transformed radius associated with background1D
    polarData    (ndarray) **optional: returns the masked polar transform from which the 1D background is computed
    """
    # assert data is proper form 
    assert isinstance(smoothing, bool), "Smoothing must be bool"
    assert smoothingWindowSize%2==1, 'Smoothing window must be odd' 
    assert isinstance(return_polararr, bool), "return_polararr must be bool"
   
    # Compute Polar Transform
    polarData, rr, tt = cartesianDataAr_to_polarEllipticalDataAr(data,tuple([qx0,qy0, 1, e, phi]))
   
    # Crop polar data to maximum distance which contains information from original image
    if (polarData.mask.sum(axis = (0))==polarData.shape[0]).any():
            ii = polar.data.shape[1]
            while(polar.mask[:,ii].all()==True):
                ii = ii-1
            maximalDistance = ii
            polarData = polarData[:,0:maximalDistance]
            r_bins = rr[0,0:maximalDistance]
    else:
            r_bins = rr[0,:]

    # Iteratively mask off high intensity peaks
    maskPolar = np.copy(polarData.mask)
    for ii in range(maskUpdateIter+1): 
        if ii > 0:    
            maskUpdate = np.logical_or(maskPolar,  
                                        polarData/background1D > min_relative_threshold)
            # Prevent entire columns from being masked off 
            colMaskMin = np.all(maskUpdate, axis = 0)  # Detect columns that are empty
            maskUpdate[:,colMaskMin] = polarData.mask[:,colMaskMin] # reset empty columns to values of previous iterations
            polarData.mask  = maskUpdate  # Update Mask

        background1D = np.ma.median(polarData, axis = 0) 

    background1D = np.maximum(background1D, min_background_value)

    if smoothing == True:
        if smoothing_log==True: 
            background1D = np.log(background1D)

        background1D = savgol_filter(background1D, 
                                     smoothingWindowSize, 
                                     smoothingPolyOrder)
        if smoothing_log==True: 
            background1D = np.exp(background1D)
    if return_polararr ==True: 
        return(background1D, r_bins, polarData)
    else: 
        return(background1D, r_bins)

#Create 2D Background 
def get_2Dbackground(data, background1D, r_bins, qx0, qy0, phi, e):
    """
    Gets 2D polar elliptical background from linear 1D background 

    Accepts:
    data            (ndarray) the data for which to find the polar eliptical background, usually a diffraction pattern
    background1D:   (ndarray) a vector representing the radial elliptical background 
    r_bins:         (ndarray) a vector of the elliptically transformed radius associated with background1D
    qx0,qy0         (floats) the ellipse center; if the braggpeaks have been centered,
                              these should be zero
    e               (float) the length ratio of semiminor/semimajor axes
    phi             (float) tilt of the major axis with respect  to (qx, qy) axis, in radians 

    Returns: 
    2D Background   (ndarray) 2D polar elliptical median background image
    """
    assert r_bins.shape==background1D.shape, "1D background and r_bins must be same length"
    # Define centered 2D cartesian coordinate system
    yc, xc = np.meshgrid(np.arange(0,data.shape[1])-qy0, 
                         np.arange(0,data.shape[0])-qx0)
   

    # Calculate the semimajor axis distance for each point in the 2D array
    r = np.sqrt(((xc*np.cos(phi)+yc*np.sin(phi))**2)+
                (((xc*np.sin(phi)-yc*np.cos(phi))**2)/(e**2)))

    # Create a 2D eliptical background using linear interpolation  
    f = interp1d(r_bins, background1D, fill_value = 'extrapolate')
    background2D = f(r)

    return(background2D)

