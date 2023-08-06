from e2eml import regression as rb
import pandas as pd
from sklearn.metrics import mean_absolute_error
# track memory consumption in terminal: dmesg


def load_housingprices_data():
    """
    Load & preprocess Housing prices dataset. T
    :return: Several dataframes and series to be processed by blueprint.
    """
    data = pd.read_csv("housingprices_train.csv")
    print('Do dataframe splits.')
    test_df = data.head(1000).copy()
    val_df = data.tail(460).copy()
    val_df_target = val_df["SalePrice"].copy()
    del val_df["SalePrice"]
    test_target = "SalePrice"
    test_categorical_cols = ["MSZoning", "Street", "Alley", "LotShape", "LotFrontage", "Street", "LandContour",
                             "Utilities", "LotConfig", "LandSlope", "Neighborhood", "Condition1", "Condition2",
                             "BldgType", "HouseStyle", "RoofStyle", "RoofMatl", "Exterior1st", "Exterior2nd",
                             "ExterQual", "ExterCond", "Foundation", "BsmtQual", "BsmtCond", "BsmtExposure",
                             "BsmtFinType1", "BsmtFinType2", "Heating", "HeatingQC", "Electrical", "KitchenQual",
                             "Functional", "FireplaceQU", "GarageType", "GarageYrBlt", "GarageFinish", "GarageQual",
                             "GarageCond", "PavedDrive", "PoolQC", "Fence", "MiscFeature", "SaleType", "SaleCondition"]
    return test_df, test_target, val_df, val_df_target, test_categorical_cols


def blueprint_regression_test_housingprices(blueprint='lgbm'):
    test_df, test_target, val_df, val_df_target, test_categorical_cols = load_housingprices_data()
    titanic_auto_ml = rb.RegressionBluePrint(datasource=test_df,
                                   target_variable=test_target,
                                   categorical_columns=test_categorical_cols,
                                   preferred_training_mode='gpu')
    if blueprint == 'lgbm':
        titanic_auto_ml.ml_bp12_regressions_full_processing_lgbm()
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_bp12_regressions_full_processing_lgbm(val_df)
        val_y_hat = titanic_auto_ml.predicted_values['lgbm']
        mae = mean_absolute_error(val_df_target, val_y_hat)
        print(mae)
    elif blueprint == 'xgboost':
        titanic_auto_ml.ml_bp11_regression_full_processing_xgboost(preprocessing_type='nlp')
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_bp11_regression_full_processing_xgboost(val_df, preprocessing_type='nlp')
        val_y_hat = titanic_auto_ml.predicted_values['xgboost']
        mae = mean_absolute_error(val_df_target, val_y_hat)
        print(mae)
    elif blueprint == 'sklearn_ensemble':
        titanic_auto_ml.ml_bp13_regression_full_processing_sklearn_stacking_ensemble()
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_bp13_regression_full_processing_sklearn_stacking_ensemble(val_df)
        val_y_hat = titanic_auto_ml.predicted_values['sklearn_ensemble']
        mae = mean_absolute_error(val_df_target, val_y_hat)
        print(mae)
    elif blueprint == 'ngboost':
        titanic_auto_ml.ml_bp14_regressions_full_processing_ngboost(preprocessing_type='nlp')
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_bp14_regressions_full_processing_ngboost(val_df, preprocessing_type='nlp')
        val_y_hat = titanic_auto_ml.predicted_values['ngboost']
        mae = mean_absolute_error(val_df_target, val_y_hat)
        print(mae)
    elif blueprint == 'linear_regression':
        titanic_auto_ml.ml_bp10_train_test_regression_full_processing_linear_reg()
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_bp10_train_test_regression_full_processing_linear_reg(val_df)
        val_y_hat = titanic_auto_ml.predicted_values['linear_regression']
        mae = mean_absolute_error(val_df_target, val_y_hat)
        print(mae)
    elif blueprint == 'avg_booster':
        titanic_auto_ml.ml_special_regression_full_processing_boosting_blender()
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_special_regression_full_processing_boosting_blender(val_df, preprocessing_type='nlp')
        val_y_hat = titanic_auto_ml.predicted_values['blended_preds']
        mae = mean_absolute_error(val_df_target, val_y_hat)
        print(mae)
    else:
        pass


blueprint_regression_test_housingprices(blueprint='avg_booster')