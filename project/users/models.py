from datetime import datetime, timedelta
from bson.objectid import ObjectId
import jwt
from apistar import http
from pymongo import MongoClient
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from apistar import exceptions
from apistar.server.components import Component
from project.settings import DATABASES, SECRET_KEY, ALGORITHM, EXPIRY_TIME
from project.helpers import object_id_to_str, remove_object_id


class User(object):
    def __init__(self,
                 _id: str,
                 username: str,
                 groups: list):
        self._id = _id
        self.username = username
        self.groups = groups

    def __str__(self):
        return self.username


class UserComponent(Component):
    def resolve(self, authorization: http.Header) -> User:
        """
        Determine the user associated with a request, using HTTP Token Authentication.
        """
        if authorization is None:
            return None

        scheme, token = authorization.split()
        if scheme.lower() != 'token':
            return None

        try:
            token = jwt.decode(jwt=token, key=SECRET_KEY, algorithm=ALGORITHM)
            user = UserDAO()
            user = user.users.find_one({'_id': ObjectId(token['user'])})
            if user:
                return User(_id=str(user['_id']),
                            username=user['username'],
                            groups=user['groups'])
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return None


class UserDAO():
    client = MongoClient(host=DATABASES['default']['HOST'],
                         port=DATABASES['default']['PORT'])

    db = client[DATABASES['default']['NAME']]
    users = db['users']

    def create(self, user):
        user = remove_object_id(dict(user))
        return self.users.insert_one(user)


    def get_one(self, key, value):
        if key == 'password':
            return exceptions.BadRequest('password key is not allow')
        return object_id_to_str(self.users.find_one({key: value}))


    def get_all(self):
        # return self.users.find({}, {'password': 0})
        return object_id_to_str(self.users.find({}, {'password': 0}), many=True)


    def login(self, username, password):
        user = self.users.find_one({'username': username})
        if user:
            ph = PasswordHasher()
            try:
                if ph.verify(user['password'], password):
                    exp = datetime.utcnow() + timedelta(hours=EXPIRY_TIME)
                    token = jwt.encode(payload={'user': str(user['_id']),
                                                'exp': exp},
                                       key=SECRET_KEY)
                    return {'token': token.decode('UTF-8')}
            except VerifyMismatchError:
                raise exceptions.BadRequest('Incorrect password')
        raise exceptions.NotFound('User not found')
