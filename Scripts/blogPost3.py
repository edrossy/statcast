# %% Fixpath, imports

#import pandas as pd

from statcast.bip import Bip
from statcast.tools.plot import correlationPlot


# %% Load data

years = (2016,)

bip = Bip(years=years)

# %% Plot Imputer Results

imputed = bip.missing(bip.scImputer.yLabels)
inds = bip.data.loc[~bip.data.exclude & ~imputed, :].index
trainInds = bip.scImputer.trainX_.index
testInds = inds.difference(trainInds)

testData = bip.data.loc[testInds, :]

testY = bip.scImputer.createY(testData)
testYp = bip.scImputer.predictD(testData)

labels = ['Exit Velocity', 'Launch Angle', 'Hit Distance']
units = ['mph', 'degrees', 'feet']

figs = correlationPlot(testY,
                       testYp,
                       labels=labels,
                       units=units,
                       ms=1)

[fig.savefig(label + ' {} ImputerResultsOnly'.format(
    ' ,'.join(str(year) for year in years)))
    for fig, label in zip(figs, labels)]

print(bip.scImputer.feature_importances_)

# %% Compare histograms of testing, imputed testing, and imputed missing data

bip.plotSCHistograms()

# %% Save Park Factors

#parkFactors = \
#    pd.DataFrame({label:
#                  bip.scFactorMdl.factors[label]['home_team'].iloc[:, 0]
#                  for label in bip.scFactorMdl.yLabels})
#parkFactors.to_csv('Park Factors 2015-2016.csv')

# %% Compare 2015 & 2016 Park Factors

#data2015 = bip.data[bip.data['game_year'] == 2015]
#data2016 = bip.data[bip.data['game_year'] == 2016]
#
#scFactorMdl15 = statcast.scFactorMdl(data=data2015, dump=False)
#scFactorMdl16 = statcast.scFactorMdl(data=data2016, dump=False)
#
#for key, label, unit in zip(bip.scFactorMdl.yLabels, labels, units):
#    X = scFactorMdl15.factors[key]['home_team'].iloc[:, 0]
#    X.name = '2015 {} ({})'.format(label, unit)
#    Y = scFactorMdl16.factors[key]['home_team'].iloc[:, 0]
#    Y.name = '2016 {} ({})'.format(label, unit)
#    fig, = correlationPlot(X, Y, mfc='None', mec='None')
#    statcast.plotMLBLogos(X, Y, ax=fig.gca())
#    fig.savefig('{} Park Factor 15-16 Correlation'.format(label))

# %% Compare Observed and Imputed Park Factors

#dataObs = bip.data[~imputed]
#dataImp = bip.data[imputed]
#
#scFactorMdlObs = statcast.scFactorMdl(data=dataObs, dump=False)
#scFactorMdlImp = statcast.scFactorMdl(data=dataImp, dump=False)
#
#for key, label, unit in zip(bip.scFactorMdl.yLabels, labels, units):
#    X = scFactorMdlObs.factors[key]['home_team'].iloc[:, 0]
#    X.name = 'Observed {} ({})'.format(label, unit)
#    Y = scFactorMdlImp.factors[key]['home_team'].iloc[:, 0]
#    Y.name = 'Imputed {} ({})'.format(label, unit)
#    fig, = correlationPlot(X, Y, mfc='None', mec='None')
#    statcast.plotMLBLogos(X, Y, ax=fig.gca())
#    fig.savefig('{} Park Factor Observed-Imputed Correlation'.format(label))

# %% Compare 2015 & 2016 Player Skills