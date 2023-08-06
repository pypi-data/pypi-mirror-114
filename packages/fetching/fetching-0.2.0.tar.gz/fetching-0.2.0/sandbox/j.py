


a = [
    ["\n hi", "\nho"],
    ["what", "\nwhwy"]
]

b = "\n".join("\n".join(c) for c in a)
print(b)