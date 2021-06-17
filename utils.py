from models import *


def get_empty_traits(user):
    empty_traits = []
    for trait, score in user.scores.__dict__.items():
        if score == 0:
            empty_traits.append(trait)
    return empty_traits


def map_calculated_scores_to_user(predictions, user):
    for row in predictions:
        user.scores.__dict__[row[0]] = row[1]
    return user


def convert_scores_to_pecentage(scores):
    percentages = {}
    total = sum(scores.values())
    for k, v in scores.items():
        percentages[k] = 100 * v / total
    return percentages


def calculate_similarities(user_scores, predition_scores):
    c = 0
    for i in range(len(user_scores)):
        if list(user_scores)[i] == list(predition_scores)[i]:
            c += 1
    return c / float(len(user_scores)) * 100


def calculate_average_accuracy(accs):
    return sum(accs) / len(accs)


def get_dataset(paths):
    dataset = Dataset(paths)
    dataset.load()
    return dataset


def generate_trait_accuracy(trait_data, user, dataset):
    original_scores = user.scores.__dict__.copy()
    trait_names, trait_scores = [], []
    for data_per_trait in trait_data:
        trait_names.append(data_per_trait[0])
        trait_scores.append(data_per_trait[1])
    leftover_traits = TRAIT_KEYWORDS.copy()
    [leftover_traits.remove(name) for name in trait_names]
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
        occurrences = calculate_occurrences(data[2] for data in scores_data)
        percentages_dict = convert_scores_to_pecentage(occurrences)
        percentages_values = percentages_dict.values()
        scores_values = [int(row[1]) for row in scores_data]
        # create a new dict with the amount of trait we check each time
        output['matches'][i + 1] = {}
        output['matches'][i + 1]['results'] = []
        output['matches'][i + 1]['range'] = (min(percentages_values), max(percentages_values))
        output['matches'][i + 1]['confidence'] = percentages_dict[str(scores_values[-1])]
        output['matches'][i + 1]['results'] = [(data[0], int(data[1])) for data in scores_data]
        user.scores.__dict__[leftover_traits[i]] = original_scores[leftover_traits[i]]
    return output


def calculate_occurrences(scores):
    occurrences = {}
    for trait_scores in scores:
        for score in trait_scores:
            if score in occurrences:
                occurrences[score] += 1
            else:
                occurrences[score] = 1
    return occurrences
