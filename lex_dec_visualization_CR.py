import pandas as pd
import numpy as np



output = pd.read_csv('output_1.csv')
output_2 = pd.read_csv('output_2.csv')
output_3 = pd.read_csv('output_3.csv')

output['ppt']=1
output_2['ppt']=2
output_3['ppt']=3

output = output.append(output_2)
output = output.append(output_3)

print(output)

from matplotlib import pyplot as plt
import seaborn as sns 
import plotnine as gg 
from plotnine import ggplot

summary = output.groupby(by='trial').aggregate(
    mean_RT=pd.NamedAgg('reaction_time', np.mean),
    std_RT=pd.NamedAgg('reaction_time', np.std)
)
summary.reset_index(inplace=True)

plt.figure()
plt.bar(summary['trial'], summary['mean_RT'])
plt.errorbar(summary['trial'], summary['mean_RT'], summary['std_RT'], fmt='k.')
plt.show()