# Butterly_Population_Simulation
An inquiry into dynamic changes to the population of butterflies given initial resource (food, population, growth rate, etc) allocation.

This project is a python implementation of a commonly used population dynamic model (often shown on the example of population of foxes vs. rabbits).

This model assumes the following initial condition:
* grid_width - the width of the simulation grid
* grid_height - the height of the simulation grid
* initial_sc - inital population of small caterpillars
* initial_mc - initial population of medium caterpillars
* initial_lc - inital population of large caterpillars
* initial_leaves - initial population of leaves (food)
* ticks - how many steps the simulation is ran
* sc_hunger_death_prob - the probabily of small caterpillar dying from hunger
* mc_hunger_revert_prob - the probability of a medium caterpillar becoming small from hunger
* lc_to_butterfly_prob - the probability of large caterpillar becoming a butterly upon eating
* lc_hunger_revert_prob - the probability of large caterpillar becomming medium caterpillar when hungry
* leaf_generation_prob - the probability of any empty cell to generate a leaf
* butterfly_sc_prob - the probability of a butterly leaving behind a small caterpillar
* butterfly_death_prob - probability of any caterpillar dying
