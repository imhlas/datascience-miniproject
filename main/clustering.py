from kmodes.kprototypes import KPrototypes
from kneed import KneeLocator
    
def elbow(data,cat):
    """
    Tests the accuracy of different number of clusters.
    
    Parameters:
    - data (Pandas dataframe)
    - cat (list): Specifies which columns in the cleaned data consist of categorical values. In this case [0,1,2,3]
    
    Returns:
    - costs (dict): Consisting of the elbow scores for each number of clusters.
    """
    
    print("Fitting models with k = ",end="",flush=True)
    costs={}
    for num_clusters in list(range(2,10)):
        print(num_clusters,end=", ",flush=True)
        kproto = KPrototypes(n_clusters=num_clusters, init='Cao')
        kproto.fit_predict(data, categorical=cat)
        costs[num_clusters] = kproto.cost_
    return costs

def chooseK(data, cat):
    """
    Function that uses the ready-made kneed package to calculate the optimal value of clusters

    Parameters:
    - data (Pandas dataframe)
    - cat (list): Specifies which columns in the cleaned data consist of categorical values. In this case [0,1,2,3]
    
    Returns:
    - K (int): optimal number of clusters
    """
    
    costs = elbow(data,cat)
    
    cost_knee_c3 = KneeLocator(
            x=list(costs.keys()), 
            y=list(costs.values()), 
            curve="convex", 
            direction="decreasing")

    K = cost_knee_c3.elbow   
    print("elbow at k =", K, "clusters")
    return K
     
def cluster(data,cat,K=0):
    """
    Function that first removes the empty rows from the clean data and then uses the KPrototypes function to cluster the data.
    
    Parameters:
    - data (Pandas dataframe)
    - cat (list): Specifies which columns in the cleaned data consist of categorical values. In this case [0,1,2,3]
    - K (int): Optimal number of clusters, if 0 calls the chooseK function.
    
    Returns:
    - data_with_clusters (Pandas dataframe): same as data, but now it contains column "clusters" with int values indicating to which cluster the row belongs.
    """
    
    df=data.copy()
    
    # Removing rows with not enough data
    df["Totals"]=df["Frequent drinkers"]+df["Non-drinkers"]+df["Occasional drinkers"]
    df=df[df["Totals"]>99]
    df=df.drop(["Totals"],axis=1)
    
    if K==0:
        K=chooseK(df,cat)

    kproto = KPrototypes(n_clusters=K, init='Cao')
    clusters=kproto.fit_predict(df, categorical=cat)
    
    cluster_dict =[]
    for c in clusters:
        cluster_dict.append(c)
        
    data_with_clusters = df.copy()
    data_with_clusters['clusters'] = cluster_dict
    
    return data_with_clusters, K
    