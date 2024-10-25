from kmodes.kprototypes import KPrototypes
from kneed import KneeLocator
    
def elbow(data,cat):
    print("Fitting models with k = ",end="",flush=True)
    costs={}
    for num_clusters in list(range(2,10)):
        print(num_clusters,end=", ",flush=True)
        kproto = KPrototypes(n_clusters=num_clusters, init='Cao')
        kproto.fit_predict(data, categorical=cat)
        costs[num_clusters] = kproto.cost_
    return costs

def chooseK(data, cat):
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
    