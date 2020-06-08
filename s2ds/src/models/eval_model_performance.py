import pandas as pd
from sklearn.metrics import (precision_recall_fscore_support, confusion_matrix, roc_auc_score)
from imblearn.metrics import sensitivity_specificity_support


def eval_model_performance(y_true, X_test, *args, name=None):
    """  Compute and display performance metrics for multiple classifier

    Arguments:
        y_true (1d-array-like): ground truth target values
        X_test (2d-array-like): feature set for target values
        *args (sklearn-classifier object): classifier object
        name (list): list of classifier names 

    Returns:
        performance (pd.DataFrame): estimated metrics

    Example:
        models.eval_model_performance(y_test, X_test, clf_logit, clf_xgb,
                                      name=['Logistic Regression','XGBoost'])


    """
    # list comprehension to loop over every classifier in *args and call _get_metrics() function
    performance = pd.DataFrame([_get_metrics(y_true=y_true,
                                             y_pred=clf.predict(X_test),
                                             y_pred_proba=clf.predict_proba(X_test)) for clf in args])

    # if name argument is available add as index
    if name is not None:
        performance.index = [name]

    return performance


def _get_metrics(y_true, y_pred, y_pred_proba):
    """ Compute metrics and store them as dictionary
    """
    # create empty dictionary
    metric = {}
    # compute precision, recall, and fscore
    prf = precision_recall_fscore_support(y_true, y_pred,
                                          average='binary',
                                          beta=1)
    metric['precision'], metric['recall'], metric['fscore'] = prf[0], prf[1], prf[2]

    # compute sensitivity and specificity
    sss = sensitivity_specificity_support(y_true, y_pred,
                                          average='binary',
                                          pos_label=1)
    metric['sensitivity'], metric['specificity'] = sss[0], sss[1]

    # compute confusion matrix entries
    metric['TN'], metric['FP'], metric['FN'], metric['TP'] = confusion_matrix(y_true, y_pred).ravel()

    # compute AUC
    metric['AUC'] = roc_auc_score(y_true, y_pred_proba[:, 1])

    return metric
