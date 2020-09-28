from __future__ import print_function
from sklearn.linear_model import Lasso
from sklearn.preprocessing import scale
import numpy as np
import pandas as pd


import warnings
warnings.filterwarnings("ignore")

def get_Xy(Samples, regmask, i):
    regmask = regmask.copy()
    regmask[i] = True
    i = np.count_nonzero(regmask[:i])
    Samples = Samples[regmask, :]
    y = Samples[i, :].T
    X = np.delete(Samples, i, 0).T
    return (X, y)


def get_error(X, y, w):
    y2 = X.dot(w)
    err = ((y - y2) ** 2).sum()
    return err


def get_one_DISCERN_score(X1, y1, w1, X2, y2, w2):
    err11 = get_error(X1, y1, w1)
    err22 = get_error(X2, y2, w2)
    err12 = get_error(X1, y1, w2)
    err21 = get_error(X2, y2, w1)
    base = err11 + err22
    err = err12 + err21
    T4 = err / base
    return T4


def get_DISCERN(Samples1, Samples2, regmask, i, alpha=1, normalize=False):
    (X1, y1) = get_Xy(Samples1, regmask, i)
    (X2, y2) = get_Xy(Samples2, regmask, i)
    cl1 = Lasso(alpha=alpha, normalize=normalize,
                fit_intercept=False, precompute=False)
    cl2 = Lasso(alpha=alpha, normalize=normalize,
                fit_intercept=False, precompute=False)
    cl1.fit(X1, y1)
    cl2.fit(X2, y2)
    return get_one_DISCERN_score(X1, y1, cl1.coef_, X2, y2, cl2.coef_)



def get_all_DISCERN(Samples1, Samples2, regmask, alpha=1, normalize=False):
    assert Samples1.shape[0] == Samples2.shape[0]
    return [get_DISCERN(Samples1, Samples2, regmask, i, alpha, normalize) for i in xrange(Samples1.shape[0])]



if __name__ == '__main__':
    from optparse import OptionParser
    import sys

    usage = "usage: %prog [options] file1 file2"
    parser = OptionParser(usage=usage)
    parser.add_option("-g", "--gene-index", action="store", type="int", dest="gene_index", default=-1)
    parser.add_option("-a", "--alpha", action="store", type="float", dest="alpha", default=0.3)
    parser.add_option("-n", "--normalize", action="store_true", dest="normalize", default=True)
    parser.add_option("-r", "--regulators", action="store", dest="regulators", default="")

    (options, args) = parser.parse_args()

    if len(args) != 2:
        print ("Please supply two input files")
        sys.exit()

    df1 = pd.read_csv(args[0], index_col=0)
    df2 = pd.read_csv(args[1], index_col=0)

    genes1 = df1.index
    genes2 = df2.index

    if not np.all(genes1 == genes2):
        print("Genes should align between two data files")
        sys.exit()

    data1 = np.array(df1)
    data2 = np.array(df2)


    if options.regulators != "":
        regulators = map(str.strip, open(options.regulators, "rt").readlines())
        regmask = np.array([g in regulators for g in genes1], dtype=bool)
    else:
        regmask = np.array([True for g in genes1], dtype=bool)


    if data1.shape[0] != data2.shape[0]:
        print ("Invalid data shape")
        sys.exit()

    alpha = options.alpha
    normalize = options.normalize
    
    if normalize == True:
        data1 = scale(data1.T).T
        data2 = scale(data2.T).T

    gene_index = options.gene_index

    result = {}
    if gene_index >= 0:
        # need to process only one gene
        print(genes1[gene_index], get_DISCERN(data1, data2, regmask, gene_index, alpha=alpha))
    else:
        for i in range(data1.shape[0]):
            #print(genes1[i], get_DISCERN(data1, data2, regmask, i, alpha=alpha))
            result[genes1[i]] = get_DISCERN(data1, data2, regmask, i, alpha=alpha)
    result1 = sorted(result.items(),key=lambda x:x[1],reverse=True)
    important_nodes = []
    with open('important.txt','r') as important:
    	for node in important:
    		node = node.strip('\n')
    		important_nodes.append(node)
    temp = 0 
    for key in result1[0:10]:
    	if str(key[0]) in important_nodes:
    		temp = temp + 1
    print(temp)

