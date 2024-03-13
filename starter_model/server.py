import mesa
import os
from model import MyModel
from agents import Food, BasicAgent, Goal, Soil

STAR_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/star.jpg",
SOIL_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/soil.jpg",
APPLE_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/apple.jpg",
HALF_EATEN_APPLE_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/half_eaten_apple.jpg",
EATEN_APPLE_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/eaten_apple.jpg",

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
    if isinstance(agent, Goal):
        portrayal = {"Shape": STAR_IMG, "Color": "yellow", "Filled": "true", "Layer": 0, "r": 0.2}
    elif isinstance(agent, Soil):
        portrayal = {"Shape": "rect", "Color": "brown", "Filled": "true", "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, BasicAgent):
        portrayal = {"Shape": "circle", "Color": "green", "Filled": "true", "Layer": 1, "r": 0.5}
        if agent.hunger <= 0:
            portrayal["Color"] = "green"
            portrayal["Layer"] = 0
        elif agent.hunger == 4:
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
    elif isinstance(agent, Food):
        portrayal = {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 1, "r": 0.5}
        if agent.supply == 2:
            portrayal["r"] = "0.5"
        if agent.supply == 1:
            portrayal["r"] = "0.25"
        if agent.supply == 0:
            portrayal["r"] = "0.0"
    else:
        portrayal = {"Shape": "circle", "Color": "purple", "Filled": "true", "Layer": 0, "r": 1}
    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)


server = mesa.visualization.ModularServer(
    MyModel, [grid], "Hungry Agents Model", model_params
)

server.port = 8521  # default
server.launch()
