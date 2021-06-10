import glob
import unittest

from main import get_dataset


class TestCases(unittest.TestCase):

    def test_has_valid_dataset(self):
        # Try to retrieve the dataset. If this fails, throw an error indicating the doest did not pass
        try:
            get_dataset(glob.glob('../data/*.csv'))
        except FileNotFoundError:
            self.fail(f'Error loading in datafiles')

    def test_get_random_user_dataset(self):
        # get the dataset object and check the function 'get_random_user' does not return None
        dataset = get_dataset(['../data/dataset_2017.csv'])
        self.assertIsNotNone(dataset.get_random_user())

    def test_user_has_similar(self):
        # get a random user from a dataset given
        dataset = get_dataset(['../data/dataset_2017.csv'])
        user, old_user = dataset.get_random_user()
        similars = []
        threshold = 1
        # fill the list with similar candidates.
        # If it does not fill on the first try we increment the threshold by onne until it does fill
        while len(similars) == 0:
            similars = dataset.get_similar_candidates(user, threshold=threshold)
            threshold += 1
            # if the threshold is larger than 5 aka there are no candidates we fail
            if threshold >= 5:
                self.fail(f'User {user} has no similar candidates!')
        # else check for results and run test
        self.assertGreaterEqual(len(similars), 1)


if __name__ == '__main__':
    unittest.main()
