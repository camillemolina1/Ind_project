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
Agents need to eat to stay alive. Agents colors represent their social value orientation (selfish, altruistic, sadistic...) 

  Agents can: 
  + move around the grid
  + eat food
  + trade food for seeds at the trading stations
  + plant the seeds on the soil
  + push agents away
  + give agents food

### Model:

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
  
Batch running the model with different parameters allows me to observe patterns in the agents behavior. Currently the batch run is set to run the model 50 times with a max of 500 iterations as I have observed that by that point is the agents are alive they don't ever die. 
  
So far I have observed that cooperative agents do the best, particularlly when there are lots of agents in the simualtion with limited food. The selfish agents also do pretty well however as soon as I add more of them into the model then tend to not do as well as a society. Competitive agents do well on theri own but as soon as I add anyone else to the model they almost always both die. Sadistic agents can lower agent's survival rates but as long as agents survive longer than 40 or so steps the sadistic agent usually dies. Finally altruistic agents that were supposed to help other agents actually seem to be doing the opposite as they get in the way of agents and are constantly taking food and not planting anything. 

  
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



