import json
from typing import List


CONFIG =  json.loads(open(file=".github/minify.json", mode="r").read())


def minify(files: List[str]):
    for minify in files:
        file_from = minify["from"]
        file_to = minify["to"]

        load = []
        open(file=file_to, mode="w").write("")

        for item in file_from:
            item_content = open(file=item, mode="r")
            for line in item_content:
                load.append(line.replace("\n", "").replace("    ", ""))

        for _load in load:
            open(file=file_to, mode="a").write(_load)


if __name__ == "__main__":
    minify(files=CONFIG["css"]["files"])
    minify(files=CONFIG["js"]["files"])
