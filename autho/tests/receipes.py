from model_mommy.recipe import Recipe


def create_user(**kwargs):
	defaults = {}
	password = kwargs.get('password')
	defaults.update(**kwargs)
	user = Recipe("autho.User").make(**defaults)
	if password:
		user.set_password(password)
		user.save()

	return user
