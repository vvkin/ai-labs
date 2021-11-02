import argparse
import random
from app.pacman.multiagent.agents import ExpectimaxAgent, MinimaxAgent
from app.pacman.search.agents import AllFoodAgent, PositionAgent
from app.utils.layout import Layout, MazeGenerator
from app.pacman.domain.player import PlayerAgent
from app.pacman.domain.ghost import GreedyGhost, RandomGhost
from app.pacman.domain.rules import GameRules
from app.pacman.graphics.ui import UI
from app.pacman.graphics.display import PacmanGraphics


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
        help="the maximum number of ghosts to use",
        default=10,
    )
    parser.add_argument(
        "-z",
        "--zoom",
        type=float,
        help="zoom the size of the graphics window",
        default=1.0,
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="fixes the random seed to always play the same game",
    )
    parser.add_argument(
        "--frame-time",
        type=float,
        help="time to delay between frames; <0 means keyboard",
        default=0.12
    )
    parser.add_argument(
        "-a",
        "--auto-pilot",
        action="store_true",
        help="whether Pacman will be controlled by the algorithm",
        default=False,
    )
    parser.add_argument(
        '-g',
        '--generate-maze',
        action="store_true",
        help="whether generate maze or not",
        default=False
    )
    parser.add_argument(
        '--log-path',
        type=str,
        default='logs/stats.csv',
        help="path to logs file"
    )

    options, args = parser.parse_args(), {}
    if options.seed is not None:
        random.seed(options.seed)
    
    if options.generate_maze:
        maze = MazeGenerator.generate(
            height=15,
            width=15,
            num_food=5,
            num_capsules=3, num_ghosts=2,
        )
        layout = Layout.from_text(maze)
    else: layout = Layout.get_layout(options.layout)

    if options.auto_pilot:
        player_agent = MinimaxAgent() #PositionAgent(layout.food.get_points()[0]) #AllFoodAgent()
    else: player_agent = PlayerAgent()
 
    args["layout"] = layout
    args["pacman_agent"] = player_agent
    args["ghost_agents"] = [MinimaxAgent(i + 1) for i in range(options.num_ghosts)]
    args["display"] =  PacmanGraphics(UI(), zoom=options.zoom, frame_time=options.frame_time)
    args["log_path"] = options.log_path
    
    return args


if __name__ == "__main__":
    args = parse_args()
    game = GameRules.new_game(**args)
    game.run()
