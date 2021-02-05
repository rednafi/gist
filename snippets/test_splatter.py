from .splatter import *

cli = CLI(Splatter)
cli.entrypoint(argv=['--json={"hello": "world"}'])
