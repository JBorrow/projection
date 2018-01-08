from parser.config import Config

import os

os.remove("example.db")

config = Config(
    tex_filename="example.tex",
    config_filename="config.yml"
)

with open("example.md", "w") as file:
    file.write("\n".join(config.parser.text))

exit(0)

