from classes import *


class Services:

    @staticmethod
    def pull_methods():
        a = globals()
        print(a)


if __name__ == "__main__":

    s = Services()
    s.pull_methods()
