from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit


def split_data(X, y, test_size=0.25):
    """ Split the DataFrame into train and test for classification 

    Arguments:
        X (2d array-like): features as pd.DataFrame
        y (1d array-like): target variables as pd.DataFrame
        test_size (float): desired test-size from 0 to 1 (optional)

    Return:
        X_train, X_test, y_train, y_test (tuple): train-test split of inputs. 

    Example:
        X_train, X_test, y_train, y_test = models.split_data(df[feature_names], df['is_rejected'], 0.25)
    """
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=test_size,
                                                        random_state=42,
                                                        shuffle=True,
                                                        stratify=y)
    # print array sizes
    print('Train size: {:8d}\nTest size:  {:8d}\nMinority-ratio {:4.1f}%\nFeatures:   {:8d}'.format(
        y_train.shape[0], y_test.shape[0], 100 * sum(y_train) / y_train.count(), X_train.shape[1]))

    return X_train, X_test, y_train, y_test
