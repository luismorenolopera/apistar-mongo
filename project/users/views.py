import typing
from bson.objectid import ObjectId
from apistar import exceptions
from users.models import User, UserDAO
from users.serializers import Auth, UserType
from users.decorators import has_group


users = UserDAO()


@has_group(['admin'])
def list_users(user: User) -> typing.List[UserType]:
    """test documentacion"""
    return [UserType(user) for user in users.get_all()]


@has_group(['admin', 'basic'])
def new_user(user: User, new_user: UserType) -> UserType:
    return users.create(new_user)


@has_group('admin', 'basic')
def hello_user(user: User) -> UserType:
    return UserType(users.get_one('_id', ObjectId(user._id)))


def auth(auth: Auth):
    """
        recibe usuario y contraseña para retornar un token de autenticacion
    """
    return users.login(auth.username, auth.password)
