import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dataset = pd.read_csv('media3.csv')
dataset2 = pd.read_csv('media2.csv')

attitude_count = dataset.groupby(['government_attitude']).size()


x = np.arange(3)
plt.bar(x, attitude_count)
plt.xticks(x, ['anti', 'neutral', 'pro'])
plt.show()

plt.bar(x, dataset2['avg_tone'])
plt.xticks(x, dataset2['media'])

plt.show()