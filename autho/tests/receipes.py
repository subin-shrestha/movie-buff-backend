from model_mommy.recipe import Recipe


USER = Recipe("autho.User")

def create_user(**kwargs):
	defaults = {}
	defaults.update(**kwargs)
	return USER.make(**defaults)