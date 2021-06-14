import copy as copy

import matplotlib.pyplot as plot

from models import *
from utils import *


def compute_predictions(user, engine):
    empty_traits = get_empty_traits(user)
    user_UPCF = copy.deepcopy(user)
    user_mean = copy.deepcopy(user)
    user_knn = copy.deepcopy(user)

    prediction_knn = engine.predict_scores_knn(empty_traits)
    for row in prediction_knn:
        user_knn.scores.__dict__[row[0]] = row[1]

    for trait in empty_traits:
        prediction_UPCF, confidence = engine.calculate_score_upcf(trait)
        prediction_mean = engine.calculate_mean_score(trait)
        user_UPCF.scores.__dict__[trait] = prediction_UPCF
        user_mean.scores.__dict__[trait] = str(round(prediction_mean))

    return user_UPCF, user_mean, user_knn


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


def plot_x_candidates(dataset, x=101):
    p_UPCF, p_mean, p_knn = [], [], []
    for i in range(x):
        user, old_user = dataset.get_random_user()
        similars = dataset.get_similar_candidates(user)
        engine = Engine(user=user, candidates=similars)

        user_UPCF, user_mean, user_knn = compute_predictions(user, engine)
        p_UPCF.append(calculate_similarities(old_user.scores.__dict__.values(), user_UPCF.scores.__dict__.values()))
        p_mean.append(calculate_similarities(old_user.scores.__dict__.values(), user_mean.scores.__dict__.values()))
        p_knn.append(calculate_similarities(old_user.scores.__dict__.values(), user_knn.scores.__dict__.values()))

    plot_data(
        'Prediction-accuracy of 50 traits over 100 candidates (2017 data)',
        [p_UPCF, "UPCF", f'Average UPCF: {round(calculate_average_accuracy(p_UPCF), 3)}%'],
        [p_mean, "Mean", f'Average mean: {round(calculate_average_accuracy(p_mean), 3)}%'],
        [p_knn, "KNN", f'Average knn: {round(calculate_average_accuracy(p_knn), 3)}%'],
        [i * 10 for i in range(11)],
        "Prediction-algorithm accuracy in %",
        "Candidate #",
        'plot_output/plot_x_candidates.png'
    )


def plot_x_traits(dataset):
    p_UPCF, p_mean, p_knn = [], [], []
    for i in range(21):
        user, old_user = dataset.get_random_user(limit=len(TRAIT_KEYWORDS) - i)
        similars = dataset.get_similar_candidates(user)
        engine = Engine(user=user, candidates=similars)

        user_UPCF, user_mean, user_knn = compute_predictions(user, engine)
        p_UPCF.append(calculate_similarities(old_user.scores.__dict__.values(), user_UPCF.scores.__dict__.values()))
        p_mean.append(calculate_similarities(old_user.scores.__dict__.values(), user_mean.scores.__dict__.values()))
        p_knn.append(calculate_similarities(old_user.scores.__dict__.values(), user_knn.scores.__dict__.values()))

    plot_data(
        'Prediction-accuracy over x amount of undetermined traits (2017 data)',
        [p_UPCF, "UPCF", f'Average UPCF: {round(calculate_average_accuracy(p_UPCF), 3)}%'],
        [p_mean, "Mean", f'Average mean: {round(calculate_average_accuracy(p_mean), 3)}%'],
        [p_knn, "KNN", f'Average knn: {round(calculate_average_accuracy(p_knn), 3)}%'],
        [i * 10 for i in range(11)],
        "Prediction-algorithm accuracy in %",
        "# of pre-determined traits",
        'plot_output/plot_x_traits.png'
    )


def plot_every_trait(dataset, iterations=101):
    for trait in TRAIT_KEYWORDS:
        p_scores = {'1': [], '2': [], '3': [], '4': []}
        for i in range(iterations):
            user, old_user = dataset.get_random_user()
            user.scores.__dict__[trait] = 0
            similars = dataset.get_similar_candidates(user)
            engine = Engine(user=user, candidates=similars)
            scores = engine.calculate_score_upcf(trait, return_full_score=True)
            [p_scores[str(k)].append(v) for k, v in convert_scores_to_pecentage(scores).items()]

        for k, v in p_scores.items():
            plot.plot(v, label=k)
        plot.title(f'Scores for trait: {trait}')
        plot.ylabel('Score in %')
        plot.xlabel('# of candidates')
        plot.legend()
        plot.grid()
        plot.savefig(f'plot_output/plots_per_trait/plot_{trait}.png')
        plot.show()


def plot_data(title, UPCF_data, mean_data, knn_data, yticks, ylabel, xlabel, savefig):
    plot.plot(UPCF_data[0], label=UPCF_data[1], color='purple')
    plot.plot(mean_data[0], label=mean_data[1], color='blue')
    plot.plot(knn_data[0], label=knn_data[1], color='orange')
    plot.title(title)
    plot.text(0, 20, knn_data[2], color='orange')
    plot.text(0, 25, UPCF_data[2], color='purple')
    plot.text(0, 30, mean_data[2], color='blue')
    plot.yticks(yticks)
    plot.ylabel(ylabel)
    plot.xlabel(xlabel)
    plot.legend()
    plot.savefig(savefig)
    plot.grid()
    plot.show()


def map_calculated_scores_to_user(predictions, user):
    for row in predictions:
        user.scores.__dict__[row[0]] = row[1]
    return user


def run_knn():
    dataset = Dataset(['data/dataset_2017.csv'])
    all_candidates = dataset.load()
    user, old_user = dataset.get_random_user()
    # similars = dataset.get_similar_candidates(user)
    empty_traits = get_empty_traits(user)
    engine = Engine(user=user, candidates=all_candidates)
    prediction_knn = engine.predict_scores_knn(empty_traits)
    user = map_calculated_scores_to_user(prediction_knn, user)


def run_mean():
    dataset = Dataset(['data/dataset_2017.csv'])
    all_candidates = dataset.load()
    user, old_user = dataset.get_random_user()
    # similars = dataset.get_similar_candidates(user)
    empty_traits = get_empty_traits(user)
    engine = Engine(user=user, candidates=all_candidates)
    prediction_scores = []
    for trait in empty_traits:
        prediction_scores.append((trait, engine.calculate_mean_score(trait)))
    user = map_calculated_scores_to_user(prediction_scores, user)


def run_UPCF():
    dataset = Dataset(['data/dataset_2017.csv'])
    all_candidates = dataset.load()
    user, old_user = dataset.get_random_user()
    # similars = dataset.get_similar_candidates(user)
    empty_traits = get_empty_traits(user)
    engine = Engine(user=user, candidates=all_candidates)
    prediction_scores = []
    for trait in empty_traits:
        prediction_UPCF, confidence = engine.calculate_score_upcf(trait)
        prediction_scores.append((trait, prediction_UPCF))
    user = map_calculated_scores_to_user(prediction_scores, user)


if __name__ == '__main__':
    # start = timeit.default_timer()
    # run_knn()
    # end = timeit.default_timer()
    # print(f'Time KNN-algorithm: {end-start} seconds')
    # start = timeit.default_timer()
    # run_mean()
    # end = timeit.default_timer()
    # print(f'Time Mean-algorithm: {end-start} seconds')
    # start = timeit.default_timer()
    # run_UPCF()
    # end = timeit.default_timer()
    # print(f'Time UPCF-algorithm: {end-start} seconds')
    dataset = get_dataset(['data/dataset_2017.csv'])
    plot_x_candidates(dataset)
    plot_x_traits(dataset)
    # plot_every_trait(dataset)
