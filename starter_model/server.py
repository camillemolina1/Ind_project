import mesa

from agent import MoneyAgent
from model import MoneyModel
from mesa.visualization.UserParam import Slider


FOOD = 0
AGENT = 1


model_params = {
    "N": mesa.visualization.Slider(
        "Number of agents",
        3,
        1,
        5,
        1,
        description="Choose how many agents to include in the model",
    ),
    "F": mesa.visualization.Slider(
        "Number of food sources",
        2,
        1,
        5,
        1,
        description="Choose how many food sources to include in the model",
    ),
    "width": 10,
    "height": 10,
}


def agent_portrayal(agent):
    if agent.type == AGENT:
        portrayal = {"Shape": "circle", "Color": "green", "Filled": "true", "Layer": 0, "r": 0.5}
        if agent.food > 0:
            portrayal["Color"] = "green"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
    else:
        portrayal = {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 1, "r": 0.2}
    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = mesa.visualization.ModularServer(
    MoneyModel, [grid], "Money Model", model_params
)

server.port = 8521  # default
server.launch()
