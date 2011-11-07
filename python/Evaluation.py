#!/usr/bin/env python
# the common main for all the Evaluators
import Plugins as pl
import EvaluationBY as eby
import numpy as np
import Brent as bt
import Sven as sv
import Histogram as hs
import matplotlib as mp
import multiprocessing as mps
import Lotka_Volterra as lv
import Bayramov as by
import logging, sys, argparse

logger = logging.getLogger('Evaluation')

class Args(object):
    _cycle = None
    _system = None
    _evaluation = None
    _amount = None
    epsilon = 0.
    atomic_propositions = ''
    processes = 0
    # the arguments handling type
    @property
    def cycle(self):
        return self._cycle
    @cycle.setter
    def cycle(self, other):
        if other == 'S':
            self._cycle = sv.CycleDetect
        else:
            self._cycle = bt.CycleDetect
    @property
    def system(self):
        return self._system
    @system.setter
    def system(self, other):
        if other == 'L':
            self._system = lv.LotkaVolterra2D
            self._evaluation = pl.Evaluation2D
        else:
            self._system = by.Bayramov
            self._evaluation = pl.Evaluation3D
    @property
    def amount(self):
        return self._amount
    @amount.setter
    def amount(self, other):
        if other == 'T':
            self._amount = pl.Thousand
        else:
            self._amount = pl.Hundred

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    argsparser = argparse.ArgumentParser(description = 'Evaluate Some Simulations')
    argsparser.add_argument('-c', '--cycle', choices = 'SB', required = True, help = "Use Sven|Brent cycle detector")
    argsparser.add_argument('-e', '--epsilon', type = float, required = True, help = "The accuracy of the cycle detector used") 
    argsparser.add_argument('-s', '--system', choices = 'LB', required = True, help = "Use Bayramov|Lotka-Volterra ODE system")
    argsparser.add_argument('-a', '--amount', choices = 'TH', required = True, help = "The Thousand|Hundred amount of initial conditions to use")
    atomicgroup = argsparser.add_mutually_exclusive_group(required = True)
    atomicgroup.add_argument('--one', help = "Use one Atomic propositions", dest = 'atomic_propositions', action = 'store_const', const = 'one_ap_filter')
    atomicgroup.add_argument('--four', help = "Use four Atomic propositions", dest = 'atomic_propositions', action = 'store_const', const = 'four_ap_filter')
    atomicgroup.add_argument('--sixteen', help = "Use sixteen Atomic propositions", dest = 'atomic_propositions', action = 'store_const', const = 'sixteen_ap_filter')
    argsparser.add_argument('-p', '--processes', type = int, required = False, default = 2, help = "The number of processes to use for paralellization")
    myargs = Args()
    argsparser.parse_args(namespace=myargs)
    
    logger.debug("args: %s" % vars(myargs))
    for x in pl.Evaluation3D.plugins:
        logger.info("Evaluation3D plugin: %s" % x)
        