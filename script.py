import random
import string

import random
import string

def generate_random_string(length: int) -> str:
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return random_string


for _ in range(5):
    print(generate_random_string(10))