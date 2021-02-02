import numpy as np

def tail_body_likelihood(params, *args):

    l, alpha, xmin = params
    #print(l)
    C = 2- np.exp(-l*xmin)
    L = 0
    r = sorted(args[1])
    pen = args[0]
    selection = [value for value in r if value < xmin]
    f = len(selection)
    #Compute log-likelihood values for the body of the distribution 
    for i in range(f):
        L = L - np.log(C) + np.log(l) - l*r[i]
    for i in range(f+1, len(r)):
        L = L - np.log(C) + np.log(alpha / xmin) - (alpha+1)*np.log(r[i]/xmin)
    
    fbody = l* np.exp(-l*xmin)/C
    ftail = alpha/(C*xmin)

    L = L-pen*(fbody-ftail)**2
    return -L