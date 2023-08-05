from abc import ABCMeta
from commonroad.scenario.lanelet import LaneletNetwork

__author__ = "Moritz Klischat"
__copyright__ = "TUM Cyber-Physical Systems Group"
__credits__ = ["ZIM Projekt ZF4086007BZ8"]
__version__ = "2021.3"
__maintainer__ = "Moritz Klischat"
__email__ = "commonroad@lists.lrz.de"
__status__ = "Released"


class AbstractScenarioWrapper(metaclass=ABCMeta):
    # these two attributes are abstract and need to be defined by the inheriting subclass
    sumo_cfg_file = ""
    lanelet_network: LaneletNetwork = None
    planning_problem_set = None

