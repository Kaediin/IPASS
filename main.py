from models import *

if __name__ == '__main__':
    dataset = Dataset(['data/dataset_2017.csv'])
    dataset.load()
    user = dataset.get_random_user()
    similars = dataset.get_similar_candidates(user)

    key = 'Belangstellend'
    engine = Engine(user=user, candidates=similars)
    user_score = user.scores.__dict__[key]
    prediction_mean = engine.calculate_mean_score(key)
    prediction_mode, accuracy = engine.calculate_mode_score(key)
    print(f'User score: {user_score}\nMean score: {prediction_mean}\nMode score: {prediction_mode}, {round(accuracy)}% accuracy')




