import re
filename = "input.txt"

# This compiles your input file to a mermaid markdown file.
# With this, part 2 is faster done by hand
with open(filename, "r") as in_f:
    with open(filename[:-3] + "mmd", "w") as out_f:
        out_f.write("flowchart TB\n")
        for li in in_f:
            if "%" in li:
                li = li.replace("%", "    ")
            elif "&" in li:
                mat = re.match(r"&(\S+)", li)
                name = mat.groups()[0]
                li = li.replace(mat[0], "    " + name + "{'" + name + "'}")
            else:
                li = li.replace("broadcaster ", "    broadcaster(broadcaster) --")
            li = li.replace(", ", " & ")
            li = li.replace(" -> ", " --> ")
            out_f.write(li)