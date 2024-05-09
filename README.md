# Multi-agent Cooperation Project

### Index:
  - [Current version](#current-version)
    - [Model](#model)
    - [Meanings](#meanings)
  - [Context](#context)
    - [SVO](#svo)
  - [How to start](#how-to-start)
  - [Stats](#stats)
  - [Previous versions](#previous-versions)
  - [Past Papers](#past-papers)

## Current version:  
Agents need to eat to stay alive. Agents colors represent their social value orientation (selfish, altruistic, sadistic...). Agents can however change their svo value to selfish if they are cooperative and believe the entire population is not going to cooperate or they are competitive and they believe no one is competing against them. Agents can now also send other agents to "prison"

  Agents can: 
  + move around the grid
  + eat food
  + trade food for seeds at the trading stations
  + plant the seeds on the soil
  + push agents away
  + give agents food

### Model:
  
<img src="https://github.com/camillemolina1/Ind_project/assets/98462350/5c3f08ac-84d3-4a10-8f12-f4e47147845d" width=50% height=50%>

### Meanings:

  #### Agents:
    
  <img src="https://github.com/camillemolina1/Ind_project/assets/98462350/700d48f1-b9f0-4017-8518-61bb318ff845" width=50% height=50%>
  
  #### Plants:
  + Plants now take time to grow  
  + they start off as seeds and get bigger with time (4 sizes possible)   
  + you can see how "big" the plant is by the number of leaves (1 leaf = 1 unit of food for agents)

  #### Gate:
  The gate is removable and serves as a "prison" for agents that are behaving in a way that only serves themselves. Agents can be sent there and brought back by altruistic, cooperative and selfish   agents if they think they have changed their svo and are ready to cooperate.

## Context

### SVO
Social value orientation (SVO) is a measure that corresponds to a combination of weights an individual places on it's own outcome vs others outcome when making a decision.

![image](https://github.com/camillemolina1/Ind_project/assets/98462350/66bef9b5-f011-471c-a72b-6dc2c827c0d5)

  
## How to start

+ Activate python environment
+ Download mesa (if needed)
+ Run server.py
+ A new window should appear at localhost:8521 with visuals
  
## Previous versions:  

<img src="https://github.com/camillemolina1/Ind_project/assets/98462350/f5b7acfc-315a-4923-8bcf-a0a568db52c5" width=48% height=48%>

#### Meanings:  
Agents: (Red circle - hungry)  ------>  (Blue circle - fed)   
Food: Green circle (the bigger the more food available)  
Trading stations : Yellow Star  
Soil : Brown squares
   
![image](https://github.com/camillemolina1/Ind_project/assets/98462350/4e634060-9080-4fee-bf0c-759add0ac819)

![image](https://github.com/camillemolina1/Ind_project/assets/98462350/831166e6-39fc-4623-92e0-fe199575db98)
  
![image](https://github.com/camillemolina1/Ind_project/assets/98462350/f47b7578-37c4-481d-b9db-ac4e7961cf49)
  
![image](https://github.com/camillemolina1/Ind_project/assets/98462350/a4ada01c-e829-4026-a1bc-b65bb6d20721)
