### Couette Flow

##### Controlling Equation for the Couette Flow:

$$
u_{i,j}^{t+1} = u_{i,j}^{t} +  \frac{\mu\Delta t}{\rho \Delta y^2 }(u_{i,j+1}^{t}  - 2u_{i,j}^{t+1} + u_{i,j-1}^{t}  )
$$

where:
$$
\mu = 0.0089 \\
\rho = 1000 \\
\Delta y = 0.1 \\
\Delta t = 1 \\ 
L_x = L_y = 10 \\
V_{Plate} = 5 \\
$$

###  2-D Heat Conduction Equation

$$
\frac{\part^2 T}{\part x^2} + \frac{\part^2 T}{\part y^2} = \frac{1}{\alpha}\frac{\part T}{\part t}    
$$

$$
Discretized \ form \ of \ the\ equation \\
T_{i,j-1} = T_{i,j+1} - 2 \Delta \frac{\part T}{\part y}
$$

For a 2-D case, considering the 2-D Matrix to be an 1-D array, we have the following equation:
$$
T_{i,j}^{n+1} = T_{i,j}^{n} + \alpha\Delta t \Big(\frac{T_{i+1,j}^{n}+T_{i,j+1}^{n}+T_{i-1,j}^{n}+T_{i,j-1}^{n}-4T_{i,j}^{n}}{(\Delta x)^2}\Big)
$$
