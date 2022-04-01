import yaml
from logging import getLogger

from utils import Factory, BASE_PATH
from cycle import MAPECycle

logger = getLogger()


def main():
    with open(BASE_PATH / 'config.yaml', 'r') as config_file:
        total_config: dict = yaml.load(config_file, Loader=yaml.SafeLoader)
    logger.info('configuration loaded.')
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
