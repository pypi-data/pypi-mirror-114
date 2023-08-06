from fetching.fetching import Fetching


def fetch(targets: list, token: str = None):
    return Fetching().fetch_and_build(targets, token)
