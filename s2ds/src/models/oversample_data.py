from imblearn.over_sampling import ADASYN


def oversample_ADASYN(X, y, ratio=0.15):
    """ Oversample minority class using the ADASYN algorithm

    Arguments:
        X (2d array-like): feature set
        y (1d array-lile): target values
        ratio (float): desired ratio between minority and majority (optional)

    Return:
        X_os (2d array-like): oversampled feature set
        y_os (1d array-lile): oversampled target values

    Example:
        X_train_os, y_train_os = models.oversample_ADASYN(X_train, y_train, 0.3)
    """

    # construct the ADASYN object
    os = ADASYN(sampling_strategy=ratio,
                n_neighbors=5,
                random_state=42)

    # oversample X and y data
    X_os, y_os = os.fit_sample(X, y)
    print('Oversampled minority-ratio of: {:3.1f}%'.format(100 * sum(y_os) / y_os.count()))

    return X_os, y_os
