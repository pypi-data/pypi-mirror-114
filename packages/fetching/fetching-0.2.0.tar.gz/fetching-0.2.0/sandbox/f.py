from fetching import Fetching


f = Fetching()
targets = [
    {
        "name": "nthparty/fetching",
        "files": ["fetching/fetching.py"],
        "ref": "055ad6af491f5cd7d308f4fbc5c32852d8748f59"
    },
    {
        "name": "nthparty/oblivious",
        "files": ["oblivious/oblivious.py", "test/test_oblivious.py"],
        "ref": "daa92da7197cdcd5dfc89854fa1b672f37096e74"
    },
    {
        "name": "nthparty/progress-tracker",
        "files": ["progress.py"]
    }
]

c = f.fetch_source(targets, "050886f9de266fddeb2ff1b23c8e0b217741942b")
b = f.build_dependencies(c)
f.write("/Users/ben/Desktop/dev/NTH/fetching/test/fixtures/source/fetch_multiple_by_ref.txt", b)
print("hi")