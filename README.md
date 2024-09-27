This program uses the **Black-Scholes-Merton** model for analytical calculation and **Monte-Carlo** simulations for numerical calculation of an option's price.
The Monte-Carlo simulations are run in **C++** to increase siumlation runtime and the C++ file is linked to python via **pybind11**, where the C++ file acts as an external library.

Below, I've added some screenshots displaying the program's features and functioning:

![image](https://github.com/user-attachments/assets/34465bbb-e104-4036-aa79-d8e2a85d65b4)

This is the interface that pops up when the code is run. Now for the plotting features that allow viewing how the option prices are affected by different variables.
![image](https://github.com/user-attachments/assets/47faf8c5-7393-47bd-9239-a4448defdafc)
![image](https://github.com/user-attachments/assets/e32eca06-0836-4dd8-b369-4cba2ec150e9)
![image](https://github.com/user-attachments/assets/8652237f-5d3f-47aa-bbeb-33f87818346e)

Below is the simulation of the geometric brownian motion paths of a stock price. (Generating this in C++ to reduce runtime)
![image](https://github.com/user-attachments/assets/a0bdcade-d2fa-43a3-b114-f5077465394f)




