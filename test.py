# dependencies ------------------------------------------------------------------------------------------------
import unittest
from recommend_agent.recommend import RoamingPlanRecommender
from recommend_agent import roaming_plans

# constants ---------------------------------------------------------------------------------------------------


# classes ----------------------------------------------------------------------------------------------------
class TestRoamingPlanRecommender(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.recommender = RoamingPlanRecommender()

    def test_roaming_plans_build(self):
        build_success, build_errors = roaming_plans.db_build()
        self.assertTrue(build_success, f'build failed with errors {build_errors}')

    def test_malaysia_2days_5gb(self):
        plans = self.recommender.recommend(
            destination="Malaysia",
            duration_days=2,
            service_type="data",
            data_needed_gb=5.0
        )
    
        self.assertTrue(plans, "Expected at least one plan, got none.")
    
        expected_plan = {
            "zone": 1,
            "duration_days": 2,
            "data_gb": 1.9,
            "price_sgd": 2.0,
            "rate_data_per_10kb": 0.01,
            "rate_calls_outgoing_per_min": 0.29,
            "rate_calls_incoming_per_min": 0.0,
            "rate_per_sms": 0.1
        }
    
        top_plan = plans[0]
    
        for key, expected_value in expected_plan.items():
            self.assertEqual(top_plan.get(key), expected_value,
                             f"Mismatch in {key}: expected '{expected_value}', got '{top_plan.get(key)}'")

    def test_invalid_destination(self):
        plans = self.recommender.recommend(
            destination="Blorkistan",
            duration_days=2,
            service_type="data",
            data_needed_gb=5.0
        )
    
        self.assertTrue(plans, "Expected a response, got none")
    
        top_plan = plans[0]
        is_expected_error = 'no zone found' in top_plan.get('error', '').lower()
        self.assertTrue(is_expected_error, f"expected 'no zone found' error, got {top_plan}")

    def test_high_data_need_filters(self):
        plans = self.recommender.recommend(
            destination="Thailand",
            duration_days=7,
            service_type="data",
            data_needed_gb=20.0
        )

        self.assertTrue(plans, "Expected at least one plan, got none.")

        top_plan = plans[0]

        expected_plan = {
            "zone": 1,
            "duration_days": 7,
            "data_gb": 6.5,
            "price_sgd": 6.0,
            "rate_data_per_10kb": 0.01,
            "rate_calls_outgoing_per_min": 0.29,
            "rate_calls_incoming_per_min": 0.0,
            "rate_per_sms": 0.1,
        }

        for key, expected_value in expected_plan.items():
            self.assertEqual(top_plan.get(key), expected_value,
                             f"Mismatch in {key}: expected '{expected_value}', got '{top_plan.get(key)}'")

    def test_unsupported_service_type(self):
        plans = self.recommender.recommend(
            destination="Malaysia",
            duration_days=1,
            service_type="fax",
            data_needed_gb=1
        )

        self.assertTrue(plans, "Expected empty result for unsupported service type")

        if plans:
            plan = plans[0]
            self.assertIn(
                'unsupported service type', 
                plan.get('error', '').lower(), 
                f"Expected error unsupported service type, got {plan}"
            )


if __name__ == '__main__':
    unittest.main()
