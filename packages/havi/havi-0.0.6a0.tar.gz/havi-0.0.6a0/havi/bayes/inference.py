import pyro
from pyro.infer import MCMC, NUTS

from havi.physics.model import (ProbabilisticVariable, ScaterModel, Surface,
                                Wave)


def get_model(epsilon: ProbabilisticVariable, rms_height: ProbabilisticVariable, correlation_longitude: ProbabilisticVariable, incident_wave: Wave, scatered_wave: Wave):
    def model(sigma):
        ep1 = pyro.sample("ep1", pyro.distributions.Uniform(epsilon.range.low, epsilon.range.high))
        s1 = pyro.sample("s1", pyro.distributions.Uniform(rms_height.range.low, rms_height.range.high))
        l1 = pyro.sample("l1", pyro.distributions.Uniform(correlation_longitude.range.low, correlation_longitude.range.high))

        surface = Surface(ep1, s1, l1)
        scater = ScaterModel(surface)
        farlopa = scater.scatering(incident_wave, scatered_wave)
        mu = pyro.deterministic('s0modelMCMC', value=farlopa)
        return pyro.sample("obs", pyro.distributions.Normal(mu, sigma))
    return model


def conditioned_model(model, sigma, y):
    return pyro.poutine.condition(model, data={"obs": y})(sigma)

NUTS_KERNEL = NUTS(conditioned_model, jit_compile=False, ignore_jit_warnings=True)

mcmc = MCMC(
    NUTS_KERNEL,
    num_samples=2000,
    warmup_steps=300,
    num_chains=1,
)
