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
