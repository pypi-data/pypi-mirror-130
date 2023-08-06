from dataclasses import dataclass
from enum import Enum
from typing import Dict

from havi.physics.constants import (CONJUGATE, COS, EXP, LOG_10, PI, POW_2,
                                    REAL_PART, SIN, SQRT, ii)


class Unit(Enum):
    UNITLESS = ''
    METER = 'm'
    SECONDS = 's'
    METER_PER_SECOND = 'm/s'


@dataclass
class Range:
    low: float = 0
    high: float = 1

@dataclass
class Position:
    x: float = 0
    y: float = 0
    z: float = 0

@dataclass
class EulerAngles:
    theta: float = 0
    phi: float = 0
    psi: float = 0

class ProbabilisticVariable:
    def __init__(self, name: str, unit: Unit, low: float, high: float):
        self.name = name
        self.unit = unit
        self.range: Range = Range(low, high)

class Wave:
    def __init__(self, angles: EulerAngles, lambda_: float) -> None:
        self.angles = angles
        self.k = 2*3.1416/lambda_
  
    def kx(self)->float:
        return self.k*SIN(self.angles.theta)*COS(self.angles.phi)

    def ky(self)->float:
        return self.k*SIN(self.angles.theta)*SIN(self.angles.phi)

    def kz(self)->float:
        return self.k*COS(self.angles.theta)

    def kr(self)->float:
        return self.k*SIN(self.angles.theta)

    def k_flat(self, epsilon) -> float:
        seno = SIN(self.angles.theta)
        return self.k*SQRT(epsilon-POW_2(seno,2))

class Floor(Enum):
    ONE = "1"
    TWO = "2"

class WType(Enum):
    GAUSS = 'gauss'
    POWER_LAW = 'power_law'
    EXPONENTIAL = 'exponential'
    CROSS_CORRELATION = 'cross'

class Surface:
    def __init__(self, 
    epsilon: float,
    rms_height: float,
    correlation_longitude: float) -> None:
        self.epsilon = epsilon
        self.rms_height = rms_height
        self.correlation_longitude = correlation_longitude

    def w(self, incident_wave: Wave, scatered_wave: Wave, type: WType) -> float:
        if type == WType.GAUSS:
            return self.w_gauss(incident_wave, scatered_wave)
        elif type == WType.POWER_LAW:
            return self.w_power_law(incident_wave, scatered_wave)
        elif type == WType.EXPONENTIAL:
            return self.w_exp(incident_wave, scatered_wave)
        elif type == WType.CROSS_CORRELATION:
            return self.w_cross(incident_wave, scatered_wave)
        return 0
        
    def w_gauss(self, incident_wave: Wave, scatered_wave: Wave) -> float:
        """
        Likelyhood of dispersion in the scatered direction given the incident direction

            Parameters:
                incident_wave (Wave): Instance of Wave with incidence values
                scatered_wave (Wave): Instance of Wave with scatered values
                layer (Floor): Enum value matching which ground layer we want to calculate for
            
            Returns:
                w_gauss (float): Surface potence spectrum dictated by gaussian function
        """
        delta_k_x = scatered_wave.kx() - incident_wave.kx()
        delta_k_y = scatered_wave.ky() - incident_wave.ky()
        rms_height = self.rms_height
        correlation_longitude = self.correlation_longitude
        exponential = EXP(-0.25*POW_2(correlation_longitude,2)*(POW_2(delta_k_x,2)+POW_2(delta_k_y,2)))
        return POW_2(rms_height,2)*POW_2(correlation_longitude,2)/(4*PI)*exponential
    
    def w_exp(self, incident_wave: Wave, scatered_wave: Wave) -> int:
        delta_k_x = scatered_wave.kx() - incident_wave.kx()
        delta_k_y = scatered_wave.ky() - incident_wave.ky()
        rms_height = self.rms_height
        correlation_longitude = self.correlation_longitude
        return POW_2(rms_height,2)*POW_2(correlation_longitude,2)/(2*PI*POW_2((1+(POW_2(delta_k_x,2)+POW_2(delta_k_y,2))*POW_2(correlation_longitude,2)),(3/2)))

    def w_power_law(self, incident_wave: Wave, scatered_wave: Wave) -> int:
        delta_k_x = scatered_wave.kx() - incident_wave.kx()
        delta_k_y = scatered_wave.ky() - incident_wave.ky()
        rms_height = self.rms_height
        correlation_longitude = self.correlation_longitude
        return POW_2(rms_height,2)*POW_2(correlation_longitude,2)/(2*PI)*EXP(-SQRT(POW_2(delta_k_x,2)+POW_2(delta_k_y,2))*correlation_longitude)

    # def w_cross(self, incident_wave: Wave, scatered_wave: Wave) -> float:
    #     delta_k_x = scatered_wave.kx() - incident_wave.kx()
    #     delta_k_y = scatered_wave.ky() - incident_wave.ky()
    #     s1 = self.layers[Floor.ONE].rms_height
    #     s2 = self.layers[Floor.TWO].rms_height
    #     l1 = self.layers[Floor.ONE].correlation_longitude
    #     l2 = self.layers[Floor.TWO].correlation_longitude
    #     return 0*s1*s2*l1*l2/(4*PI)*EXP(-0.125*(POW_2(l1,2)+POW_2(l2,2))*(POW_2(delta_k_x,2)+POW_2(delta_k_y,2)))

class ScaterModel:
    def __init__(self, surface: Surface) -> None:
        self.surface = surface

    def dispersed_amplitude(self, incident_wave: Wave, scatered_wave: Wave) -> float:
        """this is horrible to read anyway"""
        # calculate once
        eps_1 = self.surface.epsilon
        atm_incidence = self.incidence_atmosphere(incident_wave)
        first_layer_incidence = self.incidence_first_layer(incident_wave)
        incident_flat_wave_eps1 = incident_wave.k_flat(eps_1)
        incident_x_component = incident_wave.kx()
        incident_y_component = incident_wave.ky()
        incident_z_component = incident_wave.kz()
        incident_r_component = incident_wave.kr()
        scatered_flat_wave_eps1 = scatered_wave.k_flat(eps_1)
        scatered_x_component = scatered_wave.kx()
        scatered_y_component = scatered_wave.ky()
        scatered_z_component = scatered_wave.kz()
        scatered_r_component = scatered_wave.kr()
        ikr_sqrd = POW_2(incident_r_component,2)
        sk_flat_sqrd = POW_2(scatered_flat_wave_eps1,2)
        exp_layer_scatered_flat_1 = EXP(ii*(2*scatered_flat_wave_eps1))
        kx_incident_scatered = incident_x_component*scatered_x_component
        ky_incident_scatered = incident_y_component*scatered_y_component
        kx_plus_ky = kx_incident_scatered + ky_incident_scatered
        kz_sqrd = POW_2(incident_z_component,2)
        kz_plus_kr_sqrd = kz_sqrd + ikr_sqrd
        kxi_minus_kxs = incident_x_component - scatered_x_component
        kyi_minus_kys = incident_y_component - scatered_y_component
        ix_kzkrsqrd_sx = incident_x_component*(kz_plus_kr_sqrd)*scatered_x_component
        scat_x_sqrd = POW_2(scatered_x_component,2)
        scat_y_sqrd = POW_2(scatered_y_component,2)
        incident_flat_1_sqrd = POW_2(incident_flat_wave_eps1,2)
        s_flat_1_minus_z_1 = scatered_flat_wave_eps1 - scatered_z_component*eps_1
        long_term = incident_flat_1_sqrd*(kx_plus_ky) + ikr_sqrd*((kxi_minus_kxs)*scatered_x_component + (kyi_minus_kys)*scatered_y_component)
        other_long_term = ix_kzkrsqrd_sx + incident_y_component*kz_sqrd*scatered_y_component - ikr_sqrd*(scat_x_sqrd - ky_incident_scatered + scat_y_sqrd)
        third_long_term = scatered_flat_wave_eps1*(kx_plus_ky)*((-1 + atm_incidence)*incident_z_component + first_layer_incidence*incident_flat_wave_eps1*SQRT(eps_1))
        exp_sep_incident_flat_1 = EXP(ii*incident_flat_wave_eps1)
        
        # pieces of the formula
        x = scatered_r_component*(exp_layer_scatered_flat_1) + incident_flat_wave_eps1
        y = third_long_term
        z = sk_flat_sqrd*(kx_plus_ky)*SQRT(eps_1)
        a = (first_layer_incidence) * (long_term)
        b = (1 + atm_incidence)*(other_long_term)*eps_1
        c = -(eps_1) + scatered_flat_wave_eps1
        d = exp_sep_incident_flat_1
        e = third_long_term
        f = first_layer_incidence*sk_flat_sqrd*(kx_plus_ky)*SQRT(eps_1)
        g = first_layer_incidence
        h = long_term
        i = 1 + atm_incidence
        j = other_long_term
        k = eps_1 + scatered_flat_wave_eps1

        q = x*(-y + z - a * SQRT(eps_1) + b)*c - d*(-e + f + g*h*SQRT(eps_1) - i*j*eps_1)*k
        r = (exp_sep_incident_flat_1*incident_r_component*(scat_x_sqrd + scat_y_sqrd)*(EXP(2*ii*scatered_flat_wave_eps1)*(s_flat_1_minus_z_1)*(-(eps_1) + scatered_flat_wave_eps1) - (scatered_flat_wave_eps1 + scatered_z_component*eps_1)*(eps_1 + scatered_flat_wave_eps1))) 
        return q/r
    
    def incidence_atmosphere(self, wi: Wave):
        # a0VV
        eps_1 = self.surface.epsilon
        incident_flat_wave_eps1 = wi.k_flat(eps_1)
        incident_z_component = wi.kz()
        incident_flat_1_sqrd = POW_2(incident_flat_wave_eps1,2)
        q = -ii*incident_flat_wave_eps1*(incident_z_component)*COS(incident_flat_wave_eps1) + (-incident_flat_1_sqrd + incident_z_component)*SIN(incident_flat_wave_eps1)
        r = ii*incident_flat_wave_eps1*(incident_z_component)*COS(incident_flat_wave_eps1) + (incident_flat_1_sqrd + incident_z_component)*SIN(incident_flat_wave_eps1)
        return q/r
    def incidence_first_layer(self, wi: Wave):
        # b0VV
        eps_1 = self.surface.epsilon
        incident_flat_wave_eps1 = wi.k_flat(eps_1)
        incident_z_component = wi.kz()
        q = -2*(incident_flat_wave_eps1)*incident_z_component
        r = EXP(2*ii*incident_flat_wave_eps1)*(incident_flat_wave_eps1)*(incident_flat_wave_eps1 - incident_z_component) - (incident_flat_wave_eps1)*(incident_flat_wave_eps1 + incident_z_component)
        return q/r


    def scatering(self, incident_wave: Wave, scatered_wave: Wave) -> float:
        """
            Returns the scatering of a given Channel in decibels.

                Parameters:
                        incident_wave (Wave): Instance of wave with the incidence values
                        incident_wave (Wave): Instance of wave with the scatered values

                Returns:
                        scatering (float): value of scatering in given channel in decibels
        """
        ki = incident_wave.k
        
        dispersed_amp_1 = self.dispersed_amplitude(incident_wave, scatered_wave)

        w_1 = self.surface.w(incident_wave, scatered_wave, WType.GAUSS)
    
        aux = 4*PI*POW_2(ki,2)*POW_2(COS(scatered_wave.angles.theta),2)*(POW_2(abs(dispersed_amp_1),2)*w_1)
            
        return 10*LOG_10(aux)