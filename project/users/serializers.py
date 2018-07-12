from apistar import types, validators, exceptions
from project.regex import EMAIL_REGEX


class Auth(types.Type):
    username = validators.String(max_length=100)
    password = validators.String(max_length=100)


# class Token(types.Type):
#     id = validators.String(allow_null=True)
#     expiry_date = validators.DateTime(allow_null=True)


class UserType(types.Type):
    _id = validators.String(allow_null=True)
    username = validators.String(min_length=3, max_length=30)
    email = validators.String(allow_null=True, pattern=EMAIL_REGEX)
    names = validators.Array(items=validators.String(), allow_null=True)
    lastnames = validators.Array(items=validators.String(), allow_null=True)
    groups = validators.Array(unique_items=True,
                              items=validators.String(enum=['admin',
                                                            'developer',
                                                            'basic']))

    # def __init__(self, *args, **kwargs):
    # validadores extra, si algun parametro es erroneo retorna ValidationError
    # con su respectivo mensaje
        # value = super().__init__(*args, **kwargs)
        # user = args[0]
        # for name in user['names']:
        #     if not isinstance(name, str):
        #         message = 'name must be string.'
        #         raise exceptions.ValidationError(message)
        # for name in user['lastnames']:
        #     if not isinstance(name, str):
        #         message = 'lastnames must be string.'
        #         raise exceptions.ValidationError(message)
        # return value
