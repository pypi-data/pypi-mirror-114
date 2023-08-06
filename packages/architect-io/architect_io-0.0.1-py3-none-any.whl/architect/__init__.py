from typing import Optional


def say_hello(name: Optional[str] = None):
    if name:
        print(f'Hello, {name}!')
    else:
        print(f'Hello, world!')
