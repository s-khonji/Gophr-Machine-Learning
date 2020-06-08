SELECT
    job_id, event, courier_id, jobs_history.insertion_date
FROM jobs
    LEFT JOIN jobs_history ON jobs.id = jobs_history.job_id
WHERE event IN ('accepted', 'rejected')
AND jobs.insertion_date >= '2018-01-01'
AND multi_job_type = 0
