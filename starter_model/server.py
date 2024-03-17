import mesa
import os
from mesa_viz_tornado.modules import ChartModule
from model import MyModel
from agents import Plant, BasicAgent, TradingMarket, Soil

STAR_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/star.jpg",
MARKET_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/Market.png",
SOIL_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/Soil.png"
PLANT_1_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/Plant1.png",
PLANT_2_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/Plant2.png",
PLANT_3_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/Plant3.png",
PLANT_4_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/pictures/Plant4.png",

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
    "S": mesa.visualization.Slider(
        "Amount of food supply in a plant",
        2,
        1,
        4,
        1,
        description="Choose how big the food sources are",
    ),
    "width": 10,
    "height": 10,
}


def agent_portrayal(agent):
    if isinstance(agent, TradingMarket):
        portrayal = {"Shape": MARKET_IMG, "Color": "yellow", "Filled": "true", "Layer": 0, "r": 0.2}
    elif isinstance(agent, Soil) and agent.contains == 0:
        portrayal = {"Shape": SOIL_IMG, "Color": "brown", "Filled": "true", "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, BasicAgent):
        portrayal = {"Shape": "circle", "Color": "blue", "Filled": "true", "Layer": 1, "r": 0.5}
        if agent.hunger <= 0:
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
        elif agent.hunger == 4:
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 0
    elif isinstance(agent, Plant):
        portrayal = {"Shape": "circle", "Color": "green", "Filled": "true", "Layer": 1, "r": 0.5}
        if agent.supply == 4:
            portrayal["Shape"] = PLANT_4_IMG
            portrayal["r"] = "1"
        if agent.supply == 3:
            portrayal["Shape"] = PLANT_3_IMG
            portrayal["r"] = "0.75"
        if agent.supply == 2:
            portrayal["Shape"] = PLANT_2_IMG
            portrayal["r"] = "0.5"
        if agent.supply == 1:
            portrayal["Shape"] = PLANT_1_IMG
            portrayal["r"] = "0.25"
        if agent.supply == 0:
            portrayal["Shape"] = SOIL_IMG
            portrayal["r"] = "0.0"
    else:
        portrayal = {"Shape": "circle", "Color": "brown", "Filled": "true", "Layer": 0, "r": 1}
    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)

count_chart = ChartModule(
    [{"Label": "Agent_count", "Color": "#21A2EC"}, {"Label": "Food_count", "Color": "#EC4521"}],
    data_collector_name="count_chart"
)

hunger_level_chart = ChartModule(
    [{"Label": "Agent 1", "Color": "#EC4521"}, {"Label": "Agent 2", "Color": "#21A2EC"},
     {"Label": "Agent 3", "Color": "#24D339"}, {"Label": "Agent 4", "Color": "#EDDE47"},
     {"Label": "Agent 5", "Color": "#ED47E3"}], data_collector_name="hunger_levels"
)


server = mesa.visualization.ModularServer(
    MyModel, [grid, hunger_level_chart, count_chart], "Hungry Agents Model", model_params
)

server.port = 8521  # default
server.launch()
