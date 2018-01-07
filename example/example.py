from parser.config import Config

import os

os.remove("example.db")

Config(
    tex_filename="example.tex",
    config_filename="config.yml"
)

exit(0)

