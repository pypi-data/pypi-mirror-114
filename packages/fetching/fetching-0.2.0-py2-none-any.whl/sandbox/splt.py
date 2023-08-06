
reqs = [
    "one==1.1.0\ntwo~=3.0.1",
    "one==1.1.0\nthree<=2.0.0"
]

"""
want to split each entry to get:

[ 
    ["one=1.1.0", "two~=3.0.1"],
    ["one=1.1.0", "three<=2.0.0"]
]

then want to flatten that array
"""


flt = [item for sublist in reqs for item in sublist.split("\n")]
print(flt)

fltt = "\n".join(list(set([lib for file in reqs for lib in file.split("\n")])))
print(fltt)
