import string
import random
from slugify import slugify


def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator_cart(instance, new_slug = None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug_str = "or_"+str(random_string_generator(size = 8))
		slug = slugify(str(slug_str))
		# slug = slugify(str(instance.user))
	Klass = instance.__class__
	qs_exists = Klass.objects.filter(slug = slug).exists()

	if qs_exists:
		new_slug = "{slug}-{randstr}".format(
			slug = slug, randstr = random_string_generator(size = 8))
		return unique_slug_generator_cart(instance, new_slug = new_slug)
	return slug