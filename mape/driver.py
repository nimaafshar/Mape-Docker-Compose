import logging
import sys

import yaml
from logging import getLogger

from mape.utils import Factory, BASE_PATH
from mape.cycle.mape import MAPECycle

from prometheus_client import start_http_server

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(message)s')
logger = getLogger()


def main():
    start_http_server(8000)
    with open(BASE_PATH / 'config' / 'config.yaml', 'r') as config_file:
        total_config: dict = yaml.load(config_file, Loader=yaml.SafeLoader)
    logger.info(f"configuration loaded from {(BASE_PATH / 'config' / 'config.yaml').absolute()}.")
    factory: Factory = Factory(total_config)
    cycle: MAPECycle = MAPECycle(
        factory.get_hybrid_monitoring(),
        factory.get_hybrid_analysis(),
        factory.get_hybrid_planning(),
        factory.get_scaling_execution(),
        factory.get_mape_interval()
    )
    cycle.run()


if __name__ == "__main__":
    main()
