# PowNet Refactored
![license MIT](https://img.shields.io/github/license/kamal0013/PowNet) 

# PyPowNet: A Python Library for PowNet Model Optimization
[PowNet](https://github.com/kamal0013/PowNet/) is a least-cost optimization model for simulating the Unit Commitment and Economic Dispatch of large-scale power systems.
It has been applied to model Cambodian, Laotian, and Thai power systems.
PyPowNetR improves the original implementation of PowNet and simplifies the model specification process.
It aims to help researchers to import their own power system data on the PowNet model and and serve as a benchmark for optimization solvers.
Ultimately, we hope that our effort will encourage more regions to adopt renewable energy sources in the power system.

# Requirements
PyPowNetR is written in Python 3.6. It requires the following Python packages: (i) Pyomo, (ii) NumPy, and (iii) Pandas. It also requires an optimization solver (e.g. CPLEX). 
PyPowNetR has been tested in Anaconda on Windows 10.

# Installation
You can perform a minimal install of ``pypownetr`` with:

```bash
    git clone https://github.com/pacowong/pypownet.git
    cd pypownet
    pip install -e .
```

# How to run
```python
python pypownetr/solver.py datasets/kamal0013/camb_2016 2016 1 2 1 glpk
```
If you have installed [glpk], this will execute the model using the data on Cambodian power system.
The script also generates .csv files containing the values of each decision variable.

# Citation
If you use PyPowNetR for your research, please cite the following papers (mainly from the original authors), which can be found in [this document](README_LONG.md)

# License
PyPowNetR is released under the MIT license. 
