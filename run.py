import argparse
import random

from app.utils.layout import Layout
from app.pacman.domain.player import PlayerAgent
from app.pacman.domain.ghost import RandomGhost
from app.pacman.domain.rules import GameRules
from app.pacman.graphics.ui import UI
from app.pacman.graphics.display import PacmanGraphics
from app.pacman.search.pacman import PacmanSearchProblem


def parse_args():
    parser = argparse.ArgumentParser(description="Pacman Game")

    parser.add_argument(
        "-l",
        "--layout",
        help="file from which to load the map layout",
        default="mediumClassic",
    )
    parser.add_argument(
        "-k",
        "--num-ghosts",
        type=int,
        help="The maximum number of ghosts to use",
        default=10,
    )
    parser.add_argument(
        "-z",
        "--zoom",
        type=float,
        help="Zoom the size of the graphics window",
        default=1.0,
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="Fixes the random seed to always play the same game",
    )
    parser.add_argument(
        "--frame-time",
        type=float,
        help="Time to delay between frames; <0 means keyboard",
        default=0.12
    )
    parser.add_argument(
        "-a",
        "--auto-pilot",
        action="store_true",
        help="Whether Pacman will be controlled by the algorithm",
        default=False,
    )

    options, args = parser.parse_args(), {}
    if options.seed is not None:
        random.seed(options.seed)

    if (layout := Layout.get_layout(options.layout)) is None:
        raise Exception(f"The layout {options.layout} cannot be found")
    else: args["layout"] = layout

    args["pacman_agent"] = PlayerAgent()
    args["ghost_agents"] = [RandomGhost(i + 1) for i in range(options.num_ghosts)]
    args["display"] =  PacmanGraphics(UI(), zoom=options.zoom, frame_time=options.frame_time)
    
    if options.auto_pilot:
        search = PacmanSearchProblem()
        args["pacman_search"] = search
    
    return args


if __name__ == "__main__":
    args = parse_args()
    game = GameRules.new_game(**args)
    game.run()
