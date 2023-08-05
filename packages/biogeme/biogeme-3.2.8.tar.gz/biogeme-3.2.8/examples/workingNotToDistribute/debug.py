import pandas as pd
import biogeme.optimization as opt
import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models
from biogeme.expressions import Beta, Variable
import biogeme.messaging as msg
logger = msg.bioMessage()
logger.setDebug()

df = pd.DataFrame({'Person': [1, 1, 1, 2, 2],
                   'Exclude': [0, 0, 1, 0, 1],
                   'Variable1': [1, 2, 3, 4, 5],
                   'Variable2': [10, 20, 30,40, 50],
                   'Choice': [1, 2, 3, 1, 2],
                   'Av1': [0, 1, 1, 1, 1],
                   'Av2': [1, 1, 1, 1, 1],
                   'Av3': [0, 1, 1, 1, 1]})
myData = db.Database('test', df)

Choice = Variable('Choice')
Variable1 = Variable('Variable1')
Variable2 = Variable('Variable2')
beta1 = Beta('beta1', 0, None, None, 0)
beta2 = Beta('beta2', 0, None, None, 0)
V1 = beta1 * Variable1
V2 = beta2 * Variable2
V3 = 0
V ={1: V1,2: V2,3: V3}

likelihood = models.loglogit(V, av=None, i=Choice)
myBiogeme = bio.BIOGEME(myData, likelihood, numberOfThreads=1)
myBiogeme.modelName = 'simpleExample'
myBiogeme.saveIterations = False
myBiogeme.generateHtml = False
myBiogeme.generatePickle = False
print(myBiogeme)

f, g, h, gdiff, hdiff = myBiogeme.checkDerivatives(verbose=True)

print(gdiff)
