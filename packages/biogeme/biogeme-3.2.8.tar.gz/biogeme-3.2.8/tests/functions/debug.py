"""
Test the optimization module

:author: Michel Bierlaire
:data: Wed Apr 29 17:45:19 2020
"""
# Bug in pylint
# pylint: disable=no-member
#
# Too constraining
# pylint: disable=invalid-name
#
# Not needed in test
# pylint: disable=missing-function-docstring, missing-class-docstring


import unittest
import random as rnd

import numpy as np

import biogeme.biogeme as bio
import biogeme.models as models
import biogeme.optimization as opt
import biogeme.exceptions as excep
from biogeme.expressions import Variable, Beta
from testData import myData1

## For debugging
import biogeme.messaging as msg
logger = msg.bioMessage()
logger.setDebug()

class rosenbrock(opt.functionToMinimize):
    def __init__(self):
        self.x = None

    def setVariables(self, x):
        self.x = x

    def f(self, batch=None):
        if batch is not None:
            raise excep.biogemeError('This function is not data driven.')
        n = len(self.x)
        f = sum(100.0 * (self.x[i + 1]-self.x[i]**2)**2 + (1.0 - self.x[i])**2
                for i in range(n - 1))
        return f

    def g(self):
        n = len(self.x)
        g = np.zeros(n)
        for i in range(n - 1):
            g[i] = g[i] - 400 * self.x[i] * (self.x[i + 1]-self.x[i]**2) - 2 * (1-self.x[i])
            g[i + 1] = g[i + 1] + 200 * (self.x[i + 1]-self.x[i]**2)
        return g

    def h(self):
        n = len(self.x)
        H = np.zeros((n, n))
        for i in range(n-1):
            H[i][i] = H[i][i] - 400 * self.x[i + 1] + 1200 * self.x[i]**2 + 2
            H[i + 1][i] = H[i + 1][i] - 400 * self.x[i]
            H[i][i + 1] = H[i][i + 1] - 400 * self.x[i]
            H[i + 1][i + 1] = H[i + 1][i + 1] + 200
        return H

    def f_g(self, batch=None):
        if batch is not None:
            raise excep.biogemeError('This function is not data driven.')
        return self.f(), self.g()

    def f_g_h(self, batch=None):
        if batch is not None:
            raise excep.biogemeError('This function is not data driven.')
        return self.f(), self.g(), self.h()

    def f_g_bhhh(self, batch=None):
        raise excep.biogemeError('This function is not data driven.')

class testOptimization(unittest.TestCase):
    def setUp(self):
        print('Setup')
        np.random.seed(90267)
        rnd.seed(90267)
        Choice = Variable('Choice')
        Variable1 = Variable('Variable1')
        Variable2 = Variable('Variable2')
        beta1 = Beta('beta1', 0, None, None, 0)
        beta2 = Beta('beta2', 0, None, None, 0)
        V1 = beta1 * Variable1
        V2 = beta2 * Variable2
        V3 = 0
        V = {1: V1, 2: V2, 3: V3}

        likelihood = models.loglogit(V, av=None, i=Choice)
        self.myBiogeme = bio.BIOGEME(myData1, likelihood)
        self.myBiogeme.modelName = 'simpleExample'
        self.theFunction = rosenbrock()
        print('Setup done')

    def testBioNewtonLineSearch(self):
        print('testBioNewtonLineSearch')
        results = self.myBiogeme.estimate(algorithm=opt.newtonLineSearchForBiogeme)
        beta = results.getBetaValues()
        self.assertAlmostEqual(beta['beta1'], 0.144546, 3)
        self.assertAlmostEqual(beta['beta2'], 0.023502, 3)


if __name__ == '__main__':
    unittest.main()
