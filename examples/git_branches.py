import git, json

REPO_PATH = "/home/jamalex/fle/ka-lite"
REMOTE_NAME = "upstream"

repo = git.Repo(REPO_PATH)

repo.git.remote("update", REMOTE_NAME)

# branches = [b.name for b in repo.branches]
branches = [b for b in repo.git.branch(r=True).split("\n  ") if b.startswith(REMOTE_NAME + "/")]
branch_names = [b.split("/")[-1] for b in branches]
counts = [int(repo.git.rev_list(b, count=True)) for b in branches]

sets = [{"label": b, "size": c} for b, c in zip(branch_names, counts)]
overlaps = []

for i in range(len(branches)):
    for j in range(i+1, len(branches)):
        c = int(repo.git.rev_list(branches[i], "^" + branches[j], count=True))
        overlaps.append({"sets": [i, j], "size": counts[i] - c, "label": branch_names[i] + "/" + branch_names[j], "branch1": branch_names[i], "branch2": branch_names[j]})

with open("git_branches.jsonp", "w") as f:
    f.write("var sets = %s; \n\n" % json.dumps(sets))
    f.write("var overlaps = %s;" % json.dumps(overlaps))
