import json

import matplotlib.pyplot as plot

from utils import *


def compute_predictions(user, engine):
    empty_traits = get_empty_traits(user)
    user_UPCF = copy.deepcopy(user)
    user_mean = copy.deepcopy(user)

    user_knn = map_calculated_scores_to_user(engine.predict_scores_knn(empty_traits), copy.deepcopy(user))

    for trait in empty_traits:
        prediction_UPCF, confidence = engine.calculate_score_upcf(trait)
        prediction_mean = engine.calculate_mean_score(trait)
        user_UPCF.scores[trait] = prediction_UPCF
        user_mean.scores[trait] = str(round(prediction_mean))

    return user_UPCF, user_mean, user_knn


def compute_scores_all_algorithms(data, interations, incremented_trait_limit=False):
    p_UPCF, p_mean, p_knn = [], [], []
    for i in range(interations):
        if incremented_trait_limit:
            user_trait_limit = len(data.trait_keywords) - i
        else:
            user_trait_limit = int(len(data.trait_keywords) / 2)

        user, old_user = data.get_random_user(limit=user_trait_limit)
        similar_candidates = data.get_similar_candidates(user)
        engine = Engine(user=user, candidates=similar_candidates)

        user_UPCF, user_mean, user_knn = compute_predictions(user, engine)
        p_UPCF.append(calculate_similarities(old_user.scores.values(), user_UPCF.scores.values()))
        p_mean.append(calculate_similarities(old_user.scores.values(), user_mean.scores.values()))
        p_knn.append(calculate_similarities(old_user.scores.values(), user_knn.scores.values()))
    return p_UPCF, p_mean, p_knn


def plot_engine_x_candidates(data, x=101):
    p_UPCF, p_mean, p_knn = compute_scores_all_algorithms(data, x)

    plot_data(
        'Prediction-accuracy of 39/79 traits over 100 candidates (2017 + 2018 data)',
        [(p_UPCF, "UPCF", f'Average UPCF: {round(calculate_average_accuracy(p_UPCF), 3)}%', 'purple'),
         (p_mean, "Mean", f'Average Mean: {round(calculate_average_accuracy(p_mean), 3)}%', 'blue'),
         (p_knn, "KNN", f'Average KNN: {round(calculate_average_accuracy(p_knn), 3)}%', 'green')],
        [i * 10 for i in range(11)],
        "Prediction-algorithm accuracy in %",
        "Candidate #",
        'plot_output/plot_x_candidates.png'
    )


# def plot_engine_x_traits(data):
#     p_UPCF, p_mean, p_knn = compute_scores_all_algorithms(data, len(data.trait_keywords), incremented_trait_limit=True)
#
#     plot_data(
#         'Prediction-accuracy over x amount of undetermined traits (2017 + 2018 data)',
#         [(p_UPCF, "UPCF", f'Average UPCF: {round(calculate_average_accuracy(p_UPCF), 3)}%', 'purple'),
#          (p_mean, "Mean", f'Average Mean: {round(calculate_average_accuracy(p_mean), 3)}%', 'blue'),
#          (p_knn, "KNN", f'Average KNN: {round(calculate_average_accuracy(p_knn), 3)}%', 'green')],
#         [i * 10 for i in range(11)],
#         "Prediction-algorithm accuracy in %",
#         "# of pre-determined traits",
#         'plot_output/plot_x_traits.png'
#     )


# def plot_every_score_per_trait(data, iterations=101):
#     for trait in data.trait_keywords:
#         p_scores = {'1': [], '2': [], '3': [], '4': []}
#         for i in range(iterations):
#             user, old_user = data.get_random_user()
#             user.scores[trait] = 0
#             similar_candidates = data.get_similar_candidates(user)
#             engine = Engine(user=user, candidates=similar_candidates)
#             scores = engine.calculate_score_upcf(trait, return_full_score=True)
#             [p_scores[str(k)].append(v) for k, v in convert_scores_to_pecentage(scores).items()]
#
#         for k, v in p_scores.items():
#             plot.plot(v, label=k)
#         plot.title(f'Scores for trait: {trait}')
#         plot.ylabel('Score in %')
#         plot.xlabel('# of candidates')
#         plot.legend()
#         plot.grid()
#         plot.savefig(f'plot_output/plots_per_trait/plot_{trait}.png')
#         plot.show()


def plot_data(title, algorithm_data, yticks, ylabel, xlabel, savefig):
    for i, data in enumerate(algorithm_data):
        plot.plot(data[0], label=data[1], color=data[3])
        plot.text(0, 5 + (len(algorithm_data) * 10) - (i * 5), data[2], color=data[3])
    plot.title(title)
    plot.yticks(yticks)
    plot.ylabel(ylabel)
    plot.xlabel(xlabel)
    plot.legend()
    plot.savefig(savefig)
    plot.grid()
    plot.show()


if __name__ == '__main__':
    dataset = get_dataset(['data/dataset_2017.csv'])
    user, old_user = dataset.get_random_user(limit=0)
    similar_candidates = dataset.get_similar_candidates(user)
    engine = Engine(user=user, candidates=similar_candidates)
    accuracies = {}
    for trait in dataset.trait_keywords:
        print(trait)
        accuracies[trait] = generate_trait_accuracy([(trait, user.scores[trait])], user, dataset)
        print(accuracies)
        break
    with open('results.json', 'w') as f:
        json.dump(accuracies, f)
