from utils import Engine, get_dataset, get_empty_traits, map_calculated_scores_to_user, calculate_similarities

if __name__ == '__main__':
    # Get and load the dataset
    dataset = get_dataset(['data/dataset_2017.csv'])
    # Get a random user with 20/79 scores filled. The rest are 0
    user, user_original_scores = dataset.get_random_user(limit=20)
    # Get a list of similar_candidates
    similar_candidates = dataset.get_similar_candidates(user)
    # Create the engine controller
    engine = Engine(user=user, candidates=similar_candidates)
    # Get a list of empty traits. These are the trait we are going to predict
    empty_traits = get_empty_traits(user)
    # Get the scores the algorithm predicted
    knn_output = engine.predict_scores_knn(empty_traits)
    # Map the scores to the user
    user = map_calculated_scores_to_user(knn_output, user)
    # Calculate how many scores match the original user's scores
    percentage_same_scores = calculate_similarities(user_original_scores.scores.values(), user.scores.values())
    # Print output
    print(f'Prediction for user {user.id} has a {round(percentage_same_scores, 3)}% accuracy!')