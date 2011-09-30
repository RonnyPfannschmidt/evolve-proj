import argparse

from pyevolve import Util, GTree, GSimpleGA, Consts
import math
import sys

# This is the functions used by the GP core,
# Pyevolve will automatically detect them
# and the number of arguments
def gp_add(a, b): return a+b
def gp_sub(a, b): return a-b
def gp_mul(a, b): return a*b
def gp_sqrt(a):   return math.sqrt(abs(a))

functions = {
    'gp_add': gp_add,
    'gp_sub': gp_sub,
    'gp_mul': gp_mul,
    'gp_sqrt': gp_sqrt,
}


def eval_node(node, terminals, functions):
    if not node.childs:
        return terminals[node.node_data]
    else:
        args = [eval_node(c, terminals, functions)
                for c in node.childs]
        func = functions[node.node_data]
        return func(*args)

def eval_nodes(chromosome):
    error_accum = Util.ErrorAccumulator()
    root = chromosome.getRoot()
    for a in xrange(0, 5):
        for b in xrange(0, 5):
            a = float(a)
            b = float(b)
            evaluated     = eval_node(root, {'a':a, 'b':b}, functions)
            target        = math.sqrt((a*a)+(b*b))
            error_accum.append(target, evaluated)
    return error_accum.getRMSE()

def eval_code(chromosome):
    error_accum = Util.ErrorAccumulator()
    code_comp = chromosome.getCompiledCode()
    root = chromosome.getRoot()
    for a in xrange(0, 5):
        for b in xrange(0, 5):
            a = float(a)
            b = float(b)
            # The eval will execute a pre-compiled syntax tree
            # as a Python expression, and will automatically use
            # the "a" and "b" variables (the terminals defined)
            evaluated     = eval(code_comp, {'a':a, 'b':b}, functions)
            target        = math.sqrt((a*a)+(b*b))
            error_accum.append(target, evaluated)
    return error_accum.getRMSE()


def main_run(eval_func):
    genome = GTree.GTreeGP()
    genome.setParams(max_depth=5, method="ramped")
    genome.evaluator.set(eval_func)

    ga = GSimpleGA.GSimpleGA(genome)
    # This method will catch and use every function that
    # begins with "gp", but you can also add them manually.
    # The terminals are Python variables, you can use the
    # ephemeral random consts too, using ephemeral:random.randint(0,2)
    # for example.
    ga.setParams(gp_terminals       = ['a', 'b'],
                 gp_function_prefix = "gp")
    # You can even use a function call as terminal, like "func()"
    # and Pyevolve will use the result of the call as terminal
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setGenerations(500)
    ga.setMutationRate(0.08)
    ga.setCrossoverRate(1.0)
    ga.setPopulationSize(1500)
    ga.evolve(freq_stats=20)

    #print ga.bestIndividual()

if __name__ == "__main__":

    if 'code' in sys.argv:
        eval_func = eval_code
    else:
        eval_func = eval_nodes

    main_run(eval_func)
