# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/10/29'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import  train_test_split
from sklearn.tree import DecisionTreeClassifier
from matplotlib import pyplot as plt
from sklearn.model_selection import GridSearchCV

def read_dataset(fname):
    # 指定第一行为索引
    data = pd.read_csv(fname,index_col=0)
    # 丢弃无用过的数据
    data.drop(['Name','Ticket','Cabin'],axis=1,inplace=True)
    # 处理性别数据
    data["Sex"] = (data['Sex']=='male').astype('int')
    # 处理登船港口数据
    labels = data['Embarked'].unique().tolist()
    data['Embarked'] = data['Embarked'].apply(lambda n: labels.index(n))
    # 处理缺失数据
    data = data.fillna(0)
    # print(data)
    return data


train = read_dataset('./train.csv')
y = train['Survived'].values
X = train.drop(['Survived'],axis=1).values

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
# print("train_dataset:{};\ntest_data_set{}".format(X_train.shape,X_test.shape))

# 创建决策树分类器实例
# clf = DecisionTreeClassifier()
# clf.fit(X_train,y_train)
# train_score = clf.score(X_train,y_train)
# test_score = clf.score(X_test,y_test)
# print("训练得分：{};\n测试得分：{}".format(train_score,test_score))

def cv_socre(d):
    clf = DecisionTreeClassifier(max_depth=d)
    clf.fit(X_train,y_train)
    tr_score = clf.score(X_train,y_train)
    cv_socre = clf.score(X_test,y_test)
    return tr_score,cv_socre

# depths = range(2,15)
# scores = [cv_socre(d) for d in depths]
# tr_scores = [s[0] for s in scores]
# cv_scores = [s[1] for s in scores]
#
# best_score_index = np.argmax(cv_scores)
# best_socre = cv_scores[best_score_index]
# best_param = depths[best_score_index]
# print('best param:{};\nbest score:{}'.format(best_param,best_socre))
#
# plt.figure(figsize=(6,4),dpi=144)
# plt.grid()
# plt.xlabel('max depth of decision tree')
# plt.ylabel('score')
# plt.plot(depths,cv_scores,'.g-',label='cross-validation score')
# plt.plot(depths,tr_scores,'.r--',label='training score')
# plt.legend()
# plt.show()

def cv_socre_by_gini(val):
    clf = DecisionTreeClassifier(criterion='gini',min_impurity_split=val)
    clf.fit(X_train,y_train)
    tr_score = clf.score(X_train,y_train)
    cv_socre = clf.score(X_test,y_test)
    return tr_score,cv_socre


# cv_socrevalues = np.linspace(0,0.5,50)
# scores = [cv_socre_by_gini(v) for v in values]
# tr_scores = [s[0] for s in scores]
# cv_scores = [s[1] for s in scores]
#
# best_score_index = np.argmax(cv_scores)
# best_socre = cv_scores[best_score_index]
# best_param = values[best_score_index]
# print('best param:{};\nbest score:{}'.format(best_param,best_socre))
#
# plt.figure(figsize=(6,4),dpi=144)
# plt.grid()
# plt.xlabel('max depth of decision tree')
# plt.ylabel('score')
# plt.plot(values,cv_scores,'.g-',label='cross-validation score')
# plt.plot(values,tr_scores,'.r--',label='training score')
# plt.legend()
# plt.show()


def plot_curve(train_size,cv_results,xlabel):
    train_score_mean = cv_results['mean_train_score']
    train_score_std = cv_results['std_train_score']
    test_scores_mean = cv_results['mean_test_score']
    test_scores_std = cv_results['std_test_score']
    plt.figure(figsize=(6, 4), dpi=144)
    plt.grid()
    plt.xlabel('max depth of decision tree')
    plt.ylabel('score')
    plt.fill_between(
        train_size,
        train_score_mean - train_score_std,
        train_score_mean + train_score_std,
        alpha=0.1,
        color= 'r'
    )
    plt.fill_between(
        train_size,
        test_scores_mean - test_scores_std,
        test_scores_mean + test_scores_std,
        alpha=0.1,
        color='g'
    )
    plt.plot(train_size,train_score_mean, '.--', color='r',label = 'Training score')
    plt.plot(train_size, test_scores_mean, '.-', color = 'g',label='Cross-validation score')
    plt.legend(loc='best')
    plt.show()

entropy_thresholds = np.linspace(0,1,50)
gini_thresholds = np.linspace(0,0.5,50)
param_grid = [{'criterion':['entropy'],
               'min_impurity_split': entropy_thresholds},
              {'criterion':['gini'],
               'min_impurity_split':gini_thresholds},
              {'max_depth':range(2,10)},
            {'min_samples_split':range(2,30,2)}]
clf = GridSearchCV(DecisionTreeClassifier(),param_grid,cv=5)
clf.fit(X,y)
print("best param:{}\nbest socre:{}".format(clf.best_params_,clf.best_score_))
plot_curve(thresholds,clf.cv_results_,xlabel='gini thresholds')
