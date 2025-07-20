from recommend_agent.recommend import RoamingPlanRecommender

# module variables ------------------------------------------------------------------------
recommender = None

def run():
    db_load()
    test_plan_recommend_malaysia_2days_5gb()


def db_load():
    global recommender
    recommender = RoamingPlanRecommender()
    recommender.db.build(keep_open=True)


def test_plan_recommend_malaysia_2days_5gb():
    trip = {
        'destination': 'Malaysia',
        'duration_days': 2,
        'service_type': 'data',
        'data_needed_gb': 5.0
    }
    print(f'INFO. selecting plan for trip: {trip} ...')
    plan = recommender.recommend(**trip)
    rec_error = recommender.error
    db_error = recommender.db.error
    print(f'INFO. selected plan: {plan}')
    if rec_error or db_error:
        print(f'ERROR.  {rec_error} {db_error}')


if __name__ == '__main__':
    run()