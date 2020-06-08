import pandas as pd
import utils


def add_event_outcome(jobs, jobs_history):
    df = jobs.merge(jobs_history, on='job_id', suffixes=['', '_history'])
    df.event = pd.Categorical(df.event, categories=['accepted', 'rejected'])
    return df


if __name__ == '__main__':
    INPATH = utils.path_to('data', 'final', 'df_clean_jobs.feather')
    INPATH_HISTORY = utils.path_to('data', 'raw', 'jobs_history.feather')
    OUTPATH = utils.path_to('data', 'final', 'df_clean_event.feather')

    print('Reading feather file from ' + INPATH)
    jobs = pd.read_feather(INPATH)
    print('Reading feather file from ' + INPATH_HISTORY)
    jobs_history = pd.read_feather(INPATH_HISTORY)

    print('Merging dataframes')
    df = add_event_outcome(jobs, jobs_history)

    print('Writing feather file to ' + OUTPATH)
    utils.ensure_directories(OUTPATH)
    df.to_feather(OUTPATH)
