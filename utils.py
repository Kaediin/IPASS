from models import *


def get_empty_traits(user):
    """
    returns a list with trait-keywords of all the empty traits (score = 0)
    :param user: the user we want to check
    :return: a list of trait-names
    """
    empty_traits = []
    for trait, score in user.scores.items():
        if score == 0:
            empty_traits.append(trait)
    return empty_traits


def map_calculated_scores_to_user(predictions, user):
    """
    This function replaces the previous scores (only 0's in production) with the computed scores)
    :param predictions: the list of prediction-scores
    :param user: the user with its (original) scores
    :return: the user with its new scores
    """
    for row in predictions:
        user.scores[row[0]] = row[1]
    return user


def convert_scores_to_pecentage(scores):
    """
    This function takes in a dict of each unique score and the count of it, and return the % of the count
    :param scores: the scores with it counts
    :return: the dict with the unique scores but now the percentage as the value
    """
    # Create empty dict
    percentages = {}
    # add upp all the scores so we have a total
    total = sum(scores.values())
    for k, v in scores.items():
        # Calc the percentage of each unique score and add to the dict
        percentages[k] = 100 * v / total
    # return this new dict
    return percentages


def calculate_similarities(user_scores, predition_scores):
    """
    This function counts the number of scores that are same so we know how accurate a computed list has been
    :param user_scores: the scores of the user
    :param predition_scores: the scores of the prediction
    :return: a percentage of how many scores were the same of all the scores
    """
    c = 0
    for i in range(len(user_scores)):
        if list(user_scores)[i] == list(predition_scores)[i]:
            c += 1
    return c / float(len(user_scores)) * 100


def calculate_average_accuracy(accs):
    """
    A simple function to calculate the average
    :param accs:
    :return:
    """
    return sum(accs) / len(accs)


def get_dataset(paths):
    """
    A simple function to load in the dataset from (multiple) path(s)
    :param paths: the paths to the datasets
    :return: the loaded dataset-controller class with its attributes
    """
    dataset = Dataset(paths)
    dataset.load()
    return dataset


def generate_trait_accuracy(trait_data, user, dataset):
    """
    A complex function that calculates to accuracy of every trait with every number of valid scores.
    We do this before hand so that we can display some kind of accuracy indication in the boxplots.
    These values are not 100% accurate, but nothing is really...
    :param trait_data: The data of the known traits
    :param user: the user we use to compute
    :param dataset: the dataset
    :return: the output. A dictionary with every trait which has 79 trait combinations (in length) each.
    """
    # Create a copy of the original scores so we can build up scores that are realistic
    original_scores = user.scores.copy()
    trait_names, trait_scores = [], []
    # loop through all the known scores and add them to the lists
    for data_per_trait in trait_data:
        trait_names.append(data_per_trait[0])
        trait_scores.append(data_per_trait[1])
    # Calculate the trait we still need to compute
    leftover_traits = dataset.trait_keywords.copy()
    [leftover_traits.remove(name) for name in trait_names]
    # Create the dict
    output = {'matches': {}}
    # loop through all the leftover traits needed to score len(traits) - 1
    for i in range(len(leftover_traits)):
        # get 1 more each iteration
        random_traits = leftover_traits[:i + 1]
        # get the scores for every trait
        sim_candidates = dataset.get_similar_candidates(user)
        engine = Engine(user=user, candidates=sim_candidates)
        scores_data = engine.predict_scores_knn(random_traits, return_all_scores=True)
        # count the occurrences of each score and their percentages
        occurrences = Counter(scores_data[i][2])
        percentages_dict = convert_scores_to_pecentage(occurrences)
        percentages_values = percentages_dict.values()
        scores_values = [int(row[1]) for row in scores_data]
        # create a new dict with the amount of trait we check each time
        output['matches'][i + 1] = {}
        output['matches'][i + 1]['results'] = []
        output['matches'][i + 1]['range'] = (
            occurrences[occurrences.most_common()[-1][0]], occurrences[occurrences.most_common()[0]])
        output['matches'][i + 1]['confidence'] = percentages_dict[str(scores_values[-1])]
        output['matches'][i + 1]['results'] = [(data[0], int(data[1])) for data in scores_data]
        user.scores[leftover_traits[i]] = original_scores[leftover_traits[i]]
    # return the output
    return output
