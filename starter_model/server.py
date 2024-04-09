import mesa
from mesa_viz_tornado.modules import ChartModule
import variables as v
import agents as a
from model import MyModel, Plant, TradingMarket


MODEL_PARAMS = {
    "altruistic_agents": mesa.visualization.Slider(
        "Number of altruistic agents",
        0,
        0,
        5,
        1,
        description="Choose how many altruistic agents to include in the model",
    ),
    "cooperative_agents": mesa.visualization.Slider(
        "Number of cooperative agents",
        1,
        0,
        5,
        1,
        description="Choose how many cooperative agents to include in the model",
    ),
    "selfish_agents": mesa.visualization.Slider(
        "Number of selfish agents",
        1,
        0,
        5,
        1,
        description="Choose how many selfish agents to include in the model",
    ),
    "competitive_agents": mesa.visualization.Slider(
        "Number of competitive agents",
        1,
        0,
        5,
        1,
        description="Choose how many competitive agents to include in the model",
    ),
    "sadistic_agents": mesa.visualization.Slider(
        "Number of sadistic agents",
        0,
        0,
        5,
        1,
        description="Choose how many sadistic agents to include in the model",
    ),
    "plants": mesa.visualization.Slider(
        "Number of food sources / plants",
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
    if isinstance(agent, TradingMarket):
        portrayal = {"Shape": v.MARKET_IMG, "Color": "yellow", "Filled": "true", "Layer": 0, "r": 0.2}
    elif isinstance(agent, a.BasicAgent):
        portrayal = {"Shape": "circle", "Color": "blue", "Filled": "true", "Layer": 1, "r": 0.5}
        if isinstance(agent, a.AltruisticAgent):
            portrayal["Color"] = "blue"
        elif isinstance(agent, a.CooperativeAgent):
            portrayal["Color"] = "green"
        elif isinstance(agent, a.SelfishAgent):
            portrayal["Color"] = "yellow"
        elif isinstance(agent, a.SpitefulAgent):
            portrayal["Color"] = "orange"
        elif isinstance(agent, a.SadisticAgent):
            portrayal["Color"] = "red"
        if agent.hunger > 3:
            portrayal["r"] = 0.25
    elif isinstance(agent, Plant):
        portrayal = {"Shape": "circle", "Color": "green", "Filled": "true", "Layer": 1, "r": 0.5}
        if agent.size == 5:
            portrayal["Shape"] = v.SEEDS_IMG
            portrayal["r"] = "0.1"
        elif agent.size == 4:
            portrayal["Shape"] = v.PLANT4_IMG
            portrayal["r"] = "1"
        elif agent.size == 3:
            portrayal["Shape"] = v.PLANT3_IMG
            portrayal["r"] = "0.75"
        elif agent.size == 2:
            portrayal["Shape"] = v.PLANT2_IMG
            portrayal["r"] = "0.5"
        elif agent.size == 1:
            portrayal["Shape"] = v.PLANT1_IMG
            portrayal["r"] = "0.25"
        else:
            portrayal["Shape"] = v.SOIL_IMG
            portrayal["r"] = "1"
            portrayal["Color"] = "Brown"
    else:
        portrayal = {"Shape": "circle", "Color": "white", "Filled": "true", "Layer": 0, "r": 1}
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
    MyModel, [grid, hunger_level_chart, count_chart], "Hungry Agents Model", MODEL_PARAMS
)

server.port = 8521  # default
server.launch()
