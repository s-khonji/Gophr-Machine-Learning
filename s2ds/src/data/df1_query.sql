SELECT *,
CASE 
	WHEN accepted_count = 0 THEN 'abs_rejected'
	ELSE 'abs_accepted'
END AS abs_accepted_rejected
FROM(
SELECT *, COUNT(event) AS event_counts, 
	SUM( IF(event='accepted',1,0)) AS accepted_count, SUM( IF(event='rejected',1,0)) AS rejected_count
FROM (
	SELECT
	    # from jobs_history
	    jobs_history.job_id, event,
	    # from jobs
	    jobs.id, status, war_job_id,
	    #   location and distance
        #           City fields for the sake of completeness, quite messy
	    pickup_postcode, pickup_location_lat, pickup_location_lng, pickup_city,
        delivery_postcode, delivery_location_lat, delivery_location_lng, delivery_city,
	    distance,
	    #   time and date
	    jobs.insertion_date,  # indicator for direct jobs
	    earliest_pickup_time, pickup_deadline, delivery_deadline,
	    date_booked, date_started,
	    date_accepted, date_picked_up,  # no features, dependent on our criterion. may be used in visualisation
        #   job type
	    vehicle_type,
	    courier_money_earned_net,
	    is_first_war_job,
	    #       types dependent on time constraints
	    job_priority,
	    riskiness, hero_ratio, show_on_board,  # to derive if job ever was visible on the job board
	    #   consignment
	    size_x, size_y, size_z,
	    weight,
	    special_care,
	    is_food, is_fragile, is_liquid, is_not_rotatable, is_glass,
	    is_baked, is_flower, is_alcohol, is_beef, is_pork, 
	    canceled_status, canceled_reason,
	    # from jobs extra
	    estimated_journey_time,
	    final_price_net_booked, final_price_net_calc, courier_earnings_booked, courier_earnings_calc,
        available_in_job_board, taken_from_job_board, assigned_manually
	FROM jobs
		LEFT JOIN jobs_history ON jobs.id = jobs_history.job_id
		LEFT JOIN jobs_extra ON jobs.id = jobs_extra.id
	WHERE event IN ('accepted', 'rejected')
	AND jobs.insertion_date >= '2018-01-01'
	AND multi_job_type = 0
	#AND jobs.finished = 1
	#AND jobs.status IN (80)
) AS subsel
GROUP BY subsel.job_id) AS subsel_2
#HAVING accepted_count=0