
from functools import wraps

def assert_imports(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ModuleNotFoundError as err:
            print("Tip: Run `pip install feyn[extras]` to get all extra dependencies.")
            err.msg += f"\nYou can also install feyn[extras] to get all dependencies `pip install feyn[extras]`."
            raise err

    return wrapper
