import pandas as pd
import numpy as np
import powerlaw as pl
import matplotlib.pyplot as plt
import snap

df = pd.read_csv("edgesSeq.txt")
G = snap.LoadEdgeList(snap.PNGraph, "edgesSeq.txt", 0, 1)

def biggest_connected_component_on_the_network():
    WccV = snap.TIntPrV()
    snap.GetWccSzCnt(G, WccV)
    con_comp = {}
    print("Connected components info.\n")
    print("# of connected component", WccV.Len())
    for comp in WccV:
        con_comp[comp.GetVal1()] = comp.GetVal2()
    print("Biggest connected component has size of:", max(con_comp.values()))
    snap.PrintInfo(G, "tweet Information", "tweet_stats_extended.txt", False)

def extended_network_information():
    f = open('tweet_stats_extended.txt', 'r')
    file_contents = f.read()
    print(file_contents)
    f.close()

def nodes_centrality_page_rank():
    PRankH = snap.TIntFltH()
    snap.GetPageRank(G, PRankH)
    sorted_PRankH = sorted(PRankH, key=lambda key: PRankH[key], reverse=True)
    # print top n nodes with highest PageRank
    for item in sorted_PRankH[0:5]: #top 5
        print(item, PRankH[item])

def nodes_centrality_betweeness():
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    snap.GetBetweennessCentr(G, Nodes, Edges, 1.0)
    sorted_Bet = sorted(Nodes, key=lambda key: Nodes[key], reverse=True)
    # print top n nodes with highest Betweeness
    for item in sorted_Bet[0:5]: #top 5
        print(item, Nodes[item])

def nodes_centrality_degree_centrality():
    CloseCentrV = []

    for NI in G.Nodes():
        CloseCentr = snap.GetClosenessCentr(G, NI.GetId())
        CloseCentrV.append((NI.GetId(), CloseCentr))

    def getKey(item):
        return item[1]

    Sorted_CD = sorted(CloseCentrV, key=getKey, reverse=True)
    #print(Sorted_CD[0:5])
    Nodes= [x[0] for x in Sorted_CD]
    Score =[x[1] for x in Sorted_CD]
    for item in Nodes[0:5]: #top 5
        print("Node", Nodes[item], "DC:", Score[item])

def diameter_of_the_network():
    sample = int(len(df)*0.75) #use 75% of the data
    D = snap.GetBfsFullDiam(G, sample)
    print("Diameter", D)
    ED = snap.GetBfsEffDiam(G, sample)
    print("Effective Diameter", ED)
    All_dis = snap.GetBfsEffDiamAll(G, sample, False)
    print("Average Diameter:", All_dis[3])

def innermost_k_shell():
    CoreIDSzV = snap.TIntPrV() # Calcualte the number of nodes in every core
    kValue = snap.GetKCoreNodes(G, CoreIDSzV)
    for item in CoreIDSzV:
        print ("k-core: %d nodes: %d" % (item.GetVal1(), item.GetVal2()))

def clustering_coefficient():
    # Count triads
    Triads = snap.GetTriads(G)
    print("# of triads", Triads)

    # Calculate clustering coefficient
    CC = snap.GetClustCf(G)
    print("clustering coefficient", CC)

def degree_distribution():
    # Get node with max degree
    NId = snap.GetMxDegNId(G)
    print("max degree node", NId)

    # Get degree distribution
    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(G, DegToCntV)
    for item in DegToCntV:
        print("%d nodes with degree %d" % (
            item.GetVal2(), item.GetVal1()))

def degree_stats():
    InDegV = snap.TIntPrV()
    snap.GetNodeInDegV(G, InDegV)
    numItemstoList = 10;
    i = 0;
    for item in InDegV:
        print("node ID %d: in-degree %d" % (item.GetVal1(), item.GetVal2()))
        i = i + 1
        if i == numItemstoList:
            break  # comment to output all nodes

def degree_distribution_graphs():
    InDegV = snap.TIntPrV()
    snap.GetNodeInDegV(G, InDegV)
    a = np.arange(1, snap.CntNonZNodes(G) - snap.CntInDegNodes(G, 0) + 2)
    i = 0
    for item in InDegV:
        if item.GetVal2() > 0:
            i = i + 1
            a[i] = item.GetVal2()

    bars, bins = np.histogram(a, bins=np.arange(1, max(a)))
    plt.hist(bars,bins)
    plt.grid()
    plt.show()

    plt.loglog(bins[0:-1], bars)
    plt.ylabel('# users per degree')
    plt.xlabel('in-degree')
    plt.grid()
    plt.show()

    plt.loglog(bins[0:-1], sum(bars) - np.cumsum(bars))
    plt.ylabel('# users with degree larger or equal than x')
    plt.xlabel('in-degree')
    plt.grid()
    plt.show()

def power_law_fit():
    InDegV = snap.TIntPrV()
    snap.GetNodeInDegV(G, InDegV)
    a = np.arange(1, snap.CntNonZNodes(G) - snap.CntInDegNodes(G, 0) + 2)
    fit = pl.Fit(a)
    pl.plot_pdf(a, color='r')
    fig2 = fit.plot_pdf(color='b', linewidth=2)
    # power-law exponent
    print("Power Law Data\n")
    print("Power Law Exponential:",fit.alpha)
    print("Min value for X:", fit.xmin)
    print("Kolmogorov-Smirnov test:", fit.D)
    # comparison of data and Pl-fits of pdf (blue) and ccdf (red)"
    figCCDF = fit.plot_pdf(color='b', linewidth=2)
    fit.power_law.plot_pdf(color='b', linestyle='--', ax=figCCDF)
    fit.plot_ccdf(color='r', linewidth=2, ax=figCCDF)
    fit.power_law.plot_ccdf(color='r', linestyle='--', ax=figCCDF)
    ####
    figCCDF.set_ylabel(u"p(X),  p(X≥x)")
    figCCDF.set_xlabel(r"in-degree")

def transform_directed_to_undirected():
    GUn = snap.ConvertGraph(snap.PUNGraph, G)
    snap.PrintInfo(GUn, "Tweets UN stats", "Tweets_UN_info.txt", False)
    f = open('Tweets_UN_info.txt', 'r')
    file_contents = f.read()
    #print(file_contents)
    f.close()
    return GUn

def average_degree():
    GUn = transform_directed_to_undirected()
    AverageDegree = GUn.GetEdges() / GUn.GetNodes()  # truncated average degree
    AverageDegreeF = GUn.GetEdges() / float(GUn.GetNodes())
    #print(AverageDegree)
    #print(AverageDegreeF)
    return AverageDegree

def preferential_attachment():
    GUn = transform_directed_to_undirected()
    AverageDegree = average_degree()
    Rnd = snap.TRnd()
    GPA = snap.GenPrefAttach(GUn.GetNodes(), int(AverageDegree), Rnd)
    snap.PrintInfo(GPA, "Tweets PA Stats", "Tweets_PA-info.txt", False)
    f = open('Tweets_PA-info.txt', 'r')
    file_contents = f.read()
    print(file_contents)
    f.close()

def configuration_model():
    GUn = transform_directed_to_undirected()
    GUnDegSeqV = snap.TIntV()
    snap.GetDegSeqV(GUn, GUnDegSeqV)

    Rnd = snap.TRnd()
    GConfModel = snap.GenConfModel(GUnDegSeqV, Rnd)
    snap.PrintInfo(GConfModel, "Tweets ConfModel Stats", "Tweets_ConfModel-info.txt", False)
    f = open('Tweets_ConfModel-info.txt', 'r')
    file_contents = f.read()
    print(file_contents)
    f.close()

def node_rewiring():
    GUn = transform_directed_to_undirected()
    # Node Rewiring
    Rnd = snap.TRnd()
    GRW = snap.GenRewire(GUn, 1000, Rnd)
    snap.PrintInfo(GRW, "Tweets Rewire Stats", "Tweets_Rewire-info.txt", False)

    f = open('Tweets_Rewire-info.txt', 'r')
    file_contents = f.read()
    print(file_contents)
    f.close()

def erdos_renyi():
    GUn = transform_directed_to_undirected()
       # Erdos-Renyi random graph
    GER = snap.GenRndGnm(snap.PNGraph, G.GetNodes(), G.GetEdges())
    snap.PrintInfo(GER, "Tweets Random Stats", "Tweets_Random-info.txt", False)
    GUn.GetEdges()
    f = open('Tweets_Random-info.txt', 'r')
    file_contents = f.read()
    print(file_contents)
    f.close()
