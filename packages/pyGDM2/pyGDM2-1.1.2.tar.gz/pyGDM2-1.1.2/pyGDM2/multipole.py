# encoding: utf-8
#
#Copyright (C) 2017-2021, P. R. Wiecha
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
tools around multipole decomposition and effective polarizabilities

"""
from __future__ import print_function
from __future__ import absolute_import

import warnings
# import math

import numpy as np
import copy
import numba

import time


#==============================================================================
# GLOBAL PARAMETERS
#==============================================================================




#==============================================================================
# EXCEPTIONS
#==============================================================================



def multipole_decomposition_exact(sim, field_index, r0=None, epsilon=0.01, 
                                  which_moments=['p', 'm', 'qe', 'qm']):
    """exact multipole decomposition of the nanostructure optical response
    
    ** ------- FUNCTION STILL UNDER TESTING ------- **
    
    Multipole decomposition of electromagnetic field inside nanostructure for 
    electric and magnetic dipole and quadrupole moments.


    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r0 : array, default: None
        [x,y,z] position of multipole decomposition development. 
        If `None`, use structure's center of gravity
    
    epsilon : float, default: 0.01
        additional step on r0 (in nm) to avoid numerical divergence of the Bessel terms
        
    which_moments : list of str, default: ['p', 'm', 'qe', 'qm']
        which multipole moments to calculate and return. supported dipole moments: 
            - 'p': electric dipole (full)
            - 'm': magnetic dipole
            - 'qe': electric quadrupole (full)
            - 'qm': magnetic quadrupole
            - 'p1': electric dipole (first order)
            - 'pt': toroidal dipole
            - 'qe1': electric quadrupole (first order)
            - 'qet': toroidal quadrupole
            
    
    Returns
    -------
    list of multipole moments. Default:
        
    p : 3-vector
        electric dipole moment
    
    m : 3-vector
        magnetic dipole moment
    
    Qe : 3x3 tensor
        electric quadrupole moment
        
    Qm : 3x3 tensor
        magnetic quadrupole moment
    
    
    Notes
    -----
    For details about the method, see: 
    
    Alaee, R., Rockstuhl, C. & Fernandez-Corbaton, I. *An electromagnetic 
    multipole expansion beyond the long-wavelength approximation.*
    Optics Communications 407, 17–21 (2018)
    """
# =============================================================================
#     Exception handling
# =============================================================================
    if sim.E is None: 
        raise ValueError("Error: Scattered field inside the structure not yet " +
                         "evaluated. Run `core.scatter` simulation first.")
    
    which_moments = [wm.lower() for wm in which_moments]
    
# =============================================================================
#     preparation
# =============================================================================
    from scipy.special import spherical_jn as sph_jn

    ## structure
    geo = sim.struct.geometry
    if r0 is None:
        r0 = np.average(geo, axis=0)
    if np.abs(np.linalg.norm(geo - r0, axis=1)).min() > epsilon:
        epsilon = 0
    r = geo - r0 + epsilon                   # epsilon: avoid divergence of 1/kr when r=0
    norm_r = np.linalg.norm(r, axis=1)
    
    ## illumination properties
    field_params = sim.E[field_index][0]
    wavelength = field_params['wavelength']
    sim.struct.setWavelength(wavelength)
    eps_env = sim.dyads.getEnvironmentIndices(wavelength, r0[None,:])[0]  # assume structure is fully in one environment
    n_env = eps_env**0.5
    k = 2*np.pi*n_env / wavelength
    kr = k * norm_r
    
    ## electric polarization density of structure
    alpha_tensor = sim.dyads.getPolarizabilityTensor(wavelength, sim.struct)
    E = sim.E[field_index][1]
    P = np.matmul(alpha_tensor, E[...,None])[...,0]
    rP = np.einsum('ij, ij->i', r, P)
    
    ## bessel functions
    j0kr = sph_jn(0, kr)
    j1kr = sph_jn(1, kr)
    j2kr = sph_jn(2, kr)
    j3kr = sph_jn(3, kr)
    
# =============================================================================
#     multipole calculation
# =============================================================================
    ## ----------- dipole moments
    ## electric dipole
    if 'p' in which_moments or 'p1' in which_moments or 'pt' in which_moments:
        p1 = np.sum(P * j0kr[..., None], axis=0)
        
        ## "toroidal" dipole
        p2 = (k**2 / 2) * np.sum((3*rP[...,None]*r 
                                   - norm_r[..., None]**2 * P) * (j2kr/(kr**2))[..., None], 
                                  axis=0)
        
        p = p1 + p2
    
    ## magnetic dipole
    if 'm' in which_moments:
        m = -(1j*k/2.) * 3 * np.sum(np.cross(r, P) * (j1kr/kr)[..., None], axis=0)
    
    ## ----------- quadrupole moments
    ## electric quadrupole
    if 'qe' in which_moments or 'qe1' in which_moments or 'qet' in which_moments:
        Qe1 = np.zeros((3,3), dtype=np.complex64)
        Qe2 = np.zeros((3,3), dtype=np.complex64)
        for i_a in range(3):
            for i_b in range(3):
                
                ## diagonal term
                if i_a==i_b:
                    rP_delta = rP
                else:
                    rP_delta = 0
                
                ## electric quadrupole
                Qe1[i_a, i_b] = np.sum(
                    (3*(r[:,i_b]*P[...,i_a] + r[:,i_a]*P[...,i_b])
                     - 2*(rP_delta))*(j1kr/kr))
                
                ## "toroidal" quadrupole
                Qe2[i_a, i_b] = np.sum(
                      (5*r[:,i_a]*r[:,i_b]*rP 
                      - norm_r**2 * ((r[:,i_a]*P[:,i_b] + r[:,i_b]*P[:,i_a]) 
                                     + rP_delta)) * (j3kr/(kr**3)))
                
        Qe1 = 3*Qe1
        Qe2 = 3 * 2*k**2 * Qe2
        Qe = Qe1 + Qe2
    
    ## magnetic quadrupole
    if 'qm' in which_moments:
        Qm = np.zeros((3,3), dtype=np.complex64)
        for i_a in range(3):
            for i_b in range(3):
                Qm[i_a, i_b] = np.sum(
                    (r[:,i_a] * np.cross(r, P)[...,i_b] + 
                     r[:,i_b] * np.cross(r, P)[...,i_a])*(j2kr/(kr**2)))
                
        Qm = -2*(1j*k/2.) * 15 * Qm
    
# =============================================================================
#     return results
# =============================================================================
    return_list = []
    for _m in which_moments:
        if _m.lower() == "p1":
            return_list.append(p1)
        if _m.lower() == "pt":
            return_list.append(p2)
        if _m.lower() == "p":
            return_list.append(p)
            
        if _m.lower() == "m":
            return_list.append(m)
            
        if _m.lower() == "qe1":
            return_list.append(Qe1)
        if _m.lower() == "qet":
            return_list.append(Qe2)
        if _m.lower() == "qe":
            return_list.append(Qe)
            
        if _m.lower() in ["qm"]:
            return_list.append(Qm)
    
    return return_list



def extinct(sim, field_index, r0=None, eps_dd=0.001):
    """extinction cross sections from multipole decomposition
    
    ** ------- FUNCTION STILL UNDER TESTING ------- **
    
    Returns extinction cross sections for electric and magnetic dipole and 
    quadrupole moments of the multipole decomposition.
    
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r0 : array, default: None
        [x,y,z] position of mulipole decomposition development. 
        If `None`, use structure's center of gravity
    
    eps_dd : float, default: 0.1
        numerical integration step (in nm). Used for e/m quadrupole extinction.
    
    
    Returns
    -------
    sigma_ext_p : float
        electric dipole extinction cross section (in nm^2)
    
    sigma_ext_m : float
        magnetic dipole extinction cross section (in nm^2)
        
    sigma_ext_q : float
        electric quadrupole extinction cross section (in nm^2)
        
    sigma_ext_mq : float
        magnetic quadrupole extinction cross section (in nm^2)
    
    
    Notes
    -----
    The normalization is assuming an incident field amplitude normalized to 1
    
    For details about the extinction section of multipole moments, see:
    
    Evlyukhin, A. B. et al. *Multipole analysis of light scattering by 
    arbitrary-shaped nanoparticles on a plane surface.*, 
    JOSA B 30, 2589 (2013)
    
    """
    if sim.E is None: 
        raise ValueError("Error: Scattered field inside the structure not yet evaluated. Run `core.scatter` simulation first.")
    
    from pyGDM2 import linear
    
    ## by default, use center of gravity for multimode expansion
    geo = sim.struct.geometry
    if r0 is None:
        r0 = np.average(geo, axis=0)
    
    field_params = sim.E[field_index][0]
    wavelength = field_params['wavelength']
    sim.struct.setWavelength(wavelength)
    k0 = 2*np.pi / wavelength
    eps_env = sim.dyads.getEnvironmentIndices(wavelength, geo[:1])[0]  # structure must be fully in one environment zone
    n_env = eps_env**0.5
    
    ## incident field at multipole position
    env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(r0[None,:], env_dict, **field_params)
    H0 = sim.efield.field_generator(r0[None,:], env_dict, returnField='H', **field_params)
    
    ## normalization
    E2in = np.sum(np.abs(E0)**2, axis=1)   # intensity of incident field
    prefactor = (4 * np.pi * k0 * 1/n_env * 1/E2in).real
    
    p, m, Qe, Qm = multipole_decomposition_exact(sim, field_index, r0)
    
    
    ## --- dipole extinction cross sections
    sigma_ext_p = prefactor * (np.sum(np.conjugate(E0)*p)).imag
    sigma_ext_m = prefactor / n_env * (np.sum(np.conjugate(H0)*m)).imag
    
    
    ## ---  quadrupole extinction cross sections
    gradE0, gradH0 = linear.field_gradient(sim, field_index, r0[None,:], 
                                           delta=eps_dd, which_fields=['E0', 'H0'])
    gradE0cj = np.conj(np.array(gradE0)[:,0,3:])
    gradH0cj = np.conj(np.array(gradH0)[:,0,3:])
    
    sigma_ext_q = prefactor / 12. * \
                    (np.sum(np.tensordot(gradE0cj + gradE0cj.T, Qe) )).imag
    
    sigma_ext_mq = prefactor / n_env / 6 * \
                    (np.sum(np.tensordot(gradH0cj.T, Qm) )).imag
    
    return sigma_ext_p, sigma_ext_m, sigma_ext_q, sigma_ext_mq



def scs(sim, field_index, r0=None):
    """total scattering cross section from multipole decomposition
    
    ** ------- FUNCTION STILL UNDER TESTING ------- **
    
    Returns scattering cross sections for electric and magnetic dipole and 
    quadrupole moments of the multipole decomposition.
    
    
    Parameters
    ----------
    sim : :class:`.core.simulation`
        simulation description
    
    field_index : int
        index of evaluated self-consistent field to use for calculation. Can be
        obtained for specific parameter-set using :func:`.tools.get_closest_field_index`
    
    r0 : array, default: None
        [x,y,z] position of mulipole decomposition development. 
        If `None`, use structure's center of gravity
    
    
    Returns
    -------
    
    sigma_scat_p : float
        electric dipole scattering cross section (in nm^2)
    
    sigma_scat_m : float
        magnetic dipole scattering cross section (in nm^2)
        
    sigma_scat_q : float
        electric quadrupole scattering cross section (in nm^2)
        
    sigma_scat_mq : float
        magnetic quadrupole scattering cross section (in nm^2)
    
    
    Notes
    -----
    The normalization is assuming an incident field amplitude normalized to 1
    
    For details about the method, see: 
        
    Alaee, R., Rockstuhl, C. & Fernandez-Corbaton, I. *An electromagnetic 
    multipole expansion beyond the long-wavelength approximation.*
    Optics Communications 407, 17–21 (2018)
    
    """
# =============================================================================
#     Exception handling
# =============================================================================
    if sim.E is None: 
        raise ValueError("Error: Scattered field inside the structure not yet evaluated. Run `core.scatter` simulation first.")

# =============================================================================
#     scattering section calculation
# =============================================================================
    ## by default, use center of gravity for multimode expansion
    geo = sim.struct.geometry
    if r0 is None:
        r0 = np.average(geo, axis=0)
    
    field_params = sim.E[field_index][0]
    wavelength = field_params['wavelength']
    sim.struct.setWavelength(wavelength)
    k0 = 2*np.pi / wavelength
    
    eps_env = sim.dyads.getEnvironmentIndices(wavelength, geo[:1])[0]  # assume structure is fully in one environment
    n_env = eps_env**0.5
    k = k0*n_env
    
    ## normalization: incident field intensity at multipole position
    env_dict = sim.dyads.getConfigDictG(wavelength, sim.struct, sim.efield)
    E0 = sim.efield.field_generator(r0[None,:], env_dict, **field_params)
    E2in = np.sum(np.abs(E0)**2, axis=1)   # intensity of incident field
    
    ## factor 100: cm --> m (cgs units)
    ## !!!!!! investigate factor 1/0.95
    sc_factor_dp = 100*(k**4 / (n_env**4 * 4*np.pi * E2in)).real / 0.949
    sc_factor_Q = 100/120*(k**4 / (n_env**4 * 4*np.pi * E2in)).real / 0.949
    
    ## the actual scattering sections
    p, m, Qe, Qm = multipole_decomposition_exact(sim, field_index)
    
    scs_p = sc_factor_dp * np.sum(np.abs(p)**2)
    scs_m = sc_factor_dp * np.sum(np.abs(m)**2)
    
    scs_Qe = sc_factor_Q * np.sum(np.abs(k*Qe)**2)
    scs_Qm = sc_factor_Q * np.sum(np.abs(k*Qm)**2)
    
    return scs_p, scs_m, scs_Qe, scs_Qm








