import pandas as pd
import numpy as np
import multiprocessing
import matplotlib.pyplot as plt
from kstar import mapping
import multiprocessing
import itertools
import time


class gsea:
    """
    Class for running KSEA (altered version of GSEA) and analyzing the results
    """
    def __init__(self, network, experiment, data_cols = None, kinase_col = 'Kinase',
            threshold = None, threshold_on = None,
            map_network = False, network_cols = {'peptide': None, 'site': None, 'accession':None},
            map_experiment = False, experiment_cols = {'peptide': None, 'site': None, 'accession':None}, mdir = None):
        
        #save network and experiment
        self.network = network
        self.experiment = experiment

        
        #Treshold the network if thresholding
        if threshold is not None:
            self.network = self.network[self.network[threshold_on] >= threshold]
            self.network.drop([threshold_on], axis = 1, inplace = True)
            print('Network thresholded')
        #if mapping, do so here
        
            
       
        #find overlap between network and experiment
        self.exp_substrates = list(experiment['KSTAR_ACCESSION']+'_'+experiment['KSTAR_SITE'])
        self.net_substrates = list(network['KSTAR_ACCESSION']+'_'+network['KSTAR_SITE'])
        self.site_overlap = list(set(self.exp_substrates).intersection(set(self.net_substrates)))
        
        #find unique kinases
        self.kinases = network[kinase_col].unique()
        
        #extract substrate info for each kinase in the network
        self.ks_info = {}
        for kin in self.kinases:
            tmp_net = network[network[kinase_col] == kin]
            kinase_substrates = list(tmp_net['KSTAR_ACCESSION']+'_'+tmp_net['KSTAR_SITE'])
            self.ks_info[kin] = kinase_substrates
        
        #If data_cols is none, look for columns starting with 'data:'
        if data_cols is None:
            self.data_cols = [col for col in self.experiment.columns if 'data:' in col]
        else:
            self.data_cols = data_cols
            
        #If data columns are given/found, get quantifications, trim to only the sites in network, then aggregate information from rows for same substrate
        if len(self.data_cols) > 0:
            #Get quantifications, trim to only the sites in network, then aggregate information from rows for same substrate
            self.sites = self.experiment[self.data_cols]
            self.sites.index = self.exp_substrates
            self.sites = self.sites.loc[self.site_overlap]
            if len(np.unique(self.sites.index)) < len(self.sites.index):
                self.sites = self.sites.groupby(level = 0).agg('mean')
        else:
            print('No data columns found. Please indicate which columns to use.')

        self.results = {}


        
    def runGSEA_singleKinase(self, kinase_to_test, data_col,p = 1, numTrials = 1000, plotRS = True, returnNull = False, returnRS = False):
        #get quantifications, rank by quantification, drop missing sites
        sites = self.sites[data_col].sort_values(ascending = False)
        sites = sites.dropna()
        
        #get kinase substrate list
        try:
            kinase_set = self.ks_info[kinase_to_test]
        except KeyError:
            print('Provided kinase is not in the network')
        
        signature = list(set(kinase_set).intersection(set(sites.index.values)))
        #check to see if any kinase substrates are found in experiment. If they are not, return None;
        null_time = []
        rs_time = []
        if len(signature) > 0:
            #Get Running Sum 
            RS = getRunningSum(sites,kinase_set, p)
            #Find the enrichment score
            ES = RS[np.where(abs(np.array(RS)) == np.max(abs(np.array(RS))))[0][0]]

            #Find significance of ES
            if returnNull:
                p, null = computeEmpP(sites, kinase_set, p, ES, numTrials = numTrials, returnNull = True)
            else:
                p = computeEmpP(sites, kinase_set, p, ES, numTrials = numTrials, returnNull = False)

            #plot running sum if desired
            if plotRS:
                plotRunningSum(RS)
        else:
            p, ES, RS, null = None, None, None, None
            
        #return results
        
        if returnRS:
            if returnNull:
                return ES, p, RS, null
            else:
                return ES, p, RS
        elif returnNull:
            return ES, p, null
        else:
            return ES, p
        
    def runGSEA_singleExp(self, data_col, p = 1, numTrials = 1000):
 #       if PROCESSES > 1:
 #           pool = multiprocessing.Pool(processes = PROCESSES)
 #           p_exp = itertools.repeat(p, len(self.kinases))
 #           numT = itertools.repeat(numTrials, len(self.kinases))
 #           col = itertools.repeat(data_col, len(self.kinases))
 #           plotRS = itertools.repeat(False, len(self.kinases))
 #           returnNull = itertools.repeat(False, len(self.kinases))
 #           returnRS = itertools.repeat(False, len(self.kinases))
 #           kinases = list(self.kinases)
 #           iterable = zip(kinases, col, p_exp, numT, plotRS, returnNull, returnRS)
 #           result_list = pool.starmap(self.runGSEA_singleKinase, iterable)
 #       else:
        results = pd.DataFrame(None, columns = ['ES','p-value'], index = self.ks_info.keys())
        for kin in self.ks_info.keys():
            results.loc[kin] = self.runGSEA_singleKinase(kin, data_col, p = p, numTrials = numTrials, returnNull = False, returnRS = False, plotRS = False)
        
        results = results.dropna()
        self.results[data_col] = results
        results['Exp'] = data_col
        
        return results
        
    def runGSEA_batch(self, p = 1, numTrials = 1000, PROCESSES = 1):
        if PROCESSES > 1:
            pool = multiprocessing.Pool(processes = PROCESSES)
            p_list = itertools.repeat(p, len(self.data_cols))
            numT = itertools.repeat(numTrials, len(self.data_cols))
            iterable = zip(self.data_cols, p_list, numT)
            results_list = pool.starmap(self.runGSEA_singleExp, iterable)
            return results_list
            #results_ES = pd.DataFrame(columns = self.data_cols, index = self.kinases)
            #results_p = pd.DataFrame(columns = self.data_cols, index = self.kinases)
            #for r in results_list:
            #    data = r['Exp'][0]
            #    kin = np.unique(r.index.values)
            #    results_ES.loc[kin,data] = r.
            #    results_dict[data] = r
        else:
            for col in self.data_cols:
                self.runGSEA_singleExp(col, p = p, numTrials = numTrials, PROCESSES = PROCESSES)
                
    def plotResults(self, name = None, figsize = (10,10)):
        if name is None:
            print('Please indicate which result you would like to plot')
        else:
            cmap = sns.color_palette('colorblind')

            plt.figure(figsize = figsize)
            plot_data = self.results[name].sort_values(by = 'ES', ascending = True).dropna()
            kinases = plot_data.index

            #plot
            bar = plt.barh(kinases, plot_data['ES'], color = cmap[0])

            #color ES with p <= 0.05
            sig_loc = np.where(plot_data['p-value'] <= 0.05)[0]
            for loc in sig_loc:
                bar[loc].set(color = cmap[8])

            xlabel = plt.xlabel('ES')
            
            
    def saveResults(self, odir = '', net_name = None):
        for name in self.results.keys():
            if net_name is None:
                self.results[name].to_csv(f'{odir}/{name}_GSEAresults.tsv', sep = '\t')
            else:
                self.results[name].to_csv(f'{odir}/{name}_{net_name}_GSEAresults.tsv', sep = '\t')
    
            
            




    
    
    

    
    
def thresholdNetworKIN(network, threshold, percentCutoff = None):
    thresholded = network[network['value'] >= threshold]
    if percentCutoff is not None:
        for kin in thresholded['Kinase'].unique():
            tmp = thresholded[thresholded['Kinase'] == kin]
            max_prob = tmp['value'].max()
            remove = tmp[tmp['value'] < (0.9*max_prob)].index.values
            print(max_prob)
            print(remove)
            thresholded = thresholded.drop(remove, axis = 0)

    thresholded.drop(['value'], axis = 1, inplace = True)
    return thresholded
    
def getRunningSum(sites, kinase_set, p = 1, data_label = 'value'):
    #find hits
    hits = [True if s in kinase_set else False for s in sites.index]
    #calculate Nr: this is the absolute sum of all kinase set correlations times some exponent p
    Nr = sum(abs(sites[hits].values)**p)
    #total number of sites in ranked list
    N = sites.shape[0]
    #find the total number of misses
    Nh = sum([int(h) for h in hits])

    runningSum = []
    numSubInSet = 0
    pHit=0
    pMiss=0
    for i in range(sites.shape[0]):
        #add another gene and check if it is in a set
        sub = sites.index[i]
        if sub in kinase_set:
            numSubInSet = numSubInSet + 1
            if Nr != 0:
                pHit = pHit + abs(sites[sub])**p/Nr
        else:
            pMiss = pMiss + 1/(N - Nh)

        ES = pHit - pMiss
        runningSum.append(ES)
    
    return runningSum
   
def computeEmpP(sites, kinase_set, p, actualES, numTrials = 1000, returnNull = False):
    num_hits = sum([1 if s in kinase_set else 0 for s in sites.index])
    #generate random experiments by randomly assigning sites as substrate of kinase
    random_sets = [np.random.choice(sites.index, size = num_hits) for i in range(numTrials)]
    #For each random experiment, calculate the max ES score
    null_dist = []
    for rset in random_sets:
        RS = getRunningSum(sites, rset, p)
        maxLoc = np.where(abs(np.array(RS)) == np.max(abs(np.array(RS))))[0][0]
        null_dist.append(RS[maxLoc])
    
    null_dist = np.array(null_dist)
    #find p-value
    numExp = len(null_dist)
    p = (actualES >= 0) * len(np.where(null_dist >= actualES)[0])/float(numTrials) + (actualES < 0) * len(np.where(null_dist <= actualES)[0])/float(numTrials)
    
    if returnNull:
        return p, null_dist
    else:
        return p
   
def plotRunningSum(RS, title = ''):
    plt.plot(list(range(1,len(RS)+1)),RS, c = 'k', label = 'Running Sum')
    #plot point for where max is
    mes = np.max(abs(np.array(RS)))
    maxLoc = np.where(abs(np.array(RS)) == mes)[0][0]
    mes = RS[maxLoc]
    plt.scatter(maxLoc+1, mes, c = 'r', label = 'ES')
    #label plot
    plt.xlabel('Ranked Substrate Number')
    plt.ylabel('Running Sum Statistic')
    plt.title(title)
    plt.legend()