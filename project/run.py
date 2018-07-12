from apistar import App, Include
from project.hooks import Cors, MustBeAuthenticated
from users.routes import routes as users_routes
from users.models import UserComponent


routes = [
    Include('', name='users', routes=users_routes),
]

event_hooks = [Cors, MustBeAuthenticated]
components = [UserComponent()]

app = App(routes=routes, event_hooks=event_hooks, components=components)

if __name__ == '__main__':
    app.serve('0.0.0.0', 5000, debug=True)
