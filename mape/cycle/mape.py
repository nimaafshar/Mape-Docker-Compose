from ..monitoring import Monitoring, MonitoringData
from ..analysis import Analysis, AnalysisData
from ..analysis.exceptions import DataInsufficiencyException
from ..planning import Planning, PlanningData
from ..execution import Execution, ExecutionData

import signal
import datetime
from logging import getLogger
from typing import Optional

logger = getLogger()


class MAPECycle:
    """
    MAPE Cycle consists of 4 steps: monitoring, analysis, planning, execution
    """

    class GracefulKiller:
        kill_now = False

        def __init__(self):
            signal.signal(signal.SIGINT, self.exit_gracefully)
            signal.signal(signal.SIGTERM, self.exit_gracefully)

        def exit_gracefully(self, *args):
            logger.info('waiting for cycle to be ended before exiting gracefully.')
            self.kill_now = True

    def __int__(self,
                monitoring_step: Monitoring, analysis_step: Analysis, planning_step: Planning,
                execution_step: Execution, interval: datetime.timedelta):
        self._monitoring: Monitoring = monitoring_step
        self._analysis: Analysis = analysis_step
        self._planning: Planning = planning_step
        self._execution: Execution = execution_step
        self._interval: datetime.timedelta = interval

    def run(self):
        """
        running mape cycle
        """
        monitoring_input: Optional[ExecutionData] = None
        killer = MAPECycle.GracefulKiller()
        cycle: int = 0
        while not killer.kill_now:
            logger.info('mape cycle started.')
            try:
                analysis_input: Optional[MonitoringData] = self._monitoring.update(cycle, monitoring_input)
                planning_input: Optional[AnalysisData] = self._analysis.update(cycle, analysis_input)
                execution_input: Optional[PlanningData] = self._planning.update(cycle, planning_input)
                monitoring_input = self._execution.update(cycle, execution_input)
            except DataInsufficiencyException as e:
                logger.error(f'DataInsufficiencyException {e}')
                logger.info(f'skipping cycle {cycle}')
            cycle += 1
        logger.info('mape cycle ended.')
