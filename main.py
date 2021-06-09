from models import *

if __name__ == '__main__':
    dataset = Dataset(['data/dataset_2017.csv'])
    dataset.load()
    trait = 'Belangstellend'
    user = dataset.get_random_user()
    similars = dataset.get_similar_candidates(user)
    engine = Engine(user=user, candidates=similars)

    prediction_mode, confidence = engine.calculate_mode_score(trait)
    prediction_mean = engine.calculate_mean_score(trait)
    print(user.scores.__dict__[trait], prediction_mode, round(prediction_mean))
