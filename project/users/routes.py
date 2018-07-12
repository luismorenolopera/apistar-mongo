from apistar import Route
from users.views import list_users, new_user, hello_user, auth


routes = [
    Route('/users/', method='GET', handler=list_users),
    Route('/users/', method='POST', handler=new_user),
    Route('/me/', method='GET', handler=hello_user),
    Route('/login/', method='POST', handler=auth),

]
