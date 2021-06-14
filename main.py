from models import *
from utils import *
import copy as copy
import matplotlib.pyplot as plot


def compute_predictions(user, engine):
    empty_traits = get_empty_traits(user)
    user_mode = copy.deepcopy(user)
    user_mean = copy.deepcopy(user)

    for trait in empty_traits:
        prediction_mode, confidence = engine.calculate_score_upcf(trait)
        prediction_mean = engine.calculate_mean_score(trait)
        user_mode.scores.__dict__[trait] = prediction_mode
        user_mean.scores.__dict__[trait] = str(round(prediction_mean))

    return user_mode, user_mean


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

    plot_data(
        'Prediction-accuracy of 50 traits over 100 candidates (2017 data)',
        [p_mode, "Mode", f'Average mode: {round(calculate_average_accuracy(p_mode), 3)}%'],
        [p_mean, "Mean", f'Average mean: {round(calculate_average_accuracy(p_mean), 3)}%'],
        [i * 10 for i in range(11)],
        "Prediction-algorithm accuracy in %",
        "Candidate #",
        'plot_output/plot_x_candidates.png'
    )


def plot_x_traits(dataset):
    p_mode, p_mean = [], []
    for i in range(len(TRAIT_KEYWORDS)):
        user, old_user = dataset.get_random_user(limit=len(TRAIT_KEYWORDS) - i)
        similars = dataset.get_similar_candidates(user)
        engine = Engine(user=user, candidates=similars)

        user_mode, user_mean = compute_predictions(user, engine)
        p_mode.append(calculate_similarities(old_user.scores.__dict__.values(), user_mode.scores.__dict__.values()))
        p_mean.append(calculate_similarities(old_user.scores.__dict__.values(), user_mean.scores.__dict__.values()))

    plot_data(
        'Prediction-accuracy over x amount of undetermined traits (2017 data)',
        [p_mode, "Mode", f'Average mode: {round(calculate_average_accuracy(p_mode), 3)}%'],
        [p_mean, "Mean", f'Average mean: {round(calculate_average_accuracy(p_mean), 3)}%'],
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


def plot_data(title, mode_data, mean_data, yticks, ylabel, xlabel, savefig):
    plot.plot(mode_data[0], label=mode_data[1])
    plot.plot(mean_data[0], label=mean_data[1])
    plot.title(title)
    plot.text(0, 25, mode_data[2], color='blue')
    plot.text(0, 20, mean_data[2], color='orange')
    plot.yticks(yticks)
    plot.ylabel(ylabel)
    plot.xlabel(xlabel)
    plot.legend()
    plot.savefig(savefig)
    plot.grid()
    plot.show()


if __name__ == '__main__':
    dataset = get_dataset(['data/dataset_2017.csv'])
    plot_x_candidates(dataset)
    plot_x_traits(dataset)
    # plot_every_trait(dataset)
