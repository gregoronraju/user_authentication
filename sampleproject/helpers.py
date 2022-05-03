import environ
from django.core.exceptions import ImproperlyConfigured

env = environ.Env()
environ.Env.read_env()


def get_env_value(env_variable):
    """
    This function will read given key from environment and will return corresponding value
    :param env_variable string the key of the vale to be read form environment
    :returns : string

    """
    try:
        return env(env_variable)
    except KeyError:
        error_msg = 'The required Environment variable {}  is not set'.format(env_variable)
        raise ImproperlyConfigured(error_msg)
