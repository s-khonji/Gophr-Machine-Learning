from sklearn.metrics import (make_scorer, recall_score, roc_auc_score)
from sklearn.model_selection import (StratifiedKFold, GridSearchCV)
from sklearn.linear_model import LogisticRegression
import xgboost as xgb


class Model:
  """ Parent model class providing fitting and grid-search with cross-validation function
  """

  def __init__(self, HYPERPARAMETERS, CLASSIFIER, METRIC, CVFOLDS=5):
    """ Constructor for model class

    Arguments
        HYPERPARAMETERS (dictionary): hyperparameters of the model
        CLASSIFIER (sklearn API classifier): classifier  
        CVFOLDS (int): number of folds for cross-validation(optional)
        METRIC (sklearn API metric): metric used for grid-search

    """
    self.HYPERPARAMETERS = HYPERPARAMETERS
    self.CLASSIFIER = CLASSIFIER
    self.CVFOLDS = CVFOLDS
    self.METRIC = METRIC

  def fit(self, X, y):
    """ Fit classifier with sklearn's fit method
    """
    return self.CLASSIFIER(**self.HYPERPARAMETERS).fit(X, y)

  def gridsearch_fit(self, X, y, parameter_grid={}):
    """ Perform grid search
    """
    # join parameter grid dictionaries for grid search
    parameter_grid = {**self.HYPERPARAMETERS, **parameter_grid}

    # transform each value in the dictionary to a list to perform grid search
    parameter_grid.update({key: [parameter_grid[key]] for key in parameter_grid if not isinstance(parameter_grid[key], list)})

    # setup cross-validation
    skf = StratifiedKFold(n_splits=self.CVFOLDS,
                          shuffle=True,
                          random_state=42)
    # score function providing the metric for grid search
    scorer = make_scorer(self.METRIC)

    # build and fit classifier with grid search
    gs_classifier = GridSearchCV(estimator=self.CLASSIFIER(),
                                 param_grid=parameter_grid,
                                 cv=skf.split(X, y),
                                 scoring=scorer,
                                 n_jobs=4,
                                 verbose=10).fit(X, y)

    print('Best parameters found:\n {}'.format(gs_classifier.best_params_))

    return gs_classifier


class LogReg(Model):
  """ Logistic Regression model with default hyperparameters
  """

  def __init__(self):
    super().__init__(HYPERPARAMETERS={'solver': 'lbfgs',
                                      'C': 1,
                                      'penalty': 'l2',
                                      'random_state': 42,
                                      'dual': False,
                                      'max_iter': 1e3,
                                      'n_jobs': -1},
                     CLASSIFIER=LogisticRegression,
                     METRIC=roc_auc_score,
                     CVFOLDS=5)


class Xgb(Model):
  """ Child class for XGBoost model with hyperparameters
  """

  def __init__(self):
    super().__init__(HYPERPARAMETERS={'objective': 'binary:logistic',
                                      'min_child_weight': 0.3,
                                      'gamma': 0.01,
                                      'subsample': 1,
                                      'colsample_bytree': 1,
                                      'max_depth': 7,
                                      'learning_rate': 0.01,
                                      'n_estimators': 400,
                                      'reg_lambda': 1,
                                      'reg_lambda': 0.01,
                                      'scale_pos_weight': 1,
                                      'silent': False},
                     CLASSIFIER=xgb.XGBClassifier,
                     METRIC=roc_auc_score,
                     CVFOLDS=4)

  def fit_xgb_cv(self, X, y):
    """ XGB cross-validation to find number of boost rounds
    """
    dmatrix = xgb.DMatrix(X, y)
    cv_res = xgb.cv(dtrain=dmatrix,
                    params=self.HYPERPARAMETERS,
                    nfold=self.CVFOLDS,
                    num_boost_round=1000,
                    metrics='auc',
                    early_stopping_rounds=50)

    return cv_res.tail(n=1)


class Xgb_m4(Model):
  """ Child class for XGBoost model 4 with hyperparameters
  """

  def __init__(self):
    super().__init__(HYPERPARAMETERS={'objective': 'binary:logistic',
                                      'min_child_weight': 0.3,
                                      'gamma': 0.01,
                                      'subsample': 1,
                                      'colsample_bytree': 0.8,
                                      'max_depth': 12,
                                      'learning_rate': 0.2,
                                      'n_estimators': 200,
                                      'reg_lambda': 1,
                                      'reg_lambda': 0.01,
                                      'scale_pos_weight': 1,
                                      'silent': False},
                     CLASSIFIER=xgb.XGBClassifier,
                     METRIC=roc_auc_score,
                     CVFOLDS=4)

  def fit_xgb_cv(self, X, y):
    """ XGB cross-validation to find number of boost rounds
    """
    dmatrix = xgb.DMatrix(X, y)
    cv_res = xgb.cv(dtrain=dmatrix,
                    params=self.HYPERPARAMETERS,
                    nfold=self.CVFOLDS,
                    num_boost_round=1000,
                    metrics='auc',
                    early_stopping_rounds=50)

    return cv_res.tail(n=1)
