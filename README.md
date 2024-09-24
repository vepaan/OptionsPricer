This program uses the **Black-Scholes-Merton** model for analytical calculation and **Monte-Carlo** simulations for numerical calculation of an option's price.
The Monte-Carlo simulations are run in **C++** to increase siumlation runtime and the C++ file is linked to python via **pybind11**, where the C++ file acts as an external library.
