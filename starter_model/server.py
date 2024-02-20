import mesa
from model import MoneyModel

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
        elif agent.food == -40:
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
    else:
        portrayal = {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 1, "r": 0.2}
        if agent.food == 20:
            portrayal["r"] = "0.2"
            portrayal["Color"] = "red"
        if agent.food == 10:
            portrayal["r"] = "0.1"
            portrayal["Color"] = "red"
        if agent.food == 0:
            portrayal["Color"] = "grey"
            portrayal["r"] = "0.1"
    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# chart = mesa.visualization.ChartModule([{
#     'Label': 'Gini',
#     'Color': 'Blue'}],
#     data_collector_name='datacollector'
# )

server = mesa.visualization.ModularServer(
    MoneyModel, [grid], "Hungry Agents Model", model_params
)

server.port = 8521  # default
server.launch()
