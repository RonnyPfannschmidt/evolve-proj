import argparse

from pyevolve import Util, GTree, GSimpleGA, Consts
import math
import sys

class FlushFile(object):
    """Write-only flushing wrapper for file-type objects."""
    def __init__(self, f):
        self.f = f
    def write(self, x):
        self.f.write(x)
        self.f.flush()

# Replace stdout with an automatically flushing version
sys.stdout = FlushFile(sys.__stdout__)


def gp_add(a, b): return a+b
def gp_sub(a, b): return a-b
def gp_mul(a, b): return a*b
def gp_sqrt(a):   return math.sqrt(abs(a))

functions = {
    'add': gp_add,
    'sub': gp_sub,
    'mul': gp_mul,
    'sqrt': gp_sqrt,
}


stack_functions = {
    'add': lambda stack, terminals:stack.append(stack.pop()+stack.pop()),
    'sub': lambda stack, terminals:stack.append(stack.pop()-stack.pop()),
    'mul': lambda stack, terminals:stack.append(stack.pop()*stack.pop()),
    'sqrt': lambda stack, terminals:stack.append(math.sqrt(abs(stack.pop()))),
}

stack_terminas = {
    'a': lambda stack, terminals: stack.append(terminals['a']),
    'b': lambda stack, terminals: stack.append(terminals['b']),
}


def visit_node(node, terminals, functions):
    if not node.childs:
        return terminals[node.node_data]
    else:
        func = functions[node.node_data]
        if len(node.childs) == 1:
            return func(visit_node(node.childs[0], terminals, functions))
        else:
            return func(visit_node(node.childs[0], terminals, functions),
                        visit_node(node.childs[1], terminals, functions))


def eval_visit(chromosome):
    error_accum = Util.ErrorAccumulator()
    root = chromosome.getRoot()
    for a in xrange(0, 5):
        for b in xrange(0, 5):
            a = float(a)
            b = float(b)
            evaluated     = visit_node(root, {'a':a, 'b':b}, functions)
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


def nodeops(node, functions):
    res = []
    _nodeops(res, node, functions)
    return res


def _nodeops(ops, node, functions):
    if not node.childs:
        ops.append(stack_terminas[node.node_data])
    else:
        for child in node.childs:
            _nodeops(ops, child, functions)
        ops.append(stack_functions[node.node_data])


def eval_ops(ops, terminals):
    stack = []
    for op in ops:
        op(stack, terminals)
    return stack[0]


def eval_stack(chromosome):
    error_accum = Util.ErrorAccumulator()
    root = chromosome.getRoot()
    ops = nodeops(root, functions)
    for a in xrange(0, 5):
        for b in xrange(0, 5):
            a = float(a)
            b = float(b)
            # The eval will execute a pre-compiled syntax tree
            # as a Python expression, and will automatically use
            # the "a" and "b" variables (the terminals defined)
            evaluated     = eval_ops(ops, {'a':a, 'b':b})
            target        = math.sqrt((a*a)+(b*b))
            error_accum.append(target, evaluated)
    return error_accum.getRMSE()




def eval_height(chromosome):
    return abs(chromosome.tree_height-3)


def main_run(eval_func, options):
    genome = GTree.GTreeGP()
    genome.setParams(max_depth=5, method="ramped")
    genome.evaluator.set(eval_func, 5)
    genome.evaluator.add(eval_height, options.height_weight)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setParams(gp_terminals=['a', 'b'],
                 gp_function_set={
                     'add': 2,
                     'sub': 2,
                     'mul': 2,
                     'sqrt': 1,
                 })
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setGenerations(options.generations)
    ga.setMutationRate(0.08)
    ga.setCrossoverRate(1.0)
    ga.setPopulationSize(options.population)
    ga.evolve(freq_stats=20)

    print ga.bestIndividual().getPreOrderExpression()


def main():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('command')
    parser.add_argument('--generations', type=int, default=500)
    parser.add_argument('--population', type=int, default=1500)
    parser.add_argument('--height-weight', type=float, default=0)

    options = parser.parse_args()
    eval_func = globals()['eval_' + options.command]
    main_run(eval_func, options)


if __name__ == "__main__":
    main()
