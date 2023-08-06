import time

#from src.json_memoize.json_memoize import JsonMemoize
from json_memoize import JsonMemoize

jm = JsonMemoize(app_name = "test_class")
memoize = jm.memoize_with_defaults

@memoize(max_age = 30)
def test_function(*args, **kwargs):
    time.sleep(3)
    return "thanks!"

print(test_function("this is a test"))

