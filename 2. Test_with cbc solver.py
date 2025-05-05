from pyomo.environ import SolverFactory

print(SolverFactory('cbc').available())