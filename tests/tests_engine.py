import unittest

from main import get_dataset, compute_predictions
from models import *


def get_random_user_engine():
    # Create the engine class and return it
    dataset = get_dataset(['../data/dataset_2017.csv'])
    user, old_user = dataset.get_random_user()
    similar = dataset.get_similar_candidates(user)
    engine = Engine(user=user, candidates=similar)
    return engine, user


def user_has_no_missing_scores(scores):
    for k, v in scores.items():
        if int(v) == 0 or int(v) is None or int(v) < 1 or int(v) > 4:
            return False
    return True


class TestCases(unittest.TestCase):

    def test_user_has_traits(self):
        # check if the function 'get_scored_traits' works
        engine, user = get_random_user_engine()
        self.assertIsNotNone(engine.get_scored_traits())

    def test_no_crash_computations(self):
        # try to run the function 'compute_predictions'. If there is no error thrown, it works
        engine, user = get_random_user_engine()
        try:
            compute_predictions(user, engine)
        except (IndexError, ValueError) as e:
            self.fail(f"Function raised exception: {e.args}")

    def test_knn_has_results(self):
        # get a random user and engine setup
        engine, user = get_random_user_engine()
        # get results for each algorithms and check to see if the results are valid
        p_UPCF, p_mean, p_knn = compute_predictions(user, engine)
        self.assertTrue(user_has_no_missing_scores(p_knn.scores.__dict__))

    def test_mean_has_results(self):
        # get a random user and engine setup
        engine, user = get_random_user_engine()
        # get results for each algorithms and check to see if the results are valid
        p_UPCF, p_mean, p_knn = compute_predictions(user, engine)
        self.assertTrue(user_has_no_missing_scores(p_mean.scores.__dict__))

    def test_UPCF_has_results(self):
        # get a random user and engine setup
        engine, user = get_random_user_engine()
        # get results for each algorithms and check to see if the results are valid
        p_UPCF, p_mean, p_knn = compute_predictions(user, engine)
        self.assertTrue(user_has_no_missing_scores(p_UPCF.scores.__dict__))


if __name__ == '__main__':
    unittest.main()
