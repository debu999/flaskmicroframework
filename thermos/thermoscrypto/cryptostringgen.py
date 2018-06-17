"""This module is meant to provide a random string which
comprises of ascii uppercase and digits to be used as a secret key.
No seed is stored thus it is almost random to use."""

import string
import random


def id_generator(size=24, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def staticid_generator(hostname, ipaddr, dt, port, flname):
    return hostname+dt+ipaddr+port+flname

if __name__ == "__main__":
    print(id_generator())
    print(id_generator(25, "6793YUIO"))
