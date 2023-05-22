from uuid import uuid4

from django.template.defaultfilters import slugify


def generate_uuid(length=10):
    """
    Generate a UUID that we can use as unique_identifiers in our
    models instead of PK.
    """
    return str(uuid4().hex[:length])


def generate_slug(label):
    """
    Generate unique slug for our models
    """
    uuid = generate_uuid(8)  # Generate 8-character UUID
    return f'{uuid}-{slugify(label)}'
