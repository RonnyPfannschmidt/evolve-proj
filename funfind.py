import argparse

from pyevolve import Util, GTree, GSimpleGA, Consts
import math
import sys

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


def visit_node(node, terminals, functions):
    if not node.childs:
        return terminals[node.node_data]
    else:
        args = [visit_node(c, terminals, functions)
                for c in node.childs]
        func = functions[node.node_data]
        return func(*args)

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


class PushEval(object):
    def __init__(self, root, functions):
        self.ops = []
        self._nodeops(root, functions)

    def _nodeops(self, node, functions):
        if not node.childs:
            def pushterminal(stack, terminals, name=node.node_data):
                stack.append(terminals[name])
            self.ops.append(pushterminal)
        else:
            for child in node.childs:
                self._nodeops(child, functions)

            func = functions[node.node_data]
            argc = func.__code__.co_argcount
            if argc==1:
                def call1(stack, terminals, func=func):
                    stack.append(func(stack.pop()))
                self.ops.append(call1)
            else:
                def call2(stack, terminals, func=func):
                    stack.append(func(stack.pop(), stack.pop()))
                self.ops.append(call2)

    def __call__(self, terminals):
        stack = []
        for op in self.ops:
            op(stack, terminals)
        return stack[0]


def eval_stack(chromosome):
    error_accum = Util.ErrorAccumulator()
    root = chromosome.getRoot()
    eval = PushEval(root, functions)
    for a in xrange(0, 5):
        for b in xrange(0, 5):
            a = float(a)
            b = float(b)
            # The eval will execute a pre-compiled syntax tree
            # as a Python expression, and will automatically use
            # the "a" and "b" variables (the terminals defined)
            evaluated     = eval({'a':a, 'b':b})
            target        = math.sqrt((a*a)+(b*b))
            error_accum.append(target, evaluated)
    return error_accum.getRMSE()







def main_run(eval_func):
    genome = GTree.GTreeGP()
    genome.setParams(max_depth=5, method="ramped")
    genome.evaluator.set(eval_func)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setParams(gp_terminals=['a', 'b'],
                 gp_function_set={
                     'add': 2,
                     'sub': 2,
                     'mul': 2,
                     'sqrt': 1,
                 })
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setGenerations(500)
    ga.setMutationRate(0.08)
    ga.setCrossoverRate(1.0)
    ga.setPopulationSize(1500)
    ga.evolve(freq_stats=20)

    print ga.bestIndividual().getPreOrderExpression()


if __name__ == "__main__":
    command = sys.argv[1]
    eval_func = globals()['eval_' + command]

    main_run(eval_func)
