import mesa
import pandas as pd

from model import MyModel

params = {
    "altruistic_agents": 0,
    "cooperative_agents": 1,
    "selfish_agents": 0,
    "competitive_agents": 1,
    "sadistic_agents": 0,
    "plants": 2,
    "width": 10,
    "height": 10,
}

results = mesa.batch_run(
    MyModel,
    parameters=params,
    iterations=15,
    max_steps=500,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)
print("KEYS: ", results_df.keys())

data = []
for i in range(0, 15, 1):
    agent1_death = results_df[(3.9 < results_df['Agent 1']) & (results_df['RunId'] == i)].get('Step').values
    agent2_death = results_df[(3.9 < results_df['Agent 2']) & (results_df['RunId'] == i)].get('Step').values
    agent3_death = results_df[(3.9 < results_df['Agent 3']) & (results_df['RunId'] == i)].get('Step').values
    data.append([agent1_death, agent2_death, agent3_death])

new_results = pd.DataFrame(data)
print("RESULTS: ", new_results)
