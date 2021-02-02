import numpy as np



def bootstrap(log_data, tail, p):
    #Bootstrap analysis 
    p = p
    fraction = 0.8 #Fraction of data to be retained in each bootstrap sample
    n_samples = 500 #number of bootstrap samples

#Right tail with bootstrapping
    ci_samples = []

    if tail == 'right':
        for _ in range(n_samples):
            r_fraction = log_data[np.random.permutation(len(log_data))]
            r_fraction = r_fraction[:round(fraction*len(r_fraction))]
            r_fraction = sorted(r_fraction)
            r_right_fraction = r_fraction[round((1-p)*len(r_fraction)):]

            n_infraction = len(r_right_fraction)
            ci_samples.append(n_infraction/np.sum(np.log(r_right_fraction/min(r_right_fraction))))

        #ci_samples = sorted(ci_samples)
    if tail == 'left':

        for _ in range(n_samples):
            r_fraction = log_data[np.random.permutation(len(log_data))]
            r_fraction = r_fraction[:round(fraction*len(r_fraction))]
            r_fraction = sorted(r_fraction)
            r_left_fraction = [abs(value) for value in r_fraction[:round(p*len(r_fraction))]]

            n_infraction = len(r_left_fraction)
            ci_samples.append(n_infraction/np.sum(np.log(r_left_fraction/min(r_left_fraction))))

        #ci_samples = sorted(ci_samples)
    return sorted(ci_samples)



