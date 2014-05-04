# !/usr/bin/env python
import argparse
import sys

from core.runner import Runner

from logger.csv_logger import CsvLogger
from logger.console_logger import ConsoleLogger

from satellite.world.satellite_world import SatelliteWorld

from satellite.predictor.satellite_phi_predictor import SatellitePhiPredictor

from satellite.guard.satellite_guard import SatelliteGuard

from satellite.config import runner_config, logger_config, predictor_config, world_config


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('init_phi', type=int, help='starting phi position')
    parser.add_argument('--log', help='path to log file')
    parser.add_argument('--learn', action='store_const', const=True,
                        help='enable learning')
    parser.add_argument('--world',
                        help='world type',
                        choices=['satellite'],
                        default="satellite")
    parser.add_argument('--guard',
                        help='guard type',
                        choices=['satellite'],
                        default="satellite")

    args = parser.parse_args()

    predictor = SatellitePhiPredictor(predictor_config)

    if args.world == "satellite":
        world = SatelliteWorld(world_config)
    else:
        print "no such world"
        exit

    if args.guard == "satellite":
        guard = SatelliteGuard()
    else:
        guard = None

    runner = Runner(runner_config,
                    world, predictor,
                    guard=guard,
                    learning_enabled=args.learn)

    runner.addLogger(ConsoleLogger(logger_config))
    if args.log:
        runner.addLogger(CsvLogger(logger_config, args.log))

    world.setup()
    world.setInitPhi(args.init_phi)

    runner.newRun()

    while True:
        try:
            runner.tick()

        except Exception as e:
            print e
            runner.world.terminate()
            sys.exit()
