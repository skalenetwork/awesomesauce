import subprocess
from typing import Dict
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from enum import Enum
import random
from transitions import Machine


REGISTER_PERIOD = 10
UNREGISTER_PERIOD = 100


class ValidatorState(Enum) :
    UNREGISTERED = 1
    REGISTERED = 2




class EthAgent(Agent):

    states = ['REGISTERED', "UNREGISTERED"]

    def throw_dice(period):
        return random.random() < 1.0/period;

    def __init__(self, pos, model, agent_type):
        """
         Create a new Schelling agent.

         Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type
        self.machine = Machine(model=self, states = EthAgent.states, initial='UNREGISTERED')
        self.machine.add_transition('register','UNREGISTERED', 'REGISTERED')
        self.machine.add_transition('unregister','REGISTERED', 'UNREGISTERED')


    def run_command(self, contract : str, command: str, params: Dict[str,str] = None):

        cmd_line : list = ["python3", "universal-cli/main.py", contract,
                       command];

        if (params != None) :
            for key, value in params.items():
                cmd_line.append(key)
                cmd_line.append(value)


        print(cmd_line)

        subprocess.run(cmd_line,
                       check=True)

    def do_register(self):
        if not EthAgent.throw_dice(REGISTER_PERIOD):
            return;
        print(f"Registered Validator!")
        self.run_command("validator_service", "registerValidator", {"--help": ""})
        self.model.registered += 1
        self.register()




    def do_unregister(self):
        if not EthAgent.throw_dice(UNREGISTER_PERIOD):
            return;
        self.model.registered -=1
        self.run_command("validator_service", "unregisterValidator", {"--help": ""})
        print(f"Unregistered Validator!")
        self.unregister()

    def do_step(self):
        if self.is_UNREGISTERED() and EthAgent.throw_dice(REGISTER_PERIOD) :
            self.do_register()
            return
        if self.is_REGISTERED() and EthAgent.throw_dice(UNREGISTER_PERIOD) :
            self.do_unregister()
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




