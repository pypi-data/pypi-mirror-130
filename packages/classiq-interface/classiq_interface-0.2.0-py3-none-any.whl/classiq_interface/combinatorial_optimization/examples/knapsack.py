from typing import List

import numpy as np
import pyomo.core as pyo


def knapsack(values: List[int], upper_bounds: List[int]) -> pyo.ConcreteModel:
    model = pyo.ConcreteModel()

    def bounds(model, i):
        return 0, upper_bounds[i]

    model.x = pyo.Var(range(len(values)), domain=pyo.NonNegativeIntegers, bounds=bounds)
    model.cost = pyo.Objective(
        expr=values @ np.array(model.x.values()), sense=pyo.maximize
    )

    return model
