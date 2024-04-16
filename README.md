# Multi-agent Cooperation Project

### Index:
  - [Current version](#current-version)
  - [Context](#context)
  - [How to start](#how-to-start)
  - [Stats](#stats)
  - [Previous versions](#previous-versions)
  - [Past Papers](#past-papers)

## Current version:  
Agents need to eat to stay alive. Agents colors represent their social value orientation (selfish, altruistic, sadistic...) 

Agents can: 
+ move around the grid
+ eat food
+ trade food for seeds at the trading stations
+ plant the seeds on the soil
+ push agents away
+ give agents food

<img src="https://github.com/camillemolina1/Ind_project/assets/98462350/f5b7acfc-315a-4923-8bcf-a0a568db52c5" width=50% height=50%>

### Meanings:

  #### Agents:
  <img src="https://github.com/camillemolina1/Ind_project/assets/98462350/700d48f1-b9f0-4017-8518-61bb318ff845" width=50% height=50%>
  
  #### Plants:
  + Plants now take time to grow  
  + they start off as seeds and get bigger with time (4 sizes possible)   
  + you can see how "big" the plant is by the number of leaves (1 leaf = 1 unit of food for agents)

## Context

### SVO
Social value orientation (SVO) is a measure that corresponds to a combination of weights an individual places on it's own outcome vs others outcome when making a decision.

![image](https://github.com/camillemolina1/Ind_project/assets/98462350/66bef9b5-f011-471c-a72b-6dc2c827c0d5)

  
## How to start

+ Activate python environment
+ Download mesa (if needed)
+ Run server.py
+ A new window should appear at localhost:8521 with visuals
  
  
## Stats
  
To see which settings I should use in terms of the number of agents, food sources, etc.. I ran the simulation a few times and noted down how long the agents were surviving. 
From this I found that in a few cases 1 agent did manage to survive forever with plant size 2. However, generally speaking plants need to be at least of size 3 for agents to be able to survive. 
I also found that with plant size 3, if they start with enough food for them all they will all survive and if they don't (ex: 4 agents and 6 units of food) the amount of survivors changes everytime, generally at least 1 survives but the agents tend to get in each others way which leads to the death of many of them.   
  
[Link to the stats](https://docs.google.com/spreadsheets/d/1qSnYWWC09E4w8XfDHmruH8CnVsvGIsqf_7_NuVMXrPo/edit#gid=0)
  
   
## Previous versions:  

#### Meanings:  
Agents: (Red circle - hungry)  ------>  (Blue circle - fed)   
Food: Green circle (the bigger the more food available)  
Trading stations : Yellow Star  
Soil : Brown squares
  
![image](https://github.com/camillemolina1/Ind_project/assets/98462350/4e634060-9080-4fee-bf0c-759add0ac819)

![image](https://github.com/camillemolina1/Ind_project/assets/98462350/831166e6-39fc-4623-92e0-fe199575db98)
  
![image](https://github.com/camillemolina1/Ind_project/assets/98462350/f47b7578-37c4-481d-b9db-ac4e7961cf49)
  
![image](https://github.com/camillemolina1/Ind_project/assets/98462350/a4ada01c-e829-4026-a1bc-b65bb6d20721)


## Past Papers

+ Open Problems in Cooperative AI by DeepMind - [Paper](https://arxiv.org/pdf/2012.08630.pdf)  
+ UNDERSTANDING THE WORLD TO SOLVE SOCIAL DILEMMAS USING MULTI-AGENT REINFORCEMENT LEARNING - [Paper](https://arxiv.org/pdf/2305.11358.pdf)
+ Learning to cooperate in multi-agent social dilemmas - [Paper](https://www.researchgate.net/publication/221456198_Learning_to_cooperate_in_multi-agent_social_dilemmas)
+ Socially Intelligent Genetic Agents for the Emergence of Explicit Norms - [Paper](https://niravajmeri.github.io/docs/IJCAI22-SIGA.pdf)
+ Too many cooks: Coordinating multi-agent collaboration through inverse planning - [Paper](https://dspace.mit.edu/bitstream/handle/1721.1/138369/0157.pdf?sequence=2&isAllowed=y)



