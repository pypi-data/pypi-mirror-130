from  changefinderPRO import changefinderTS
from  changefinderPRO import plotTSScore
import numpy as np

data=np.concatenate([np.random.normal(0.7, 0.05, 300),
np.random.normal(1.5, 0.05, 300),
np.random.normal(0.6, 0.05, 300),
np.random.normal(1.3, 0.05, 300)])

ret = changefinderTS(data, r=0.03, order=1, smooth=5)

plotTSScore(data, ret)