# Havi
[stands for Odin](https://en.wikipedia.org/wiki/H%C3%A1r_and_H%C3%A1rr)


scatering model and bayesian inference

---
**Note from author**

If you use our library on a research or paper please give us a citation

- [PyPi](https://pypi.org/project/havi/)

- [Github](https://github.com/bjornaer/havi)

---

### Installation

    pip install havi

### Usage

```python
import havi as h

# scatering angles
incident_angles = [theta, phi, psi] # incidence angles - floats
scatered_angles = [theta, phi, psi] # scatering angles - floats
wavelength = 0.5

havi = h.Havi(incident_angles, scatered_angles, wavelength)

# surface boudaries for random variables
rms_height = (0.1, 0.8) # lower and higher boundaries
correlation_longitude = (0.1, 0.8) # lower and higher boundaries
dielectric_constant = (0.1, 0.8) # lower and higher boundaries

havi.set_boundaries(rms_height, correlation_longitude, dielectric_constant)

sigma = h.Tensor([0.5])
observed_data = h.Tensor([-12,-7,-8])

trace = havi.inference(sigma, observed) # you can plot the trace however you want OR
havi.plot()
```

### API

This package exports:

A pytorch Tensor type

    havi.Tensor

Our inference model abstraction, holds data of incident wave, scatered wave and their wave length:
        
    havi.Havi(incident_angles: List[float], scatered_angles: List[float], wavelength: float)

Set boundaries for probabilistic variables

    Havi.set_boundaries(rms_height: Tuple[float], correlation_longitude: Tuple[float], dielectric_constant: Tuple[float]) -> None

Runs MCMC(Monte Carlo Markov Chain) bayesian inference with NUTS kernel over scatering model

    Havi.inference(sigma: Tensor, observed: Tensor) -> trace: dict

Plots all of the traced values from MCMC bayesian inference

    Havi.plot() -> None

