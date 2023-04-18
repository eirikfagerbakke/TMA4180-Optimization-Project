import importlib
import TensegrityStruct as TS
importlib.reload(TS)
import numpy as np


class FreeStandingStruct(TS.TensegrityStruct):
    """
    A class used to represent free standing structures. The class can also be used to represent structures with
    fixed nodes and only bars present in the structure.

    ...

    Attributes
    ----------
        penalty : Float
            Represents the penalty in the quadratic penalty function

        All other parameters are as in the TensegrityStruct, but the number of fixed nodes is 0 by default.

    Methods
    ----------
        E_cable_e()
            Function to calculate the elastic energy in the cables if there are any present.

        E()
            The object's objective function, i.e. the quadratic penalty function. This was done this way as this is
            really the function we want to minimize for these type of objects, not only its energy. The function
            calculates the function's energy if the penalty is first set to 0.

        gradient()
            Uses previous implementations of the gradient in order to calculate the gradient of our new objective
            function, with the first two components equal to zero, as these represent fixed coordinates.

        The class also inherits all other methods from the TensegrityStruct class.

    """
    def __init__(self, num_of_nodes, nodes, masses, cables, bars, k, c, bar_density, penalty, num_of_fixed_nodes=0):
        """
        :param penalty: Float to represent the penalty in the quadratic penalty function
        """
        TS.TensegrityStruct.__init__(self, num_of_nodes, num_of_fixed_nodes, nodes, masses, cables, bars, k, c, bar_density)

        self.penalty = penalty

    def E(self):
        """
        The object's objective function, i.e. the quadratic penalty function. This was done this way as this is
        really the function we want to minimize for these type of objects, not only its energy. The function
        calculates the function's energy if the penalty is first set to 0.

        :return: The value of the structure's objective function
        """
        x3 = self.nodes[:, -1]
        c_min = np.minimum(x3, np.zeros(self.num_of_nodes))
        return super().E()+self.penalty/2*np.dot(c_min, c_min)

    #def update_nodes(self, new_X):
    #    self.nodes[0, 2] = new_X[0]
     #   self.nodes[1:, ] = np.reshape(new_X[1:], (self.num_of_nodes-1, 3))
      #  self.X = new_X

    def gradient(self):
        """
        Uses previous implementations of the gradient in order to calculate the gradient of our new objective
        function, with the first two components equal to zero, as these represent fixed coordinates.

        :return: The gradient of the objective function
        """
        print(super().gradient())
        penalty_grad = np.zeros(self.X.size) # additional gradient term
        x3 = self.nodes[:,-1]
        c_min = np.minimum(x3, np.zeros(self.num_of_nodes))
        penalty_grad[2::3] = self.penalty*c_min
        #print(penalty_grad)
        grad = super().gradient() + penalty_grad

        grad[:2] = 0
        #grad = grad[2:]
        return grad