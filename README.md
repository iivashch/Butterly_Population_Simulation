# Butterly_Population_Simulation
An inquiry into dynamic changes to the population of butterflies given initial resource (food, population, growth rate, etc) allocation.

This project is a python implementation of a commonly used population dynamic model (often shown on the example of population of foxes vs. rabbits).

### Motivation:
In nature some caterpillar species of caterpillars feed on poisonous species of leaves making themselves protected from otherwise natural preditors, which refuse to eat poisoned food. However, such leaves are a rare commodity, and is often not enought for all caterpillars. Thus, in order to survive, caterpillars often need to canibalize on their siblings.

### Operation:
The model works on a principle of random interractions. Probabilities are used as a measure of time. E.g. if a probability of a leaf appearing is set to 0.25 (25%) then, on average, we can expect the leaf to appear after 4 steps (ticks) of the simulation. Thus, in a way mimicing the leaf growing for four days. In practice this only works over large time frames (thus 1000 steps of the simulation as a default value). Similarly, the caterpillars and butterflies also behave in probabilities ways. In particular, each step of the model caterpillars and butterlies are moving to one randomly selected adjacent cell (four cardinal directions + the diagonals).

### Mechanics:
Caterpillars are hungry at each step, if they find a leaf they will move to that leaf to consume it. If no leaf is found, they consume a smaller caterpillar. If no food (leaves or caterpillars) is found, they remain hungry and run a risk of becoming weak (smaller if they are medium or large catterpillar) or dying (if they are small caterpillar).


This model assumes the following initial condition, initial quantities are shows in parenthesis:
* grid_width(15) - the width of the simulation grid
* grid_height(15) - the height of the simulation grid
* initial_sc(10) - inital population of small caterpillars
* initial_mc(5) - initial population of medium caterpillars
* initial_lc(3) - inital population of large caterpillars
* initial_leaves(15) - initial population of leaves (food)
* ticks(1000) - how many steps the simulation is ran
* sc_hunger_death_prob(0.01) - the probabily of small caterpillar dying from hunger
* mc_hunger_revert_prob(0.03) - the probability of a medium caterpillar becoming small from hunger
* lc_to_butterfly_prob(0.05) - the probability of large caterpillar becoming a butterly upon eating
* lc_hunger_revert_prob(0.05) - the probability of large caterpillar becomming medium caterpillar when hungry
* leaf_generation_prob(0.01) - the probability of any empty cell to generate a leaf
* butterfly_sc_prob(0.2) - the probability of a butterly leaving behind a small caterpillar
* butterfly_death_prob(0.02) - probability of any caterpillar dying
