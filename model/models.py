import sys
sys.path.append('..')

import lightgbm as lgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from cleansing.data_cleansing import preprocess_data, ros_preprocess_data, oss_preprocess_data
import catboost as cb
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
import numpy as np

X_train, X_test, y_train, y_test = preprocess_data()

def LGBMmodel():
    # LightGBM 데이터셋으로 변환
    lgb_train = lgb.Dataset(X_train, label=y_train)
    lgb_eval = lgb.Dataset(X_test, label=y_test, reference=lgb_train)

    # LightGBM 모델 설정
    params = {
        'objective': 'regression',
        'metric': ['rmse', 'mae'], # 'set' 대신 'list'로 변경
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'max_depth': 6,
        'min_child_weight': 0.1,
        'verbosity': -1
    }

    # 모델 학습
    num_round = 100
    bst = lgb.train(params, lgb_train, num_round, valid_sets=[lgb_train, lgb_eval], early_stopping_rounds=10, verbose_eval=0)

    # 모델 예측
    y_pred_lgb = bst.predict(X_test, num_iteration=bst.best_iteration)

    # 예측값과 실제값의 MSE 계산
    mse = mean_squared_error(y_test, y_pred_lgb)
    print("LightGBM MSE:", mse)

    return y_pred_lgb

def CatBoostModel():
    # CatBoost 데이터셋으로 변환
    cb_train = cb.Pool(X_train, label=y_train)
    cb_eval = cb.Pool(X_test, label=y_test)

    # 모델 학습
    model = cb.CatBoostRegressor(
        loss_function='RMSE',
        eval_metric='RMSE',
        learning_rate=0.05,
        iterations=1000,
        depth=6,
        l2_leaf_reg=3,
        random_seed=42
    )
    model.fit(cb_train, eval_set=cb_eval, early_stopping_rounds=10, verbose=0, plot=True)

    # 모델 예측
    y_pred_cb = model.predict(X_test)

    # 예측값과 실제값의 MSE 계산
    mse = mean_squared_error(y_test, y_pred_cb)
    print("CatBoost MSE:", mse)

    return y_pred_cb

def LRModel():
    # 선형 회귀 모델 학습 및 예측
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)

    mse = mean_squared_error(y_test, lr_pred)
    
    print("Linear Regression MSE:", mse)

    return lr_pred

def RidgeModel():
    # Ridge 회귀 모델 학습 및 예측
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train, y_train)
    ridge_pred = ridge.predict(X_test)

    mse = mean_squared_error(y_test, ridge_pred)
    
    print("Ridge Regression MSE:", mse)

    return ridge_pred

def LassoModel():
    # Lasso 회귀 모델 학습 및 예측
    lasso = Lasso(alpha=0.1)
    lasso.fit(X_train, y_train)
    lasso_pred = lasso.predict(X_test)
    print("Lasso Regression 학습 완료.")

    mse = mean_squared_error(y_test, lasso_pred)
    
    print("Ridge Regression MSE:", mse)

    return lasso_pred

def EnetModel():
    # ElasticNet 회귀 모델 학습 및 예측
    enet = ElasticNet(alpha=0.1, l1_ratio=0.7)
    enet.fit(X_train, y_train)
    enet_pred = enet.predict(X_test)

    mse = mean_squared_error(y_test, enet_pred)
    
    print("ElasticNet Regression MSE:", mse)

    return enet_pred

def DTreeModel():
    # 결정 트리 회귀 모델 학습 및 예측
    dt = DecisionTreeRegressor(max_depth=5, random_state=42)
    dt.fit(X_train, y_train)
    dt_pred = dt.predict(X_test)

    mse = mean_squared_error(y_test, dt_pred)
    
    print("Dicision Tree Regression MSE:", mse)

    return dt_pred

def RandomForestModel():
    # 랜덤 포레스트 회귀 모델 학습 및 예측
    rf = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)

    mse = mean_squared_error(y_test, rf_pred)
    
    print("Dicision Tree Regression MSE:", mse)

    return rf_pred

def K_FoldModel():

    # LightGBM 모델 설정
    params_lgb = {
        'objective': 'regression',
        'metric': 'rmse',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'max_depth': 6,
        'min_child_weight': 0.1,
        'verbosity': -1
    }

    # CatBoost 모델 설정
    params_catboost = {
        'iterations': 1000,
        'learning_rate': 0.05,
        'depth': 6,
        'loss_function': 'RMSE',
        'verbose': False
    }

    # Random Forest 모델 설정
    params_rf = {
        'n_estimators': 100,
        'max_depth': 6,
        'min_samples_split': 10,
        'min_samples_leaf': 5,
        'random_state': 42
    }

    # XGBoost 모델 설정
    params_xgb = {
        'objective': 'reg:squarederror',
        'learning_rate': 0.05,
        'max_depth': 6,
        'min_child_weight': 5,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'verbosity': 0
    }

    # GradientBoosting 모델 설정
    params_gb = {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 6,
        'min_samples_split': 10,
        'min_samples_leaf': 5,
        'random_state': 42
    }

    # KFold 교차 검증
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # 모델 리스트 초기화
    models = []

    # 각 모델에 대한 KFold 교차 검증 수행
    for train_index, valid_index in kf.split(X_train):

        # LightGBM 모델 학습
        lgb_train = lgb.Dataset(X_train.iloc[train_index], label=y_train.iloc[train_index])
        lgb_valid = lgb.Dataset(X_train.iloc[valid_index], label=y_train.iloc[valid_index])
        bst_lgb = lgb.train(params_lgb, lgb_train, valid_sets=[lgb_train, lgb_valid], early_stopping_rounds=10, verbose_eval=0)

        # CatBoost 모델 학습
        cb_train = cb.CatBoostRegressor(**params_catboost)
        cb_train.fit(X_train.iloc[train_index], y_train.iloc[train_index])

        # Random Forest 모델 학습
        rf_train = RandomForestRegressor(**params_rf)
        rf_train.fit(X_train.iloc[train_index], y_train.iloc[train_index])

        # XGBoost 모델 학습
        xgb_train = XGBRegressor(**params_xgb)
        xgb_train.fit(X_train.iloc[train_index], y_train.iloc[train_index])

        # Gradient Boosting 모델 학습
        gb_train = GradientBoostingRegressor(**params_gb)
        gb_train.fit(X_train.iloc[train_index], y_train.iloc[train_index])

        # 모델 리스트에 학습된 모델 추가
        models.append((bst_lgb, cb_train, rf_train, xgb_train, gb_train))

        # 각 모델의 예측 결과를 더해줌

        predictions = np.zeros(len(X_test))

        for model in models:
            predictions += model[0].predict(X_test)
            predictions += model[1].predict(X_test)
            predictions += model[2].predict(X_test)
            predictions += model[3].predict(X_test)
            predictions += model[4].predict(X_test)

        # 예측 결과의 평균을 구함

        predictions /= len(models) * 5

        # 예측 결과 출력

        print('KF-MSE:', mean_squared_error(y_test, predictions))
        
        return predictions