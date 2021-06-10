import unittest

from main import get_dataset, compute_predictions
from models import *


def get_random_user_engine():
    dataset = get_dataset(['../data/dataset_2017.csv'])
    user, old_user = dataset.get_random_user()
    similar = dataset.get_similar_candidates(user)
    engine = Engine(user=user, candidates=similar)
    return engine, user


class TestCases(unittest.TestCase):

    def test_user_has_traits(self):
        engine, user = get_random_user_engine()
        self.assertIsNotNone(engine.get_scored_traits())

    def test_no_crash_computations(self):
        engine, user = get_random_user_engine()
        try:
            compute_predictions(user, engine)
        except (IndexError, ValueError) as e:
            self.fail(f"Function raised exception: {e.args}")


if __name__ == '__main__':
    unittest.main()
