import os

# PLANTS
SOIL = 0
BABY_PLANT = 1
MEDIUM_PlANT = 2
BIG_PlANT = 3
HUGE_PlANT = 4

# MODEL PARAMS
SIZE = 3
GROWTH_TIME = 2

# AGENT TYPES
ALTRUISTIC = 0
COOPERATIVE = 1
SELFISH = 2
COMPETITIVE = 3
SADISTIC = 4

# AGENT HAS
NOTHING = 0
PLANT = BABY_PLANT or MEDIUM_PlANT or BIG_PlANT or HUGE_PlANT
SEEDS = 5

# IMAGES
STAR_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/../pictures/star.jpg",
MARKET_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/../pictures/Market2.png",
SOIL_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/../pictures/Soil.png",
SEEDS_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/../pictures/seeds.png",
PLANT1_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/../pictures/Plant1.png",
PLANT2_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/../pictures/Plant2.png",
PLANT3_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/../pictures/Plant3.png",
PLANT4_IMG = f"{os.path.dirname(os.path.realpath(__file__))}/../pictures/Plant4.png",

