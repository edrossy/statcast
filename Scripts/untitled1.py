# %% Plot Learning Curves

import numpy as np
from sklearn.model_selection import learning_curve


estimator = bip.scImputer.__class__(**bip.scImputer.get_params())
data = bip.data.loc[~bip.data.exclude & ~bip.imputed & (bip.data.game_year == 2016),
                       estimator.xLabels + estimator.yLabels]
train_sizes = np.logspace(-2, 0, 11)

train_sizes_abs, train_scores, test_scores = \
    learning_curve(estimator=estimator,
                   X=estimator.createX(data),
                   y=estimator.createY(data),
                   train_sizes=train_sizes,
                   n_jobs=-1,
                   scoring='neg_mean_squared_error',
                   cv=10)

import matplotlib.pyplot as plt

train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

plt.style.use('personal')
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(train_sizes_abs, -train_scores_mean, '-o', label='Training')
ax.plot(train_sizes_abs, -test_scores_mean, '-o', label='Cross-validation')
ax.fill_between(train_sizes_abs, -train_scores_mean + train_scores_std,
                -train_scores_mean - train_scores_std, alpha=0.35, lw=0)
ax.fill_between(train_sizes_abs, -test_scores_mean + test_scores_std,
                -test_scores_mean - test_scores_std, alpha=0.35, lw=0)
ax.legend(loc='best')
ax.set_xlabel('Training Data Size')
ax.set_ylabel('Mean Squared Error')
#ax.set_xlim(left=0)
ax.set_xscale('log')
ax.set_ylim(bottom=0)
ax.set_title('Learning Curve')

# %% Plot Correlation of 2015 vs. 2016

labels = ['Exit Velocity', 'Launch Angle', 'Hit Distance']
units = ['mph', 'degrees', 'feet']


data2015 = bip.data.loc[~bip.data.exclude & ~bip.imputed & (bip.data.game_year == 2015),
                       estimator.xLabels + estimator.yLabels]
data2016 = bip.data.loc[~bip.data.exclude & ~bip.imputed & (bip.data.game_year == 2016),
                       estimator.xLabels + estimator.yLabels]
estimator2015 = bip.scImputer.__class__(**bip.scImputer.get_params()).fitD(data2015)
estimator2016 = bip.scImputer.__class__(**bip.scImputer.get_params()).fitD(data2016)


figs2015 = correlationPlot(estimator2015.trainY_,
                       estimator2015.oob_prediction_,
                       labels=labels,
                       units=units,
                       ms=1)

figs2016 = correlationPlot(estimator2016.trainY_,
                       estimator2016.oob_prediction_,
                       labels=labels,
                       units=units,
                       ms=1)

# %% Choose model from a range of models using cross-validation

from statcast.bip import Bip
from statcast.better.spark import GridSearchCV


years = (2016,)
bip = Bip(years=years)

trainData = bip.data[~bip.data.exclude].sample(frac=0.05)
param_grid = {'criterion': ['mse', 'mae']}

result = GridSearchCV(bip.scImputer, param_grid).fit(bip.scImputer.createX(trainData), bip.scImputer.createY(trainData))