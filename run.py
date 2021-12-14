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
from app.pacman.rl.config import DQNAgentConfig
from app.pacman.rl.dqn.configs.model import ModelConfig
from app.pacman.rl.dqn.configs.dqn import DQNConfig
from app.pacman.rl.config import EpsParams
from app.pacman.rl.agents import DQNAgent


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
    
    args = {"num_games": int(1e5) }

    args["ghost_agents"] = [RandomGhost(i + 1) for i in range(options.num_ghosts)]
    args["display"] =  PacmanGraphics(UI(), zoom=options.zoom, frame_time=options.frame_time)
    args["log_path"] = options.log_path

    layout_params = {
        "width": 32,
        "height": 32,
        "num_food": 25,
        "num_ghosts": 1,
    }

    agent_config = DQNAgentConfig(
        model=ModelConfig(
            dqn=DQNConfig(
                width=32,
                height=32,
                in_channels=4,
                out_features=4,
            ),
            memory=10000,
            lr=2e-4,
            batch_size=64,
            gamma=0.999,
            update_step=200,
            device="cpu",
            train_start=2000,
            model_path="app/pacman/rl/dqn/trained/checkpoint.tar.pth",
        ),
        eps_params=EpsParams(start=0.9, end=0.05, step=10000),
        train=True,
    )
    args["pacman_agent"] = DQNAgent(agent_config)
    
    return args, layout_params

def generate_layout(params) -> Layout:
    maze = MazeGenerator.generate(
        height=params["height"],
        width=params["width"],
        num_food=params["num_food"],
        num_ghosts=params["num_ghosts"],
        num_capsules=0,
    )
    layout = Layout.from_text(maze)
    return layout


if __name__ == "__main__":
    args, layout_params = parse_args()
    num_games = args.pop("num_games")

    for idx in range(num_games):
        args["layout"] = generate_layout(layout_params)
        game = GameRules.new_game(**args)
        game.run()
