from typing import List
import numpy  as np 
import matplotlib.pyplot as pl

#quadrratic 1D



def yfunc(y):
    return 4*y
def xfunc(x):
    return 2*x


def quadraticGradient():

    x=3
    y=2
    pltox = [x]
    ploty = [y]
    learning_rate=0.1
    for i in range(20):
        y= y- learning_rate*yfunc(y)
        x=x-learning_rate*xfunc(x)
        pltox.append(x)
        ploty.append(y)
    pltox= np.array(pltox)
    ploty= np.array(ploty)
    x_grid = np.linspace(-4, 4, 100)
    y_grid = np.linspace(-4, 4, 100)
    X, Y = np.meshgrid(x_grid, y_grid)
    Z = X**2 + 2 * Y**2  # The original 2D function shape

    # 2. Draw the background contours
    pl.contour(X, Y, Z, levels=20, cmap="viridis")

    # 3. Draw your gradient descent path (Fixed the syntax here!)
    pl.plot(pltox, ploty, color="red", marker="o", label="GD Path")

    pl.xlabel("X")
    pl.ylabel("Y")
    pl.title("2D Gradient Descent Path on Contours")
    pl.legend()
    pl.show()

    return x,y


print(quadraticGradient())