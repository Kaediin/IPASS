import unittest

from main import *
from models import *


class TestCases(unittest.TestCase):

    def test_user_has_similar(self):
        dataset = get_dataset(['../data/dataset_2017.csv'])
        user, old_user = dataset.get_random_user()
        similars = []
        threshold = 1
        while len(similars) == 0:
            similars = dataset.get_similar_candidates(user, threshold=threshold)
            threshold += 1
            if threshold >= 5:
                self.fail(f'User {user} has no similar candidates!')
        self.assertGreaterEqual(len(similars), 1)

    def test_no_crash_computations(self):
        dataset = get_dataset(['../data/dataset_2017.csv'])
        user, old_user = dataset.get_random_user()
        similar = dataset.get_similar_candidates(user)
        engine = Engine(user=user, candidates=similar)
        try:
            compute_predictions(user, engine)
        except (IndexError, ValueError) as e:
            self.fail(f"Function raised exception: {e.args}")


if __name__ == '__main__':
    unittest.main()
