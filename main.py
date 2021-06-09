import random
from collections import Counter
from models import *


def getRandomUserEmptyTraits(candidates):
    r_candidate = random.choice(candidates)
    return r_candidate


# def predictScoreBasedOnOthers(candidates, user, key='Zorgvuldig', span=1):
#     traits = TRAIT_KEYWORDS.copy()
#     traits.remove(key)
#     similar_scoring_cadidates = []
#     for candidate in candidates:
#         has_incorrect_value = False
#         for trait in traits:
#             if abs(int(candidate.scores.__dict__[trait]) - int(user.scores.__dict__[trait])) > span:
#                 has_incorrect_value = True
#                 break
#         if not has_incorrect_value:
#             similar_scoring_cadidates.append(candidate)
#     sim_scores = Counter(candidate.scores.__dict__[key] for candidate in similar_scoring_cadidates)
#     print(
#         f'Most common score on trait "{key}": {sim_scores.most_common(1)[0][0]}. User scored: {user.scores.__dict__[key]}')


# def predictScoreBasedOnAverage(candidates, user, key='Zorgvuldig'):
#     traits = TRAIT_KEYWORDS.copy()
#     traits.remove(key)
#     scores = [int(candidate.scores.__dict__[key]) for candidate in candidates]
#     print(f'Average score for trait "{key}": {round(sum(scores)/float(len(scores)))}')


if __name__ == '__main__':
    dataset = Dataset(['data/dataset_2017.csv'])
    dataset.load()
    user = dataset.getRandomUserEmptyTraits()
    print(len(dataset.getSimilarCandidates(user)))
    # candidates = getAllCandidates(['data/dataset_2017.csv'])
    # print(len(candidates))
    # user = getRandomUserEmptyTraits(candidates)
    # predictScoreBasedOnOthers(candidates, user)
    # predictScoreBasedOnAverage(candidates, user)
