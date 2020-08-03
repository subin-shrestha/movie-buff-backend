from model_mommy.recipe import Recipe


def create_movie(**kwargs):
	return Recipe("quiz.Movie").make(**kwargs)


def create_question(**kwargs):
	return Recipe("quiz.Question").make(**kwargs)


def create_choice(**kwargs):
	return Recipe("quiz.Choice").make(**kwargs)


def create_user_aggregate(**kwargs):
	return Recipe("quiz.UserAggregate").make(**kwargs)
