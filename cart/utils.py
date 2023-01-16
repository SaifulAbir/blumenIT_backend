import string
import random
from slugify import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator_cart(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug_str = "or_"+str(random_string_generator(size=8))
        slug = slugify(str(slug_str))
        # slug = slugify(str(instance.user))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=8))
        return unique_slug_generator_cart(instance, new_slug=new_slug)
    return slug


def unique_order_id_generator_for_order(instance, new_order_id=None):
    if new_order_id is not None:
        order_id = new_order_id
    else:
        order_id_str = "or_"+str(random_string_generator(size=8))
        order_id = slugify(str(order_id_str))
        # slug = slugify(str(instance.user))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_id).exists()

    if qs_exists:
        new_order_id = "{order_id}-{randstr}".format(
            order_id=order_id, randstr=random_string_generator(size=8))
        return unique_order_id_generator_for_order(instance, new_order_id=new_order_id)
    return order_id


def unique_sub_order_id_generator_for_sub_order(instance, new_sub_order_id=None):
    if new_sub_order_id is not None:
        sub_order_id = new_sub_order_id
    else:
        sub_order_id_str = "sub_or_"+str(random_string_generator(size=8))
        sub_order_id = slugify(str(sub_order_id_str))
        # slug = slugify(str(instance.user))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(sub_order_id=sub_order_id).exists()

    if qs_exists:
        new_order_id = "{sub_order_id}-{randstr}".format(
            sub_order_id=sub_order_id, randstr=random_string_generator(size=8))
        return unique_sub_order_id_generator_for_sub_order(instance, new_order_id=new_order_id)
    return sub_order_id


def unique_order_id_generator_for_vendor_order(instance, new_vendor_order_id=None):
    if new_vendor_order_id is not None:
        vendor_order_id = new_vendor_order_id
    else:
        vendor_order_id_str = "or_"+str(random_string_generator(size=8))
        vendor_order_id = slugify(str(vendor_order_id_str))
        # slug = slugify(str(instance.user))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(vendor_order_id=vendor_order_id).exists()

    if qs_exists:
        new_vendor_order_id = "{vendor_order_id}-{randstr}".format(
            vendor_order_id=vendor_order_id, randstr=random_string_generator(size=8))
        return unique_order_id_generator_for_vendor_order(instance, new_vendor_order_id=new_vendor_order_id)
    return vendor_order_id
