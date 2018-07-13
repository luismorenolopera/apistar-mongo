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
        Determina el usuario asociado con una peticion, usando Token de autenticacion
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
        """
            crea un usuario y retorna los datos del usuario creado
        """
        user = remove_object_id(dict(user))
        try:
            new_user = self.users.insert_one(user).inserted_id
        except Exception as e:
            raise exceptions.BadRequest('resource not created')
        new_user = self.users.find_one({'_id':new_user})
        return object_id_to_str(new_user)


    def get_one(self, key, value):
        """
            obtiene un usuario dada una llave y un valor,
            en caso de pasar la llave con el nombre password lanzara
            una exepcion
        """
        if key == 'password':
            raise exceptions.BadRequest('password key is not allow')
        return object_id_to_str(self.users.find_one({key: value}))


    def get_all(self):
        """
            obtiene todos los usuarios con sus respectivos datos,
            exepto contraseña
        """
        return object_id_to_str(self.users.find({}, {'password': 0}), many=True)


    def login(self, username, password):
        """
            comprueba usuario y contraseña y retorna un token con tiempo
            de expiracion
        """
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
