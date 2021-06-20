import json

from utils import *

if __name__ == '__main__':
    dataset = get_dataset(['data/dataset_2017.csv'])
    user, old_user = dataset.get_random_user(limit=0)
    similar_candidates = dataset.get_similar_candidates(user)
    engine = Engine(user=user, candidates=similar_candidates)
    accuracies = {}
    for trait in dataset.trait_keywords:
        print(trait)
        accuracies[trait] = generate_trait_accuracy([(trait, user.scores[trait])], user, dataset)
    with open('results.json', 'w') as f:
        json.dump(accuracies, f)
