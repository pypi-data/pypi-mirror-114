from github import Github

token = "050886f9de266fddeb2ff1b23c8e0b217741942b"
g = Github(token)
r = g.get_repo("multiparty/oprf")

t = r.get_tags()
for tt in t:
    print(tt)

rr = r.get_releases()
for rrr in rr:
    print(rrr)
    a = rrr.get_assets()
    for aa in a:
        print(aa)
    print("hi")

# c = r.get_contents("rust_examples_cli/src/main.rs", ref="03c837a70a9b6b98839120bb4ffaf093d9a412e6")
# d = c.decoded_content.decode("utf-8")

print("hi")