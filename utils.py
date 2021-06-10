def get_empty_traits(user):
    empty_traits = []
    for trait, score in user.scores.__dict__.items():
        if score == 0:
            empty_traits.append(trait)
    return empty_traits
