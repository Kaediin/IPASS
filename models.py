from copy import deepcopy
from csv import reader as csv_reader
from math import sqrt
from random import choice, randint
from collections import Counter
from dataclasses import dataclass


# A list with static trait-keywords. All the rows in the datasets have scores corresponding to these keys


@dataclass(frozen=False)
class Dataset:
    """
    Dataset class model which is used as a controller class.
    This class has a set of functions used to compute data with the attributes

    Args:
        :param paths: a list of paths where the datasets are placed
        :param candidates: hold a list of all the candidates. These are computed by function: load
     """
    paths: list
    traits_to_reset = set()
    candidates = []
    trait_keywords = []

    def load(self):
        """
        Load all the rows from the dataset(s) into the dataclass as Candidate models
        :return: all of the Candidate-objects from the loaded dataset(s)
        """
        candidates_models = []
        self.trait_keywords = []
        # Loop through every file-path
        for file in self.paths:
            # open the file as f
            with open(file, newline='') as f:
                # create a reader (by reader the file)
                reader = csv_reader(f, delimiter=';')
                # Create a candidate object:
                #     - First column is the candidates id
                #     - Second column is the candidas research_id
                #     - The rest of the columns are the traits
                # Add these candidates to a list ( we use a list-comprehension as these have faster runtimes)
                # We also skip the first iteration as this row ony has the headers of the columns
                for i, row in enumerate(reader):
                    if i == 0:
                        self.trait_keywords = row[2:]
                    else:
                        candidates_models.append(Candidate(row[0], row[1], self.match_score_traits(row[2:])))
        # Assign the list of candidates to the class attribute and return said attribute
        self.candidates = candidates_models
        return self.candidates

    def match_score_traits(self, user_scores):
        scores = {}
        for i, score in enumerate(user_scores):
            scores[self.trait_keywords[i]] = score
        return scores

    def get_random_user(self, empty_traits=True, limit=int(len(trait_keywords) / 2)):
        """
        This function gets and returns a random (mutated) candidate from the list of all candidates
        :param empty_traits: a boolean that clears a set amount of traits (based on the limit value)
        :param limit: determines how many traits will be cleared
        :return: the candidate with mutated trait-values if stated by the parameters
        """
        # Choose a random candidate from the list of candidates
        candidate = choice(self.candidates)
        # remove this candidate from the list so it doesnt get compared to itself lateron
        self.candidates.remove(candidate)
        # create a deepcopy (for testing purposes we want to see the before and after -values)
        old_candidate = deepcopy(candidate)
        if empty_traits:
            # Create a set of unqiue trait-names
            while len(self.traits_to_reset) < limit:
                self.traits_to_reset.add(choice(self.trait_keywords))
            # loop through the row and set the value to 0
            for trait in list(self.traits_to_reset)[:limit]:
                candidate.scores[trait] = 0
        # return the new (mutated) and old (original) candidate
        return candidate, old_candidate

    def get_similar_candidates(self, user, threshold=1):
        """
        This function will return a list of candidates similar to the user
        The candidates are taken from the attribute of this class. These are given by calling the function 'load'
        :param user: the user you want to compare the candidates to
        :param threshold: an Integer which states how much the trait-score can be off by for it to be accepted
        :return: a list of similar scoring candidates
        """
        # Create a list of traits where the corresponding value is not 0
        traits = [k for k, v in user.scores.items() if v != 0]
        similar_scoring_cadidates = []
        # Loop through every candidate
        while len(similar_scoring_cadidates) == 0:
            for candidate in self.candidates:
                # set a default value
                has_higher_threshold_value = False
                # Loop through every trait
                for trait in traits:
                    # If the candidate and the user both have a value for this trait we keep going
                    # else we continue to next iteration
                    if int(candidate.scores[trait]) != 0 and int(user.scores[trait]) != 0:
                        # If the absolute value of the candidate score minus the user score is less than the threshold
                        # (ie we are out of range) we change the value letting the outer-scope know and break
                        if abs(int(candidate.scores[trait]) - int(user.scores[trait])) > threshold:
                            has_higher_threshold_value = True
                            break
                # Depending on the value we append the candidate to the list
                # (if the absolute value above was in range or not)
                if not has_higher_threshold_value:
                    similar_scoring_cadidates.append(candidate)
            if len(similar_scoring_cadidates) == 0:
                threshold += 1
            else:
                break
        return similar_scoring_cadidates


@dataclass(frozen=True)
class Candidate:
    """
    the candidate model used to convert a row of the dataset to an object

    Arguments:
        :param id: the unique id of the user
        :param research_id: the unique research-database id
        :param scores: a dict of all the traits with the name as key and score as value.
                        Disguised as the object TraitScores
    """
    id: int
    research_id: str
    scores: {}


@dataclass(frozen=False)
class Engine:
    """
    The engine class which is used as a controller-class
    This class is used to compute predictions with the arguments given
    Arguments:
        :param candidates: a list of candidates (usually similar candidates to the user)
        :param user: the user you want to predict scores for
    """
    candidates: list
    user: Candidate

    def get_scored_traits(self):
        """
        This class check every score of the user and returns only the scores which have a value
        :return: a list of trait-names which have corresponding values
        """
        # Check for every item in the dict is the value is not 0. Then we append the key. Else nothing
        # We do this in a list-comprehension as the runtimes are faster
        return [k for k, v in self.user.scores.items() if v != 0]

    def calculate_mean_score(self, trait_name):
        """
        Predict a score based on the mean score of the (similar) candidates
        :param trait_name: the name of the trait we want to compute the mean score of
        :return: the mean score of the trait
        """
        # Get all the scores of the trait given from all the candidates
        scores = [int(candidate.scores[trait_name]) for candidate in self.candidates]
        # If we dont have a single score (ie: we dont have (similar) candidates with a traitscore)
        # We return a predefined value
        if len(scores) == 0:
            # TODO: Find valid response!
            return randint(0, 5)
        # return the summed up values divided by the lengths. Also known as the mean-value
        return sum(scores) / float(len(scores))

    def calculate_score_upcf(self, trait_name, return_full_score=False):
        """
        This function will compute a score of a trait from the list of (similar) candidates with te UPCF algorithm
        This algorithm is described in detail here: https://github.com/Kaediin/IPASS/issues/6
        :param return_full_score: return the dict with all the scores and their counters
        :param trait_name: the trait-name we want to predict a score for
        :return: The calculated mean score
        """

        sim_scores = Counter(candidate.scores[trait_name] for candidate in self.candidates)
        if return_full_score:
            return sim_scores
        if len(sim_scores.values()) == 0:
            # TODO: Find valid response!
            return randint(0, 5), 0
        return sim_scores.most_common(1)[0][0], (100 * sim_scores.most_common(1)[0][1] / sum(sim_scores.values()))

    def calculate_euclidean_distance(self, traits, similar_candidate):
        """
        Calculate the Euclidean distance between two vectors (candidates). We do this by:
            1. Subtracting both trait values
            2. Squaring this result
            3. Appending the squared resul to the distance value
            4. Return the square-root of the total distances
        :param traits: the list of traits we want to calculate the distance of
        :param similar_candidate: a candidate similar to the user
        :return: the square-root value of the distance
        """
        distance = 0.0
        for trait in traits:
            distance += (float(self.user.scores[trait]) - float(similar_candidate.scores[trait])) ** 2
        return sqrt(distance)

    def get_nearest_neighbours(self, traits, num_neighbors=-1):
        """
        Get nearest neighbours to the user
        :param traits: The traits we want to look at to determine the distance
        :param num_neighbors: the amount of neighbours we want to have
        :return: all the distances sorted so we can return a certain amount of neighbours
        """
        distances = [(candidate, self.calculate_euclidean_distance(traits, candidate)) for candidate in self.candidates]
        distances.sort(key=lambda row: row[1])
        num_neighbors = len(distances) if num_neighbors == -1 or num_neighbors > len(distances) else num_neighbors
        return [distances[i][0] for i in range(num_neighbors)]

    def predict_scores_knn(self, traits, num_neighbors=-1, return_all_scores=False):
        """
        This function combines the other KNN-functions to compute an output
        :param return_all_scores: deteremines if the algorithm wants all the scores back
        :param traits: the traits we want to predict scores for
        :param num_neighbors: the amount of neighbours we want to use for computing
        :return: the values. A tuple with the trait-name and score
        """
        # Get all the neighbours
        neighbours = self.get_nearest_neighbours(traits, num_neighbors=num_neighbors)
        output_values = []
        for trait in traits:
            # get the value from all the neighbours
            values_trait = [nb.scores[trait] for nb in neighbours]
            vals = values_trait.copy()
            # get the max value which is the most likely that the user will score
            prediction = max(set(values_trait), key=values_trait.count)
            # append the prediction-value in a tuple with the trait-name to the output list and all the scores if stated
            if return_all_scores:
                output_values.append((trait, prediction, list(vals)))
            else:
                output_values.append((trait, prediction))
        # return the list with trait-names and corresponding scores
        return output_values
