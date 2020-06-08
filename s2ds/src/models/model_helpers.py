import pickle
import utils
import os


def save_model(classifier, save_as, model_dir=utils.path_to('models')):
    """ Save classifier 

    Arguments:
        classifier (sklearn API classifier): classifier object
        save_as (string): filename
        model_dir (string): filepath 
    """
    try:
        pickle.dump(obj=classifier,
                    file=open(os.path.join(model_dir, save_as), "wb"))
        print('Saved: {}.'.format(type(classifier)))
    except:
        print('Not successful! {}.'.format(type(classifier)))


def load_model(filename, model_dir=utils.path_to('models')):
    """ Load classifier 

    Arguments:
        filename (string): filename to load
        model_dir (string): filepath 

    Return:
        classifier (sklearn API classifier): loaded classifier

    """
    try:
        classifier = pickle.load(open(os.path.join(model_dir, filename), "rb"))
        print('Loaded: {}.'.format(type(classifier)))
        return classifier
    except:
        print('Not Successful!')
