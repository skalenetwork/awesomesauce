import random
import subprocess
from enum import Enum
from typing import Dict

from mesa import Model, Agent
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from transitions import Machine

REGISTER_PERIOD = 100
SET_NAME_PERIOD = 1


class ValidatorState(Enum):
    UNREGISTERED = 1
    REGISTERED = 2


class EthAgent(Agent):
    states = ['REGISTERED', "UNREGISTERED"]

    @staticmethod
    def call_method(o, name: str):
        return getattr(o, name)()

    def set_transitions(self) -> None:
        self.add_transition('register', 'UNREGISTERED', 'REGISTERED',
                            "validator_service", "registerValidator", REGISTER_PERIOD)
        self.add_transition('set_name', 'REGISTERED', 'REGISTERED', "validator_service", "setValidatorName",
                            SET_NAME_PERIOD)

    transitionsToPeriods: Dict[str, float] = {}
    transitionsToContracts: Dict[str, str] = {}
    transitionsToCommands: Dict[str, str] = {}

    @staticmethod
    def throw_dice(period: float) -> bool:
        return random.random() < 1.0 / period

    def add_transition(self, transition: str, state: str, next_state: str,
                       contract: str, command: str, period: float) -> None:
        self.machine.add_transition(transition, state, next_state)
        self.transitionsToPeriods[transition] = period
        self.transitionsToContracts[transition] = contract
        self.transitionsToCommands[transition] = command

    def __init__(self, pos, model, agent_type):

        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type
        self.machine = Machine(model=self, states=EthAgent.states, initial='UNREGISTERED')
        self.set_transitions()

    def maybe_run_command(self, transition: str, params: Dict[str, str] = None) -> bool:

        if not EthAgent.throw_dice(self.transitionsToPeriods[transition]):
            return False

        cmd_line: list = ["python3", "universal-cli/main.py", self.transitionsToContracts[transition],
                          self.transitionsToCommands[transition]]

        if params is not None:
            for key, value in params.items():
                cmd_line.append(key)
                if len(value) > 0:
                    cmd_line.append(value)

        print("")
        print(cmd_line)

        subprocess.run(cmd_line,
                       check=True)

        return True

    def do_transition(self, transition: str) -> None:
        if not self.maybe_run_command(transition, {"--help": ""}):
            return
        self.model.registered += 1
        EthAgent.call_method(self, transition)

    def do_register(self) -> None:
        do_transition
        if not self.maybe_run_command("register", {"--help": ""}):
            return
        self.model.registered += 1
        EthAgent.call_method(self, "register")

    def do_setname(self):
        if not self.maybe_run_command("set_name", {"--help": ""}):
            return
        self.set_name()

    def do_step(self):
        if self.state == "UNREGISTERED":
            self.do_register()
            self.model.registered += 1
            return
        if self.state == "REGISTERED":
            self.do_setname()
            return

    def step(self):

        self.do_step()

        similar = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1

        # If unhappy, move:
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1


class Network(Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, height=20, width=20, density=0.8, minority_pc=0.2, homophily=3):
        """
        """

        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.happy = 0
        self.registered = 0
        self.datacollector = DataCollector(
            {"happy": "happy"},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_pc:
                    agent_type = 1
                else:
                    agent_type = 0

                agent = EthAgent((x, y), self, agent_type)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False
