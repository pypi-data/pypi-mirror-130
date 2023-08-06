import pandas as pd
import numpy as np
import sklearn.metrics as sm
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import datasets
from screeningBuilding.configFilesBuilding import ConfigFilesBuilding
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import StandardScaler,normalize
from matplotlib.cm import register_cmap
from scipy import stats
from plotly.validators.scatter.marker import SymbolValidator

from plotly.subplots import make_subplots
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from yellowbrick.cluster import KElbowVisualizer
from pylab import cm
import matplotlib.colors as mtpcl
from sklearn.cluster import DBSCAN
from sklearn import metrics
import re


" cette fonction retourne les DataFrame que j'utiliserais au courant de mon programme qui retourne dff donc les enregistrements sont le temps et df_col donc les enregistrements sont les compteurs en jours "
def getData(listDates,listTags,cfg):
    dfs =[]
    # df1.resample('1s').apply(np.trapz)
    for j in listDates:
        for compt in listTags:
            df = cfg.DF_loadTimeRangeTags([j+' 00:00',j+' 23:59'],[compt],rs="1800s")
            # print("j",j)
            if df.empty:
                print("df est vide")
            else:
                df.columns = df.columns + '_' + j
                df=df.resample("30min").first()

                df.index = pd.to_datetime(df.index).strftime('%H:%M:%S') #si tu veux pas changer le type des dates sur les données , commentez cette ligne
                dfs.append(df)

    dff=pd.concat(dfs,axis=1)
    dff=dff.ffill().bfill()
    columns = [i for i in dff.columns if i.startswith('time')]
    sub_l1 = [i for i in dff.columns if i.startswith('tag')]
    sub_l2 = [i for i in dff.columns if i.startswith('value')]


    if set(columns).issubset(dff.columns):
        dff.drop(columns,inplace=True,axis=1)
    if set(sub_l1).issubset(dff.columns):
        dff.drop(sub_l1,inplace=True,axis=1)
    if set(sub_l2).issubset(dff.columns):
        dff.drop(sub_l2,inplace=True,axis=1)
    colonne=["C00000001-A003-1-kW sys-JTW_2021-05-18"]
    if set(colonne).issubset(dff.columns):
        del dff["C00000001-A003-1-kW sys-JTW_2021-05-18"]
    colonne1=['C00000003-B001-3-kW sys-JTW_2021-05-18']
    if set(colonne1).issubset(dff.columns):
        del dff['C00000003-B001-3-kW sys-JTW_2021-05-18']


    dff=dff.sort_index()
    df_col = dff.transpose().ffill().bfill()



    return df_col,dff,dfs

" fonction pour les couleurs"
"N: nbre de couleurs que cous vouler "
def couleurs(N,cmap='jet'):
    c=cm.get_cmap(cmap,N)
    colors= [mtpcl.rgb2hex(c(k)) for k in range(c.N)]
    return colors


def representationdesdonnees(dff):
    colors=couleurs(len(dff.columns),cmap='jet')
    w=2850
    fig=px.scatter(dff, color_discrete_sequence=colors)
    fig.update_traces(mode="lines+markers")
    fig.write_image('repredonnees.png',width=w,height=w*.3,format='png')
    fig.show()
    return fig


"PARTIE DU CLUSTERING "


"fonction fait appel a la librairie de la PCA appliquée sur le dataframe df_col pour pourvoir reduire le nbre de dimension"

def pcadimension(df_col):
    pca=PCA()
    pca.fit(df_col)
    x_reduit=[]

    pcadim=[]
    for i in range(2,6):
         pca_=PCA(i)
         pca_.fit(df_col)
         pcadim.append(pca_)
         x_redui=pca_.fit_transform(df_col)
         x_redui=pd.DataFrame(x_redui)

         for j in range(0,len(x_redui.columns)):
             x_redui=x_redui.rename(columns={j:"p"+str(j+1)})
         x_reduit.append(x_redui)

    # pca_2=PCA(2)
    #
    # pca2_fit=pca_2.fit(df_col)
    # pca_fit =pca.fit(df_col)
    #
    # pca_transf=pca2_fit.transform(df_col)
    return pca,pcadim,x_reduit

"reconstruction de notre dataframe avec la pca qui nous permet de voir dans differnte dimension "


def reconstructionendim2(dff,df_col):

    pca,pcadim,x_reduit=pcadimension(df_col)

    dff=dff.copy()
    dfreconstruct=pcadim[0].inverse_transform(x_reduit[0])
    pd.DataFrame(dfreconstruct)
    pd.DataFrame(dfreconstruct).transpose()
    pd.DataFrame(dfreconstruct).transpose().columns
    dfreconstruct=pd.DataFrame(dfreconstruct).transpose()
    dfreconstruct.columns = dff.columns
    # #
    dffplot=dff.melt()
    dffplot['recontruct']=False
    dfreconplot=dfreconstruct.melt()
    dfreconplot['reconstruct']=True
    dffplot.columns=['variable','value','reconstruct']
    dfreconplot.columns=['variable','value','reconstruct']
    dff["temps"]=dff.index
    df2=pd.DataFrame(dff["temps"])
    dftemps=[]
    for i in range(1,len(dff)+1):
        dftemps.append(df2)
    dftemps=pd.concat(dftemps,axis=1)
    dftemps=dftemps.melt()
    dfreconplot["temps"]=dftemps["value"]
    dffplot["temps"]=dftemps["value"]

    dffinal=pd.concat([dffplot,dfreconplot])

    dffinal["compteurs"]=0
    dffinal['jour']=0
    dffinal['compteurs']=[k.split('-')[1] for k in dffinal['variable']]
    dffinal['jour']=[k.split('_')[1] for k in dffinal['variable']]

    return dffinal
def graphereconstructiondim2(dffinal,**kwargs):
    w=1000
    fig=px.line(dffinal,x="temps",y='value',facet_col='jour',color='reconstruct',**kwargs)
    fig.update_yaxes(matches=None)
    fig.update_xaxes(matches=None)
    fig.update_layout(title_text="ANALYSE EN COMPOSANTES PRINCIPALES en dimension 2 ")
    fig.show()
    fig.write_image('reconstitution2.png',width=w,height=w*.3,format='png')
    return fig

def reconstructionendim3(dff,df_col):

    pca,pcadim,x_reduit=pcadimension(df_col)

    dff=dff.copy()
    dfreconstruct=pcadim[1].inverse_transform(x_reduit[1])
    pd.DataFrame(dfreconstruct)
    pd.DataFrame(dfreconstruct).transpose()
    pd.DataFrame(dfreconstruct).transpose().columns
    dfreconstruct=pd.DataFrame(dfreconstruct).transpose()
    dfreconstruct.columns = dff.columns
    # #
    dffplot=dff.melt()
    dffplot['recontruct']=False
    dfreconplot=dfreconstruct.melt()
    dfreconplot['reconstruct']=True
    dffplot.columns=['variable','value','reconstruct']
    dfreconplot.columns=['variable','value','reconstruct']
    dff["temps"]=dff.index
    df2=pd.DataFrame(dff["temps"])
    dftemps=[]
    for i in range(1,len(dff)+1):
        dftemps.append(df2)
    dftemps=pd.concat(dftemps,axis=1)
    dftemps=dftemps.melt()
    dfreconplot["temps"]=dftemps["value"]
    dffplot["temps"]=dftemps["value"]

    dffinal=pd.concat([dffplot,dfreconplot])

    dffinal["compteurs"]=0
    dffinal['jour']=0
    dffinal['compteurs']=[k.split('-')[1] for k in dffinal['variable']]
    dffinal['jour']=[k.split('_')[1] for k in dffinal['variable']]
    return dffinal

def graphereconstructiondim3(dffinal,**kwargs):
    w=1000
    fig=px.line(dffinal,x="temps",y='value',facet_col='jour',color='reconstruct',**kwargs)
    fig.update_yaxes(matches=None)
    fig.update_xaxes(matches=None)
    fig.update_layout(title_text="ANALYSE EN COMPOSANTES PRINCIPALES en dimension 3 ")
    fig.show()
    fig.write_image('reconstitution3.png',width=w,height=w*.3,format='png')
    return fig


"representation des compossantes principales "
"Maintenant, l'ACP crée essentiellement autant de composantes principales qu'il y a de caractéristiques dans nos données"
"En substance, l'ACP a appliqué une transformation linéaire à nos données, ce qui a créé de nouvelles variables. Maintenant, certaines "
"d entre elles contiennent une grande partie de la variance,tandis que d autres - presque aucune. "
"Ensemble, ces  composantes expliquent 100% de la variabilité des données - c'est pourquoi si vous additionnez tous les chiffres que vous voyez, vous obtiendrez 1"
def compoprincipale(df_col):

    pca,pcadim,x_reduit=pcadimension(df_col)

    # pourcentage de la variance expliquée pour chaque composantes
    print('variance expliquée pour chaque composantes: %s' % str(pca.explained_variance_ratio_))
    h=850
    pca_variance = pca.explained_variance_ratio_
    pca_variance_df=pd.DataFrame()
    pca_variance_df['Rapport de variance']= pca_variance
    pca_variance_df['Composantes principales']= np.arange(len(pca_variance))

    fig=px.bar(pca_variance_df,x= "Composantes principales", y="Rapport de variance")
    fig.update_layout(title_text="variance expliquée")
    fig.write_image('composanteprincipale.png',width=h,height=h,format='png')
    fig.show()
    return fig

"pour trouver le nbres de clusters qui peut en ressprtir de cest donnes en utilisant "
"WCSS (somme des carrés des distances des points de données)"
"le point du coude est celui du nombre de clusters à partir duquel la variance ne se réduit plus significativement. "
"En effet, la “chute” de la courbe de variance  (distortion) entre 1 et 3 clusters est "
"significativement plus grande que celle entre 5 clusters et 9 clusters."

def nbrecluster(df_col):

    pca,pcadim,x_reduit=pcadimension(df_col)
    #avec une pca
    wcss = []
    for i in range(1,11):
       model = KMeans(n_clusters = i, init = "k-means++", random_state = 42)
       model.fit(x_reduit[0])
       wcss.append(model.inertia_)

    wcss_pcadf=pd.DataFrame()
    wcss_pcadf["cluster"]=range(1, 11)
    wcss_pcadf["inertia"]=wcss

#sur les donnees brutes

    kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, }

    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(df_col)
        sse.append(kmeans.inertia_)

    wcss_df=pd.DataFrame()
    wcss_df["cluster"]=range(1, 11)
    wcss_df["inertia"]=sse

    w=850
    fig1=px.line(wcss_df, x="cluster",y="inertia")
    # fig1.update_layout(title_text="choix du cluster sur les donnéesdf_col")
    title1="choix du cluster sur les donnéesdf_col"
    fig2=px.line(wcss_pcadf,x="cluster",y="inertia")
    # fig2.update_layout(title_text="choix du cluster dur les données de la pca")
    title2="choix du cluster dur les données de la pca"
    trace1=fig1['data'][0]
    trace2=fig2['data'][0]
    fig=make_subplots(rows=1, cols=2, subplot_titles=(title1,title2),specs=[[{"type": "xy"}, {"type": "xy"}]])
    fig.add_trace(trace1,row=1,col=1)
    fig.add_trace(trace2,row=1,col=2)
    fig.write_image('nbrecluster.png',width=w*1.5,height=w,format='png')
    fig.show()
    return fig

def profitssimiliaires(df_col):

    pca,pcadim,x_reduit=pcadimension(df_col)

    # x_reduit=[x_reduit[0],x_reduit[1]]
    w=850
    labels=[k.split('_')[1] for k in df_col.index]
    fig1= px.scatter(x_reduit[0], x='p1',y='p2',text=labels,log_x=True, size_max=50)
    fig1.update_traces(textposition='top center')
    title1="ACP rapprochant des profils d'évolution similaires en dim 2"
    title2="ACP rapprochant des profils d'évolution similaires en dim 3"
    fig1.update_layout(height=1000, title_text=title1)
    fig2= px.scatter_3d(x_reduit[1], x='p1',y='p2',z='p3',text=labels,log_x=True, size_max=50)
    fig2.update_traces(textposition='top center')
    fig2.update_layout(height=1000, title_text=title2)
    trace1=fig1['data'][0]
    trace2=fig2['data'][0]
    fig=make_subplots(rows=1, cols=2, subplot_titles=(title1,title2)
                                        ,specs=[[{"type": "xy"}, {"type": "scene"}]])
    fig.add_trace(trace1,row=1,col=1)
    fig.add_trace(trace2,row=1,col=2)
    # fig.update_traces(log_x=True)
    # fig.update_traces(marker_size=5,mode='markers')
    # fig.add_trace(trace2,row=1,col=2)
    fig.write_image('profitsimiliaire.png',width=w*1.5,height=w,format='png')
    fig.show()

    return fig


"La simulation de Monte-Carlo est une méthode d’estimation d’une quantité numérique qui utilise des nombres aléatoires."
"appliquons l'algorithme du kmeans sur les données brutes et les données de la pca"

def clusterappliquerpca(df_col):

    pca,pcadim,x_reduit=pcadimension(df_col)

     #on prend cluster=2

    choixcluster=[2,3,4,5,6,7,8,9]
    x=len(choixcluster)
    w=1000
    x_reduit=[x_reduit[0],x_reduit[1]]
    tab_xreduit=[]
    moyennetotale=[]
    moyennetotale3=[]
    silhouettes=[]
    tab_barycentre=[]
    dfhist=pd.DataFrame()
    noms=[]
    for indice in range(len(x_reduit)):
        # print("reduit",indice)
        for nbrecluster in choixcluster:

            for i in range(1,300):
                # print("cluster",nbrecluster)
                # print("i",i)
                kmeans=KMeans(n_clusters=nbrecluster)
                kmeans.fit(x_reduit[indice])
                labels= kmeans.labels_
                y_kmeans_pca=kmeans.fit_predict(x_reduit[indice])
                centers_pca=kmeans.cluster_centers_
                x_reduit[indice]["cluster"]=labels
                x_reduit[indice]=x_reduit[indice].astype({'cluster':'string'})
                silhouette= metrics.silhouette_score(x_reduit[indice], labels, metric="sqeuclidean")

                silhouettes.append(silhouette)
                #print("moyenneintermediare",silhouettes)
                moyenne=np.mean(silhouettes)
            # print('moyenne',moyenne)

            moyennetotale.append(round(moyenne,3))


            if indice ==0:
                fig=px.scatter(x_reduit[indice],x='p1',y= 'p2', color="cluster",title= str(nbrecluster)+" clusters sur les données de la pca à 2 composantes avec pour silhouette"+ str(moyenne ))
                fig.add_trace(go.Scatter(x=centers_pca[:,0],y=centers_pca[:,1],name='barycentre',marker_symbol='cross',marker_color='black'))
                fig.update_traces(marker_size=10,mode='markers')
                fig.write_image('cluster'+str(nbrecluster)+"dim"+str(indice+2)+'.png',width=w,height=w*.6,format='png')
                # fig.show()
            if indice ==1:
                fig=px.scatter_3d(x_reduit[indice],x='p1',y= 'p2',z='p3', color="cluster",title=str(nbrecluster)+" clusters pour les connées de la pca à 3 composantes avec pour silhouette"+ str(moyenne ) )
                fig.add_trace(go.Scatter3d(x=centers_pca[:,0],y=centers_pca[:,1],z=centers_pca[:,3],name='barycentre',marker_symbol='cross',marker_color='black'))
                # fig.update_layout(height=1000, title_text=title2)
                fig.update_traces(marker_size=10,mode='markers')
                fig.write_image('cluster'+str(nbrecluster)+"dim"+str(indice+2)+'.png',width=w,height=w*.6,format='png')
                # fig.show()
            a=silhouettes
            tab_sil=np.array_split(a,len(choixcluster)*2)
            dfhist=pd.DataFrame(tab_sil).transpose()
            c="silhouette"+str(nbrecluster)+"dim"+str(indice+2)
            noms.append(c)
    dfhist.columns=[noms]
    dfhist=dfhist.melt(var_name='nomsilhouette',value_name='silhouette')
    fig1=px.histogram(dfhist,nbins=30,facet_col="nomsilhouette",facet_col_wrap=4)
    fig1.update_layout( title="histogramme des silhouette pour chaque cluster"+ str(moyennetotale))
    fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig1.write_image('histsilhpca.png',width=w,height=w*.6,format='png')
    fig1.show()


def algoithmekmeans(df_col,listTags):

    choixcluster=[2,3,4,5,6,7,8,9]
    dictcluster={}
    similar=[]
    silhouettes=[]
    moytotale=[]
    dfhist=pd.DataFrame()
    df2=df_col.copy()
    noms=[]
    for nbrecluster in choixcluster:
        for i in range(1,300):

            # print("cluster:",nbrecluster)
            kmeans = KMeans(n_clusters=nbrecluster)
            model = kmeans.fit(df2)
            cluster_map = pd.DataFrame()
            cluster_map['data_index'] = df2.index.values
            cluster_map['cluster'+str(nbrecluster)] = model.labels_
            centers = model.cluster_centers_
            df2["cluster"+str(nbrecluster)]= model.labels_
            df2=df2.astype({'cluster'+str(nbrecluster):'string'})

            # unique_clusters = cluster_map['cluster'+str(nbrecluster)].unique()
            silhouette= metrics.silhouette_score(df2, model.labels_, metric="sqeuclidean")
            silhouettes.append(silhouette)

            moyenne=np.mean(silhouettes)
        moytotale.append(round(moyenne,3))
        a=silhouettes
        tab_sil=np.array_split(a,len(choixcluster))
        dfhist=pd.DataFrame(tab_sil).transpose()
        c="silhouette"+str(nbrecluster)
        noms.append(c)
    dfhist.columns=[noms]

    return df2,dfhist,moytotale

def representationkmeansdonnes(dff,df_col,listTags):

    raw_symbols = SymbolValidator().values
    df2,dfhist,moytotale=algoithmekmeans(df_col,listTags)
    # xx=[1800*k for k in range(0,len(dff))]
    w=1000
    somme=dff.apply(np.trapz,args=(None,1800)) #pour calculer l'integrale de la courbe avce un pas de 30min constant
    df2["somme"]=somme
    dffig=df2
    dffig['jour']=dffig.index
    labels=[k.split('_')[1] for k in dffig["jour"]]
    dffig["jour"]=labels
    sub_l = [i for i in dffig.columns if i.startswith('cluster')]
    sub_l.append('jour')
    sub_l.append('somme')
    dffig=dffig.melt(id_vars=sub_l).set_index('timestampUTC')
    dffig=dffig.melt(id_vars=['jour','value','somme'],var_name='nbclust',value_name='cluster',ignore_index=False)
    dfhist=dfhist.melt(var_name='silhouette')
    #representer les données par chaque nbre de clusters
    w=1000
    fig=px.scatter(dffig,x=dffig.index,y='value',color='cluster',facet_col="nbclust",symbol='jour',facet_col_wrap=4)
    fig.update_traces(mode='lines')
    # ,symbol_sequence=raw_symbols[2::3]
    fig.update_layout( showlegend=False, title='choix du nombre de cluster sur kmeans appliqué sur mes données avec pour silhouette'+ str(moytotale))
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.write_image('kmeansdf_col.png',width=w,height=w*.6,format='png')

    # fig.show()

    "étant donné une entrée particulière, produira toujours la même sortie, avec la machine sous-jacente passant toujours par la même séquence d'états"

    #representer les histogramme de silhouettes
    fig1=px.histogram(dfhist,nbins=30,facet_col="silhouette",facet_col_wrap=4)
    fig1.update_layout( title="histogramme pour montrer l'evolution des silhouette pour chaque cluster"+ str(moytotale))
    fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig1.write_image('histsilh.png',width=w,height=w*.6,format='png')
    # fig1.show()

    #representation des histogramme de la consommation energique en foction des clusters
    fig3=px.histogram(dffig,x="somme",color='cluster',facet_col='nbclust',facet_col_wrap=4,nbins=30,barmode="overlay")
    fig3.update_layout(title='histogramme  pour consommation energetique pour  chaque cluster')
    fig3.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig3.write_image('histcluster.png',width=w,height=w*.6,format='png')
    fig3.show()

    return fig,fig1,fig3



    # return dfcluster
