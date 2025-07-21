# dependencies ------------------------------------------------------------------------------------------------
import unittest
from recommend_agent.recommend import RoamingPlanRecommender
from recommend_agent import roaming_plans
from recommend_agent.chat_agent import RoamingPlanAgent


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


class TestRoamingPlanAgent(unittest.TestCase):
    """Design placeholder tests for the conversational Recommendation Agent.

    These tests outline expected behaviours described in the design document.
    They are marked as skipped until the RoamingPlanAgent implementation is
    available.  Each test demonstrates the intended invocation pattern using an
    ``agent.step`` interface that returns a structured dictionary with plan
    choices or error details.
    """

    @classmethod
    def setUp(cls):
        # Placeholder agent stub. In future this should instantiate the real
        # RoamingPlanAgent with access to RoamingPlanRecommender.
        cls.agent = RoamingPlanAgent()

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_valid_query(self):
        """Valid query returns ranked plan options."""
        user_msg = "I'm going to Japan for 3 days and need 2GB of data."
        # response = self.agent.step(user_msg)
        # self.assertEqual(len(response['plans']), 3)
        # self.assertFalse(response.get('error'))

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_invalid_country_retry(self):
        """Unknown country should trigger validation feedback."""
        user_msg = "I'll be in Blorkistan."

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_near_match_country(self):
        """Agent clarifies close country names."""
        user_msg = "I'm traveling to Korea."

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_plan_query_prompt_duration_and_amount(self):
        """Agent asks for missing duration/data when only destination given."""
        user_msg = "Need data for Thailand."

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_non_numeric_near_duration(self):
        user_msg = "I'll be there for a few moons."

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_non_numeric_nonsense_duration(self):
        user_msg = "I'll be there for a few spoons."

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_out_of_scope_query(self):
        user_msg = "How's the weather in Tokyo?"

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_high_data_demand(self):
        user_msg = "Going to Malaysia, need 100GB for 2 weeks."

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_sms_only_request(self):
        user_msg = "Going to Vietnam, only need SMS for 5 days."

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_purchase_rejection(self):
        user_msg = "No thanks"  # after plan shown

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_user_confirms_plan(self):
        user_msg = "I'll take option 2"

    @unittest.skip("RoamingPlanAgent not implemented")
    def test_unexpected_utterance_mid_flow(self):
        user_msg = "Nevermind, show me movie times"


if __name__ == '__main__':
    unittest.main()
