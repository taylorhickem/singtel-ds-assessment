# dependencies ------------------------------------------------------------------------------------------------
import unittest
#from recommend_agent.recommend import RoamingPlanRecommender
from recommend_agent import roaming_plans

# constants ---------------------------------------------------------------------------------------------------
TEST_RECOMMEND_CSV_DATA = 'data/roaming_plans.csv'


# classes ----------------------------------------------------------------------------------------------------
class TestRoamingPlanRecommender(unittest.TestCase):

    #@classmethod
    #def setUpClass(cls):
    #    cls.recommender = RoamingPlanRecommender(csv_path=TEST_RECOMMEND_CSV_DATA)

    def test_roaming_plans_build(self):
        build_success, build_errors = roaming_plans.db_build()
        self.assertTrue(build_success, f'build failed with errors {build_errors}')

    #def test_malaysia_2days_5gb(self):
    #    plans = self.recommender.recommend(
    #        destination="Malaysia",
    #        duration="2 days",
    #        service_type="data",
    #        data_needed_gb=5.0
    #    )
    #
    #    self.assertTrue(plans, "Expected at least one plan, got none.")
    #
    #    expected_plan = {
    #        "Zone": "Zone 1",
    #        "Destination": "Malaysia",
    #        "Data_Pass_Validity": "2 days",
    #        "Data_Pass_Data": "5.6GB",
    #        "Data_Pass_Price": "S$6"
    #    }
    #
    #    top_plan = plans[0]
    #
    #    for key, expected_value in expected_plan.items():
    #        self.assertEqual(top_plan.get(key), expected_value,
    #                         f"Mismatch in {key}: expected '{expected_value}', got '{top_plan.get(key)}'")


if __name__ == '__main__':
    unittest.main()
