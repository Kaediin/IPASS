import glob
import unittest

from main import get_dataset


class TestCases(unittest.TestCase):

    def test_has_valid_dataset(self):
        try:
            get_dataset(glob.glob('../data/*.csv'))
        except FileNotFoundError:
            self.fail(f'Error loading in datafiles')

    def test_get_random_user_dataset(self):
        dataset = get_dataset(['../data/dataset_2017.csv'])
        self.assertIsNotNone(dataset.get_random_user())

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


if __name__ == '__main__':
    unittest.main()
