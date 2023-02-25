import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def get_prediction(model, x_test, y_test, name):
    prediction = model.predict(x_test)

    print(name, 'x coefficients: ', model.coef_)
    print(name, 'coefficient of determination: %.2f' % r2_score(y_test, prediction), '\n')
    return prediction


column_names = ['complexAge', 'totalRooms', 'totalBedrooms', 'complexInhabitants', 'apartmentsNr', 'medianComplexValue']
raw_dataset = pd.read_csv("normalized.csv", names=column_names)

x = raw_dataset[['complexAge', 'totalRooms', 'totalBedrooms', 'complexInhabitants', 'apartmentsNr', ]].values
y = raw_dataset['medianComplexValue'].values
sns.pairplot(raw_dataset[column_names], diag_kind='kde', height=1.5, plot_kws=dict(s=1))
plt.show()

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)

# 4 different models
lr_model = linear_model.LinearRegression()
lr_model.fit(x_train, y_train)
lr_pred = get_prediction(lr_model, x_test, y_test, 'LinearRegression')

en_model = linear_model.ElasticNet(random_state=1)
en_model.fit(x_train, y_train)
en_pred = get_prediction(en_model, x_test, y_test, 'ElasticNet')

ls_model = linear_model.Lasso(random_state=1)
ls_model.fit(x_train, y_train)
ls_pred = get_prediction(ls_model, x_test, y_test, 'Lasso')

rd_model = linear_model.Ridge(random_state=1)
rd_model.fit(x_train, y_train)
rd_pred = get_prediction(rd_model, x_test, y_test, 'Ridge')

# Plot
figure, axis = plt.subplots(2, 2)
figure.set_figwidth(15)
figure.set_figheight(7)

lims = [0, 500000]

axis[0, 0].scatter(y_test, lr_pred, s=1)
axis[0, 0].set_title("LinearRegression")
axis[0, 0].set_xlim(lims)
axis[0, 0].set_ylim(lims)

axis[0, 1].scatter(y_test, en_pred, s=1)
axis[0, 1].set_title("ElasticNet")
axis[0, 1].set_xlim(lims)
axis[0, 1].set_ylim(lims)

axis[1, 0].scatter(y_test, ls_pred, s=1)
axis[1, 0].set_title("Lasso")
axis[1, 0].set_xlim(lims)
axis[1, 0].set_ylim(lims)

axis[1, 1].scatter(y_test, rd_pred, s=1)
axis[1, 1].set_title("Ridge")
axis[1, 1].set_xlim(lims)
axis[1, 1].set_ylim(lims)

plt.show()
