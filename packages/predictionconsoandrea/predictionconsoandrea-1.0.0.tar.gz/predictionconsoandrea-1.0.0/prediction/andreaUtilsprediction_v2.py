import andreaUtilsclustering
import importlib
import pickle
from screeningBuilding.configFilesBuilding import ConfigFilesBuilding
importlib.reload(andreaUtilsclustering)
from andreaUtilsclustering import *
from sklearn.model_selection import train_test_split
import datetime as dt
from datetime import time
import time

"   prediction des courbes je vais tester avec plusieurs moyens pour avoir la bonne prediction "

"je cherche a predire les courbes avec les courbes moyennes de chaque cluster on a pris le nbre de cluster 3"

def appelerdataframe():
    with open("b001.pkl",'rb') as f:
        s=pickle.load(f)

    dff,df_col=s  # dataframe de base le tout premier dataframe de mon projet pour faire resortir les journées
    # #
    # #
    with open('dfcluster.pkl','rb') as f:
        c=pickle.load(f)
    dfcluster=c  # le dataframe qui resume tout les cas  de nombre de cluster que le clustering nous propose


    with open('courbepredicte.pkl','rb') as f:
        p=pickle.load(f)
        dfpredic=p   #la courbe qu'on doit predire
    return dff,df_col,dfpredic,dfcluster

#fonction pour definir la ou les courbes à predire
# def datadescluster(df_col,listTags,listDatespredic,cfg):
#
#     dfpredic = cfg.DF_loadTimeRangeTags(['2021-09-27','2021-09-29'],listTags,rs="1800s")
#     if dfpredic.empty:
#         print('vide')
#     else:
#         dfpredic=dfpredic.resample("30min").first()
#
#     return dfpredic


#calcul d'une distance euclidienne pour differents points
def calculdistance(dist1,dist2):
    distance= np.sqrt(np.sum((dist1-dist2)**2))
    return distance

#preparer les datframe contenant les courbes moyennes de chacune
def dfprepare():
    dff,df_col,dfpredic,dfcluster=appelerdataframe()
    dfprediccopie=dfpredic.copy()
    dfclu3=df_col

    dfclu3["cluster"]=dfcluster["cluster3"]
    df0=dfclu3[(dfclu3.cluster=="0")]
    df1=dfclu3[(dfclu3.cluster=="1")]
    df2=dfclu3[(dfclu3.cluster=="2")]

    moyenne0=df0.mean(axis=0)
    moyenne1=df1.mean(axis=0)
    moyenne2=df2.mean(axis=0)
    dfmoyenne=pd.concat([moyenne0,moyenne1,moyenne2], axis=1)
    for j in range(0,len(dfmoyenne.columns)):
        dfmoyenne=dfmoyenne.rename(columns={j:"courbe"+str(j)})

    return dfmoyenne, dfprediccopie

def predictionnaive(tcourant,timewindow,hours2predict,compteur):

    dff,df_col,dfpredic,dfcluster= appelerdataframe()
    dfmoyenne, dfprediccopie=dfprepare()

    plageecart=tcourant+dt.timedelta(hours=timewindow)
    plagepredic=plageecart+dt.timedelta(hours=hours2predict)

    dfpred=dfpredic[(dfpredic.index>=tcourant) &(dfpredic.index<=plageecart)]
    dfpredcopie=dfpred.copy()

    dfpred.index=dfpred.index.strftime('%H:%M:%S')
    dfmoy = dfmoyenne.loc[dfpred.index]

    # calculer les distances et 4. find the min and determine cluster

    dfcourbepredicte=pd.DataFrame()
    distances=pd.DataFrame([calculdistance(dfmoy[k],dfpred[compteur]) for k in dfmoy.columns],index=dfmoy.columns)
    distance=distances.idxmin().iloc[0]
    # clusters.append(distance)

# 5. calcul pred t+timewindow t+14 et 6. select real data t+timewindow t+14

    dfreelle=dfpredic[(dfpredic.index>plageecart)&(dfpredic.index<=plagepredic)]
    dfreellecopie=dfreelle.copy()
    dfreelle.index=dfreelle.index.strftime('%H:%M:%S')

    dfmoypredicte = dfmoyenne.loc[dfreelle.index]
    #
    dfcourbepredicte[distance]=dfmoypredicte[distance]

    # 7.calcul performance diff real pred
    perf=calculdistance(dfcourbepredicte[distance],dfreelle[compteur])


    dfcourbepredicte.index=dfreellecopie.index
    dfcourbepredicte=dfcourbepredicte.resample('1h').first()
    dfcourbepredicte = dfcourbepredicte.iloc[1:,:]
    dfmoy.index=dfpredcopie.index

    return plageecart,distance, perf,dfcourbepredicte

def predictioninitiale(t1,tcourant,timewindow,hours2predict,compteur):
    "#je dois ajouter le parametre compteur quand on aura plusieurs compteur  pour faire une boucle dans le main"
    heures=[]
    clusters=[]
    performances=[]

    dff,df_col,dfpredic,dfcluster= appelerdataframe()
    dfmoyenne, dfprediccopie=dfprepare()

    couleur=couleurs(hours2predict+1,cmap='jet')
    fig=go.Figure() # initialisation de la figure
    fig.add_trace(go.Scatter(x=dfprediccopie.index,y=dfprediccopie[compteur],mode='lines+markers',
                                name='courbe réelle',marker= dict(color= 'black')))
    namesCourbes=['prediction t + ' + str(k) for k in range(1,hours2predict+1)]
    for i,name in enumerate(namesCourbes):
        fig.add_trace(go.Scatter(x=[],y=[],mode='lines+markers',
                            name=name,marker= dict(color= couleur[i+1])))

    # start loop
    while tcourant<=t1-dt.timedelta(hours=timewindow+hours2predict):

        plageecart,distance, perf,dfcourbepredicte= predictionnaive(tcourant,timewindow,hours2predict,compteur)
        heures.append(plageecart)
        clusters.append(distance)
        performances.append(perf)

        for i in range(1,len(namesCourbes)+1):
            fig.data[i]['x']=np.append(fig.data[i]['x'],dfcourbepredicte.index[i-1])

            fig.data[i]['y']=np.append(fig.data[i]['y'],dfcourbepredicte.iloc[i-1,:])

        tcourant+=dt.timedelta(hours=1)

    fig.show()
    # 8.mettre performance temps cluster dans un dataframe
    resume=pd.DataFrame([heures,performances,clusters]).transpose()
    resume.columns =['heure','perfomance','cluster']
       # time.sleep(1)
    # print(tcourant)

    return resume,fig


"prediction intelligente"


    #
