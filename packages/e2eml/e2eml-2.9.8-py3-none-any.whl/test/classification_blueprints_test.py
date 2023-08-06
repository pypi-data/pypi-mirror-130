from e2eml import classification as cb
import pandas as pd
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import classification_report
import re


def load_titanic_data():
    """
    Load & preprocess Titanic dataset. The feature engineering simulates the business knowledge part.
    The code has been taken from:
    https://towardsdatascience.com/predicting-the-survival-of-titanic-passengers-30870ccc7e8
    :return: Several dataframes and series to be processed by blueprint.
    """
    data = pd.read_csv("titanic_train.csv")
    print('Create additional features and modify existing ones.')
    deck = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "U": 8}
    data['Cabin'] = data['Cabin'].fillna("U0")
    data['Deck'] = data['Cabin'].map(lambda x: re.compile("([a-zA-Z]+)").search(x).group())
    data['Deck'] = data['Deck'].map(deck)
    data['Deck'] = data['Deck'].fillna(0)
    data['Deck'] = data['Deck'].astype(int)

    data.loc[data['Fare'] <= 7.91, 'Fare'] = 0
    data.loc[(data['Fare'] > 7.91) & (data['Fare'] <= 14.454), 'Fare'] = 1
    data.loc[(data['Fare'] > 14.454) & (data['Fare'] <= 31), 'Fare'] = 2
    data.loc[(data['Fare'] > 31) & (data['Fare'] <= 99), 'Fare'] = 3
    data.loc[(data['Fare'] > 99) & (data['Fare'] <= 250), 'Fare'] = 4
    data.loc[data['Fare'] > 250, 'Fare'] = 5

    data['Age'].fillna(0, inplace=True)
    data['Age'] = data['Age'].astype(int)
    data.loc[data['Age'] <= 11, 'Age'] = 0
    data.loc[(data['Age'] > 11) & (data['Age'] <= 18), 'Age'] = 1
    data.loc[(data['Age'] > 18) & (data['Age'] <= 22), 'Age'] = 2
    data.loc[(data['Age'] > 22) & (data['Age'] <= 27), 'Age'] = 3
    data.loc[(data['Age'] > 27) & (data['Age'] <= 33), 'Age'] = 4
    data.loc[(data['Age'] > 33) & (data['Age'] <= 40), 'Age'] = 5
    data.loc[(data['Age'] > 40) & (data['Age'] <= 66), 'Age'] = 6
    data.loc[data['Age'] > 66, 'Age'] = 6

    titles = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
    # extract titles
    data['Title'] = data.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
    # replace titles with a more common title or as Rare
    data['Title'] = data['Title'].replace(['Lady', 'Countess','Capt', 'Col','Don', 'Dr',
                                                 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    data['Title'] = data['Title'].replace('Mlle', 'Miss')
    data['Title'] = data['Title'].replace('Ms', 'Miss')
    data['Title'] = data['Title'].replace('Mme', 'Mrs')
    # convert titles into numbers
    data['Title'] = data['Title'].map(titles)
    # filling NaN with 0, to get safe
    data['Title'] = data['Title'].fillna(0)

    data['relatives'] = data['SibSp'] + data['Parch']
    data.loc[data['relatives'] > 0, 'not_alone'] = 0
    data.loc[data['relatives'] == 0, 'not_alone'] = 1
    data['not_alone'] = data['not_alone'].astype(int)

    data['Fare'] = data['Fare'].astype(int)
    data['Age_Class'] = data['Age']*data['Pclass']
    data['Fare_Per_Person'] = data['Fare']/(data['relatives']+1)
    data['Fare_Per_Person'] = data['Fare_Per_Person'].astype(int)
    print('Do dataframe splits.')
    test_df = data.head(800).copy()
    val_df = data.tail(91).copy()
    val_df_target = val_df["Survived"].copy()
    del val_df["Survived"]
    test_target = "Survived"
    test_categorical_cols = ["Pclass", "Name", 'Sex', 'PassengerId']
    return test_df, test_target, val_df, val_df_target, test_categorical_cols


def synthetic_multiclass_data():
    data = pd.read_csv("synthetic_multi_classifcation.csv")
    test_df = data.head(2500).copy()
    val_df = data.tail(499).copy()
    val_df_target = val_df["recommendation"].copy()
    del val_df["recommendation"]
    test_target = "recommendation"
    test_categorical_cols = ["status", "country"]
    return test_df, test_target, val_df, val_df_target, test_categorical_cols


def nlp_multiclass_data():
    data = pd.read_csv("Corona_NLP_train.csv", encoding='latin-1')
    data.replace({'Sentiment' : { 'Extremely Negative': 0, 'Negative': 0, 'Neutral': "N",
                                  'Extremely Positive': 1, 'Positive': 1, }}, inplace=True)
    data = data[data.Sentiment != 'N']
    test_df = data.head(2500).copy()
    val_df = data.tail(499).copy()
    val_df_target = val_df["Sentiment"].copy()
    del val_df["Sentiment"]
    test_target = "Sentiment"
    test_categorical_cols = ["Location", "OriginalTweet"]
    return test_df, test_target, val_df, val_df_target, test_categorical_cols


def blueprint_binary_test_titanic(blueprint='logistic_regression', dataset='titanic'):
    if dataset == 'titanic':
        test_df, test_target, val_df, val_df_target, test_categorical_cols = load_titanic_data()
        titanic_auto_ml = cb.ClassificationBluePrint(datasource=test_df,
                                       target_variable=test_target,
                                       categorical_columns=test_categorical_cols,
                                                     preferred_training_mode='gpu')
    elif dataset == 'synthetic_multiclass':
        test_df, test_target, val_df, val_df_target, test_categorical_cols = synthetic_multiclass_data()
        titanic_auto_ml = cb.ClassificationBluePrint(datasource=test_df,
                                                     target_variable=test_target,
                                                     categorical_columns=test_categorical_cols)
    elif dataset == 'corona_tweet':
        test_df, test_target, val_df, val_df_target, test_categorical_cols = nlp_multiclass_data()
        titanic_auto_ml = cb.ClassificationBluePrint(datasource=test_df,
                                                     target_variable=test_target,
                                                     categorical_columns=test_categorical_cols,
                                                     preferred_training_mode='gpu')
    if blueprint == 'lgbm':
        titanic_auto_ml.ml_bp02_multiclass_full_processing_lgbm_prob()
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_bp02_multiclass_full_processing_lgbm_prob(val_df)
        val_y_hat = titanic_auto_ml.predicted_classes['lgbm']
    elif blueprint == 'xgboost':
        titanic_auto_ml.ml_bp01_multiclass_full_processing_xgb_prob(preprocessing_type='nlp')
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_bp01_multiclass_full_processing_xgb_prob(val_df, preprocessing_type='nlp')
        val_y_hat = titanic_auto_ml.predicted_classes['xgboost']
    elif blueprint == 'sklearn_ensemble':
        titanic_auto_ml.ml_bp03_multiclass_full_processing_sklearn_stacking_ensemble()
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_bp03_multiclass_full_processing_sklearn_stacking_ensemble(val_df)
        val_y_hat = titanic_auto_ml.predicted_classes['sklearn_ensemble']
    elif blueprint == 'logistic_regression':
        titanic_auto_ml.ml_bp00_train_test_binary_full_processing_log_reg_prob()
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_bp00_train_test_binary_full_processing_log_reg_prob(val_df)
        val_y_hat = titanic_auto_ml.predicted_classes['logistic_regression']
    elif blueprint == 'ngboost':
        titanic_auto_ml.ml_bp04_multiclass_full_processing_ngboost(preprocessing_type='nlp')
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_bp04_multiclass_full_processing_ngboost(val_df, preprocessing_type='nlp')
        val_y_hat = titanic_auto_ml.predicted_classes['ngboost']
    elif blueprint == 'avg_booster':
        titanic_auto_ml.ml_special_binary_full_processing_boosting_blender(preprocessing_type='nlp')
        print("Start prediction on holdout dataset")
        titanic_auto_ml.ml_special_binary_full_processing_boosting_blender(val_df, preprocessing_type='nlp')
        val_y_hat = titanic_auto_ml.predicted_classes['blended_preds']
    else:
        pass

    print(classification_report(val_df_target, val_y_hat))
    try:
        matthews = matthews_corrcoef(val_df_target, val_y_hat)
    except Exception:
        print("Matthew failed.")
        matthews = 0
    print(matthews)

    if matthews > 0:
        return print('The test ran successfully.')
    else:
        return print('The test failed. Please investigate.')


blueprint_binary_test_titanic(blueprint='avg_booster', dataset='titanic')
