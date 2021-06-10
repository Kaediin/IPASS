from models import *
from utils import *
import copy as copy
import matplotlib.pyplot as plot


def compute_predictions(user, engine):
    empty_traits = get_empty_traits(user)
    user_mode = copy.deepcopy(user)
    user_mean = copy.deepcopy(user)

    for trait in empty_traits:
        prediction_mode, confidence = engine.calculate_mode_score(trait)
        prediction_mean = engine.calculate_mean_score(trait)
        user_mode.scores.__dict__[trait] = prediction_mode
        user_mean.scores.__dict__[trait] = str(round(prediction_mean))

    return user_mode, user_mean


def calculate_similarities(user_scores, predition_scores):
    c = 0
    for i in range(len(user_scores)):
        if list(user_scores)[i] == list(predition_scores)[i]:
            c += 1
    return 100 * c / len(user_scores)


def calculate_average_accuracy(accs):
    return sum(accs) / len(accs)


def get_dataset(paths):
    dataset = Dataset(paths)
    dataset.load()
    return dataset


def plot_x_candidates(dataset, x=101):
    p_mode, p_mean = [], []
    for i in range(x):
        user, old_user = dataset.get_random_user()
        similars = dataset.get_similar_candidates(user)
        engine = Engine(user=user, candidates=similars)

        user_mode, user_mean = compute_predictions(user, engine)
        p_mode.append(calculate_similarities(old_user.scores.__dict__.values(), user_mode.scores.__dict__.values()))
        p_mean.append(calculate_similarities(old_user.scores.__dict__.values(), user_mean.scores.__dict__.values()))

    plot.plot(p_mode, label="Mode")
    plot.plot(p_mean, label="Mean")
    plot.text(0, 25, f'Average mode: {calculate_average_accuracy(p_mode)}%', color='blue')
    plot.text(0, 20, f'Average mean: {calculate_average_accuracy(p_mean)}%', color='orange')
    plot.yticks([i * 10 for i in range(11)])
    plot.ylabel("Prediction-algorithm accuracy in %")
    plot.xlabel("Candidate #")
    plot.legend()
    plot.savefig('plot_output/plot_mode_mean.png')
    plot.show()


if __name__ == '__main__':
    dataset = get_dataset(['data/dataset_2017.csv'])
    plot_x_candidates(dataset)
