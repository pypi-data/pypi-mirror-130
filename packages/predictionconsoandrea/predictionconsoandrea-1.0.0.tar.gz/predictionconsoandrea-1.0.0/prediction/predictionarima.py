import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
import pickle
import warnings
warnings.filterwarnings('ignore')

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA

with open("b001depuisledebut.pkl",'rb') as f:
    s=pickle.load(f)
dfpr=s

dfpr=dfpr.rename(columns={'C00000003-B001-3-kW sys-JTW':'B001'})
# dfpr=dfpr.squeeze()
dfpr=dfpr[dfpr.abs()<5000]
dfpr= dfpr.ffill()

#prepresentation des données

plt.xlabel('Date')
plt.ylabel('conso energetique')
plt.plot(dfpr)
plt.show()

# Faisons une fonction consistant à vérifier la stationnarité des données et
# à faire fonctionner le test ADCF. Comme nous devrons répéter les étapes plusieurs
#  fois, la création de cette fonction sera très pratique.

def test_stationarity(timeseries):

    #Determine rolling statistics
    movingAverage = timeseries.rolling(window=12).mean()
    movingSTD = timeseries.rolling(window=12).std()

    #Plot rolling statistics
    plt.plot(timeseries, color='blue', label='Original')
    plt.plot(movingAverage, color='red', label='moyenne mobile')
    plt.plot(movingSTD, color='black', label='ecart-type mobile')
    plt.legend(loc='best')
    plt.title('moyenne et ecart-type mobile')
    plt.show()

    #Perform Dickey–Fuller test:
    # print('Results of Dickey Fuller Test:')
    df_test = adfuller(timeseries['B001'])
    # dfoutput = pd.Series(df_test[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    print('Statistiques ADF : {}'.format(df_test[0]))
    print('p-value : {}'.format(df_test[1]))
    print('Valeurs Critiques :')
    for key,value in df_test[4].items():
        print('\t{}: {}'.format(key, value))
    #     dfoutput['Critical Value (%s)'%key] = value
    # print(dfoutput)

#tester la fonction
test_stationarity(dfpr)

# le result sur les données montre que la serie temporelle est stationnaire
# mais appliquons quelques transformations de données pour atteindre une bonne stationnarité.

"échelle logarithmique/Log Transformation,"

dfpr_log=np.log(dfpr)
plt.plot(dfpr_log)
# plt.show()
rollmean_log = dfpr_log.rolling(window=12).mean()
rollstd_log = dfpr_log.rolling(window=12).std()

plt.plot(dfpr_log, color='blue', label='Original')
plt.plot(rollmean_log, color='red', label='Rolling Mean')
plt.plot(rollstd_log, color='black', label='Rolling Std')
plt.legend(loc='best')
plt.title('Rolling Mean & Standard Deviation (Logarithmic Scale)')
plt.show()

# D'après le graphique ci-dessus, les séries temporelles avec une échelle logarithmique ainsi que la moyenne glissante (moving avg)
# ont toutes deux une composante de tendance. Ainsi, soustraire l'une
# de l'autre devrait supprimer la composante de tendance.

dfpr_new = dfpr_log - rollmean_log
dfpr_new.dropna(inplace=True)
test_stationarity(dfpr_new)

# Time Shift Transformation
dfpr_log_diff = dfpr_log - dfpr_log.shift()
plt.plot(dfpr_log_diff)
# plt.show()
dfpr_log_diff.dropna(inplace=True)
plt.plot(dfpr_log_diff)
plt.show()

test_stationarity(dfpr_log_diff)

# Décomposons maintenant les 3 composantes de la série de l'échelle logarithmique
# en utilisant une fonction de la bibliothèque du système. Une fois que nous avons
# séparé les composantes, nous pouvons simplement ignorer la tendance et la saisonnalité et
# vérifier la nature de la partie résiduelle.

decomposition = seasonal_decompose(dfpr_log)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(dfpr_log, label='Original')
plt.legend(loc='best')

plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')

plt.subplot(413)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')

plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

# il peut y avoir des cas où une observation consiste simplement en une tendance et une saisonnalité. Dans ce cas, il n'y aura pas de composante
#  résiduelle et ce serait un nul ou NaN. Par conséquent, nous éliminons
#   également ces cas.

dfpr_decompose = residual
dfpr_decompose.dropna(inplace=True)

rollmean_decompose = dfpr_decompose.rolling(window=12).mean()
rollstd_decompose = dfpr_decompose.rolling(window=12).std()

plt.plot(dfpr_decompose, color='blue', label='Original')
plt.plot(rollmean_decompose, color='red', label='Rolling Mean')
plt.plot(rollstd_decompose, color='black', label='Rolling Std')
plt.legend(loc='best')
plt.title('Rolling Mean & Standard Deviation sur le df du residual')
plt.show()

# Plotting ACF & PACF
# Le PACF exprime la corrélation entre les observations faites à deux moments dans le temps
#  tout en tenant compte de l’influence éventuelle d’autres points de données.

lag_acf = acf(dfpr_log_diff, nlags=20)
lag_pacf = pacf(dfpr_log_diff, nlags=20, method='ols')

#Plot ACF:
plt.subplot(121)
plt.plot(lag_acf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96/np.sqrt(len(dfpr_log_diff)), linestyle='--', color='gray')
plt.axhline(y=1.96/np.sqrt(len(dfpr_log_diff)), linestyle='--', color='gray')
plt.title('Autocorrelation Function')

#Plot PACF
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96/np.sqrt(len(dfpr_log_diff)), linestyle='--', color='gray')
plt.axhline(y=1.96/np.sqrt(len(dfpr_log_diff)), linestyle='--', color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()
plt.show()


# AR Model
#
# Making order = (2,1,0)

model1 = ARIMA(dfpr_log, order=(2,1,0))
results_AR = model1.fit(disp=-1)
plt.plot(dfpr_log_diff)
plt.plot(results_AR.fittedvalues, color='red')
plt.title('RSS: %.4f'%sum((results_AR.fittedvalues - dfpr_log_diff['B001'])**2))
plt.show()
print('Plotting AR model')


# MA Model
#
# Making order = (0,1,2)

model2 = ARIMA(dfpr_log, order=(0,1,2))
results_MA = model2.fit(disp=-1)
plt.plot(dfpr_log_diff)
plt.plot(results_MA.fittedvalues, color='red')
plt.title('RSS: %.4f'%sum((results_MA.fittedvalues - dfpr_log_diff['B001'])**2))
plt.show()
print('Plotting MA model')


# AR+I+MA = ARIMA Model
#
# Making order = (2,1,2)

model = ARIMA(dfpr_log, order=(2,1,2))
results_ARIMA = model.fit(disp=-1)
plt.plot(dfpr_log_diff)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.title('RSS: %.4f'%sum((results_ARIMA.fittedvalues - dfpr_log_diff['B001'])**2))
plt.show()
print('Plotting ARIMA model')

# Une fois le modèle ARIMA construit, nous allons maintenant générer des prédictions.
# Mais, avant de faire des graphiques pour les prédictions, nous devons reconvertir
#  les prédictions dans leur forme originale. En effet, notre modèle a été construit
#  sur des données transformées en logarithme.

predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
predictions_ARIMA_diff.head()

predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
predictions_ARIMA_diff_cumsum.head()

predictions_ARIMA_log = pd.Series(dfpr_log['B001'].iloc[0], index=dfpr_log.index)
predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum, fill_value=0)
predictions_ARIMA_log.head()


# Inverse of log is exp

predictions_ARIMA = np.exp(predictions_ARIMA_log)
plt.plot(dfpr)
plt.plot(predictions_ARIMA)
plt.show()

dfpr_log.head()

print("dernier")
results_ARIMA.plot_predict(1,264)
