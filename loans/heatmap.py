import seaborn as sns
import matplotlib.pyplot as plt

def heatmap(data,figsize=(8,8), annot=True):
    #plot heatmap to find multicollinearity
    plt.figure(figsize=figsize)
    cmap = sns.diverging_palette(220, 20, sep=20, as_cmap=True)
    sns.heatmap(data.corr(),vmin=-0.75,vmax=0.75,center=0, cmap=cmap,annot=annot, fmt='.1f')



