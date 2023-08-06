from typing import Any, List, Tuple, Union

import numpy as np
import pandas as pd
import seaborn as sns
import torch

from havi.bayes.inference import get_model, mcmc
from havi.physics.model import EulerAngles, ProbabilisticVariable, Unit, Wave

Tensor = torch.Tensor


class Havi:
    def __init__(
        self,
        incident_angles: List[float],
        scatered_angles: List[float],
        wavelength: float,
    ) -> None:
        self._boudaries_set = False
        theta_i = torch.tensor(incident_angles[0])
        phi_i = torch.tensor(incident_angles[1])
        psi_i = torch.tensor(incident_angles[2])
        theta_s = torch.tensor(scatered_angles[0])
        phi_s = torch.tensor(scatered_angles[1])
        psi_s = torch.tensor(scatered_angles[2])
        landa = torch.tensor(wavelength)
        self.incident_wave = Wave(EulerAngles(theta_i, phi_i, psi_i), landa)
        self.scatered_wave = Wave(EulerAngles(theta_s, phi_s, psi_s), landa)

    def set_boundaries(
        self,
        rms_height: Tuple[float],
        correlation_longitude: Tuple[float],
        dielectric_constant: Tuple[float],
    ) -> None:
        """
        Set boundaries for probabilistic variables

            Parameters:
                rms_height (Tuple[float]): Lower and higher boundaries for rms height values
                correlation_longitude (Tuple[float]): Lower and higher boundaries for correlation long. values
                dielectric_constant (Tuple[float]): Lower and higher boundaries for dielectric constant values

            Returns:
                None
        """

        self.rms_height = ProbabilisticVariable(
            "rms height", Unit.METER, rms_height[0], rms_height[1]
        )
        self.correlation_longitude = ProbabilisticVariable(
            "correlation longitude",
            Unit.METER,
            correlation_longitude[0],
            correlation_longitude[1],
        )
        self.dielectric_constant = ProbabilisticVariable(
            "epsilon", Unit.UNITLESS, dielectric_constant[0], dielectric_constant[1]
        )
        self._boudaries_set = True

    def inference(self, sigma: Tensor, observed: Tensor) -> Union[dict, Any, None]:
        """
        Runs MCMC(Monte Carlo Markov Chain) bayesian inference with NUTS kernel over scatering model

            Parameters:
                sigma (Tensor): error margin for probabilistic model inference
                observed (Tensor): Observed result from scatering measurement to condition bayesian model

            Returns:
                trace (Union[dict, Any, None]): Trace of the inference space of most likely values
        """
        if not self._boudaries_set:
            raise Exception(
                "boundaries for probabilistic variables not set! please call set_boundaries method"
            )
        model = get_model(
            self.dielectric_constant,
            self.rms_height,
            self.correlation_longitude,
            self.incident_wave,
            self.scatered_wave,
        )
        # I am reading this to understand it
        # https://github.com/pyro-ppl/pyro/blob/674af7eab1bb64caf27c9b995913d309229f2c34/pyro/infer/mcmc/api.py#L403
        # observed = torch.Tensor([-12,-7,-8]) #DS2 ### corresponds with Y in conditioned_model
        # ligma = torch.Tensor([0.5]) ## corresponds with sigma in conditioned_model
        mcmc.run(model, sigma, observed)
        mcmc.summary(prob=0.5)
        trace = mcmc.get_samples()
        self.trace = trace
        return trace

    # TODO allow parameter to print or save plots
    def plot(self):
        """
        Plots all of the traced values from MCMC bayesian inference

            Parameters:
                None

            Returns:
                None
        """
        sns.set()
        trace = self.trace
        todos = np.stack((trace["epsilon"], trace["rms_height"], trace["corr_long"])).T
        dfTodos = pd.DataFrame(todos, columns=["eps", "s", "l"])
        # sns.pairplot(dfTodos)
        g = sns.PairGrid(dfTodos)
        g.map_upper(sns.histplot)
        g.map_lower(sns.kdeplot, fill=True)
        g.map_diag(sns.histplot, kde=True)
