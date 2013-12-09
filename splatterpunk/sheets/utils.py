from functools import wraps


class LoginError(Exception):
    pass


def logged_in(user_factory):
    def logged_in(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            user = user_factory.create()
            username = user.username
            password = user.username
            if not self.client.login(username=username, password=password):
                raise LoginError
            return f(self, user, *args, **kwargs)
        return wrapper
    return logged_in
