import random

import mesa
import pandas as pd

from model import MyModel


params = {
    "altruistic_agents": 0,
    "cooperative_agents": 1,
    "selfish_agents": 1,
    "competitive_agents": 1,
    "sadistic_agents": 0,
    "plants": 3,
    "width": 10,
    "height": 10,
}
print(params)

results = mesa.batch_run(
    MyModel,
    parameters=params,
    iterations=50,
    max_steps=500,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)
print("KEYS: ", results_df.keys())

data = []
for i in range(0, 50):
    agent1_death = results_df[(3.9 < results_df['Agent 1']) & (results_df['RunId'] == i)].get('Step').values
    if len(agent1_death) > 0:
        agent1_death = agent1_death[len(agent1_death) - 1]
    agent2_death = results_df[(3.9 < results_df['Agent 2']) & (results_df['RunId'] == i)].get('Step').values
    if len(agent2_death) > 0:
        agent2_death = agent2_death[len(agent2_death) - 1]
    agent3_death = results_df[(3.9 < results_df['Agent 3']) & (results_df['RunId'] == i)].get('Step').values
    if len(agent3_death) > 0:
        agent3_death = agent3_death[len(agent3_death) - 1]
    agent4_death = results_df[(3.9 < results_df['Agent 4']) & (results_df['RunId'] == i)].get('Step').values
    if len(agent4_death) > 0:
        agent4_death = agent4_death[len(agent4_death) - 1]
    agent5_death = results_df[(3.9 < results_df['Agent 5']) & (results_df['RunId'] == i)].get('Step').values
    if len(agent5_death) > 0:
        agent5_death = agent5_death[len(agent5_death) - 1]
    data.append([agent1_death, agent2_death, agent3_death, agent4_death, agent5_death])

new_results = pd.DataFrame(data)
print("RESULTS: ", new_results)
