import string
import random
from slugify import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator_ticket(instance, new_ticket_id=None):
    if new_ticket_id is not None:
        ticket_id = new_ticket_id
    else:
        ticket_id_str = str(random_string_generator(size=8))
        ticket_id = slugify(str(ticket_id_str))

        Klass = instance.__class__
        qs_exists = Klass.objects.filter(ticket_id=ticket_id).exists()

    if qs_exists:
        new_ticket_id = 's_'+ "{ticket_id}-{randstr}".format(ticket_id=ticket_id, randstr=random_string_generator(size=8))
        return unique_slug_generator_ticket(instance, new_ticket_id=new_ticket_id)
    else:
        new_ticket_id = 's_'+ "{ticket_id}-{randstr}".format(ticket_id=ticket_id,randstr=random_string_generator(size=8))


    return new_ticket_id

