import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from mpl_toolkits.mplot3d import Axes3D
data = pd.read_csv("datosproyecto1", index_col=0)
titulos= list(data.columns[:-1])
titulos.remove("date")
titulos.remove("quarter")
titulos.remove("department")
titulos.remove("day")
features = titulos
X = data[features]
y = data.actual_productivity
X = data[features]
y = data.actual_productivity
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
X_train = sm.add_constant(X_train)
model = sm.OLS(y_train, X_train).fit()
import numpy as np
xx_pred, yy_pred = np.meshgrid(X_test, y_test)
model_viz = np.array([xx_pred.flatten(), yy_pred.flatten()]).T
predicted = model.predict(model_viz)

ejex = data[['incentive', 'over_time']].values.reshape(-1,2)
ejey = data['actual_productivity']


xx = ejex[:, 0]
yy = ejex[:, 1]
zz = ejey

r2 = 1


plt.style.use('default')

fig = plt.figure(figsize=(12, 4))

ax1 = fig.add_subplot(131, projection='3d')
ax2 = fig.add_subplot(132, projection='3d')
ax3 = fig.add_subplot(133, projection='3d')

axes = [ax1, ax2, ax3]

for ax in axes:
    ax.plot(xx, yy, zz, color='k', zorder=15, linestyle='none', marker='o', alpha=0.5)
    ax.scatter(xx_pred.flatten(), yy_pred.flatten(), predicted, facecolor=(0,0,0,0), s=20, edgecolor='#70b3f0')
    ax.set_xlabel('Productiviy (%)', fontsize=12)
    ax.set_ylabel('incentive', fontsize=12)
    ax.set_zlabel('Over time', fontsize=12)
    ax.locator_params(nbins=4, axis='x')
    ax.locator_params(nbins=5, axis='x')

ax1.text2D(0.2, 0.32, '', fontsize=13, ha='center', va='center',
           transform=ax1.transAxes, color='grey', alpha=0.5)
ax2.text2D(0.3, 0.42, '', fontsize=13, ha='center', va='center',
           transform=ax2.transAxes, color='grey', alpha=0.5)
ax3.text2D(0.85, 0.85, '', fontsize=13, ha='center', va='center',
           transform=ax3.transAxes, color='grey', alpha=0.5)

ax1.view_init(elev=27, azim=112)
ax2.view_init(elev=16, azim=-51)
ax3.view_init(elev=60, azim=165)

fig.suptitle('$R^2 = %.2f$' % r2, fontsize=20)

fig.tight_layout()