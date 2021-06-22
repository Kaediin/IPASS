import matplotlib.pyplot as plot
from utils import *


def compute_predictions(user, engine):
    """
    A simple helper function that computes predictions with all the algorithms at the same time of a user. Used for plots.
    :param user: the user
    :param engine: the engine
    :return:
    """
    # get the remaining traits and create 2 copies of the user
    empty_traits = get_empty_traits(user)
    user_UPCF = deepcopy(user)
    user_mean = deepcopy(user)
    # calculate the knn scores
    user_knn = map_calculated_scores_to_user(engine.predict_scores_knn(empty_traits), deepcopy(user))
    # Loop throught the empty traits and compute scores with the other 2 algorithms
    for trait in empty_traits:
        prediction_UPCF, confidence = engine.calculate_score_upcf(trait)
        prediction_mean = engine.calculate_mean_score(trait)
        user_UPCF.scores[trait] = prediction_UPCF
        user_mean.scores[trait] = str(round(prediction_mean))
    # return the 3 new users
    return user_UPCF, user_mean, user_knn


def compute_scores_all_algorithms(data, interations, incremented_trait_limit=False):
    """
    A function that computed scores for x amount of users. With helps of other classes in this script.
    :param data: the dataset
    :param interations: amount of iterations (new users)
    :param incremented_trait_limit: determines if the trait_limit should increment or not. Used for different plots
    :return: the predictions of each algorithm with the length of 'iterations'
    """
    p_UPCF, p_mean, p_knn = [], [], []
    # loop through every iteration
    for i in range(interations):
        # determine if the trait-limit need to be incremented
        if incremented_trait_limit:
            user_trait_limit = len(data.trait_keywords) - i
        else:
            user_trait_limit = int(len(data.trait_keywords) / 2)
        # create an engine controller class
        user, old_user = data.get_random_user(limit=user_trait_limit)
        similar_candidates = data.get_similar_candidates(user)
        engine = Engine(user=user, candidates=similar_candidates)

        # Get the scores and append them to the list as percentages of how many traits match (are similar)
        user_UPCF, user_mean, user_knn = compute_predictions(user, engine)
        p_UPCF.append(calculate_similarities(old_user.scores.values(), user_UPCF.scores.values()))
        p_mean.append(calculate_similarities(old_user.scores.values(), user_mean.scores.values()))
        p_knn.append(calculate_similarities(old_user.scores.values(), user_knn.scores.values()))
    # return the list
    return p_UPCF, p_mean, p_knn


def plot_engine_x_candidates(data, x=101):
    """
    A function that plots x amount of candidates and the prediction of half their scores.
    :param data: the dataset
    :param x: the amount of candidates to plot
    :return: Nothing
    """
    p_UPCF, p_mean, p_knn = compute_scores_all_algorithms(data, x)

    plot_data(
        'Prediction-accuracy of 39/79 traits over 100 candidates (2017 data)',
        [(p_UPCF, "UPCF", f'Average UPCF: {round(calculate_average_accuracy(p_UPCF), 3)}%', 'purple'),
         (p_mean, "Mean", f'Average Mean: {round(calculate_average_accuracy(p_mean), 3)}%', 'blue'),
         (p_knn, "KNN", f'Average KNN: {round(calculate_average_accuracy(p_knn), 3)}%', 'green')],
        [i * 10 for i in range(11)],
        "Prediction-algorithm accuracy in %",
        "Candidate #",
        'plot_output/plot_x_candidates.png'
    )


def plot_engine_x_traits(data):
    """
        A function that plots all the traits and incrementing the known scores by 1 each iteration
        :param data: the dataset
        """
    p_UPCF, p_mean, p_knn = compute_scores_all_algorithms(data, len(data.trait_keywords), incremented_trait_limit=True)

    plot_data(
        'Prediction-accuracy over x amount of undetermined traits (2017 data)',
        [(p_UPCF, "UPCF", f'Average UPCF: {round(calculate_average_accuracy(p_UPCF), 3)}%', 'purple'),
         (p_mean, "Mean", f'Average Mean: {round(calculate_average_accuracy(p_mean), 3)}%', 'blue'),
         (p_knn, "KNN", f'Average KNN: {round(calculate_average_accuracy(p_knn), 3)}%', 'green')],
        [i * 10 for i in range(11)],
        "Prediction-algorithm accuracy in %",
        "# of pre-determined traits",
        'plot_output/plot_x_traits.png'
    )


def plot_data(title, algorithm_data, yticks, ylabel, xlabel, savefig):
    """
    The function that plots the info
    :param title: title of the plot
    :param algorithm_data: the amount of lines, their labels, colors etc.
    :param yticks: The yaxis steps
    :param ylabel: the y label
    :param xlabel: the x labl
    :param savefig: filepath to save it to
    :return: None
    """
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
