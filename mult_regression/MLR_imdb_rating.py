#importing the libraries
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso
import statsmodels.api as sm
import pyreadr
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import explained_variance_score
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

result = pyreadr.read_r('Movies.RData')# also works for Rds
print(result.keys())
df = pd.DataFrame(result['movies'], columns=result['movies'].keys() )
df.shape

df.shape[0]
df.set_index("title", inplace=True) #setting the index name
df_1 = df.loc[:, ['imdb_rating','genre', 'runtime', 'best_pic_nom',
                  'top200_box', 'director', 'actor1']]

#Let's also check the column-wise distribution of null values
print(df_1.isnull().values.sum())
print(df_1.isnull().sum())

#Dropping missing values from my dataset
df_1.dropna(how='any', inplace=True)
print(df_1.isnull().values.sum()) #checking for missing values after the dropna()

#Splitting for 2 matrices: independent variables used for prediction and dependent variables (that is predicted)
X = df_1.drop(["imdb_rating", 'runtime'], axis = 1)   #Feature Matrix
y = df_1["imdb_rating"] #Dependent Variables

#Treating categorical variables with One-hot-encoding
from sklearn import preprocessing
le = preprocessing.LabelEncoder()


# LabelEncoder for a number of columns
class MultiColumnLabelEncoder:

    def __init__(self, columns = None):
        self.columns = columns # list of column to encode
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''

        output = X.copy()

        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(output[col])
        else:
            for colname, col in output.iteritems():
                output[colname] = LabelEncoder().fit_transform(col)

        return output
    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)

le = MultiColumnLabelEncoder()
X_train_le = le.fit_transform(X)

#From labels to dummy
from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(sparse=False)
X_train_ohe = ohe.fit_transform(X_train_le)

#Treating continous variables with Standart Scaler

columns_to_scale = np.array(df_1['runtime'])
#Initiate Scaler:
scaler = StandardScaler()
scaled_columns  = scaler.fit_transform(columns_to_scale[:, np.newaxis])

# Resulted feature matrix with all of independent variables
X_2 = np.concatenate((scaled_columns,X_train_ohe),axis=1)

from sklearn import linear_model
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X_2, y,test_size = 0.25, random_state = 0)
# Create linear regression object
regr = linear_model.LinearRegression(fit_intercept=False) # Do not use fit_intercept = False if you have removed 1 column after dummy encoding
# Train the model using the training sets
regr.fit(X_train, Y_train)
y_pred = regr.predict(X_test)

#Slope for every predictor
df = pd.DataFrame({'Actual': Y_test.values.flatten(), 'Predicted': y_pred.flatten()})
df.head(25)

from sklearn.metrics import mean_squared_error, r2_score
print("Mean squared error: %.2f"
      % mean_squared_error(Y_test, y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(Y_test, y_pred))
