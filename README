# NAME
### Simulation Analysis of Large-scale Dynamic Systems

 * Validation of model properties - prototype evaluation
   * `Check_BY.py` - oscillation on a Bayramov model
   * `Check_LV.py` - oscillation on a Lotka-Volterra model
   * `Check_WH.py` - reachability on a Wilhelm model
 * Prefix prefix length distribution - prototype evaluation
   * `EvaluateBY.py` - Bayramov model
   * `EvaluateLV.py` - Lotka-Volterra model
   * `EvaluateWH.py` - Wilhelm model
 * System models - ODE numerics
   * `Bayramov.py`
   * `Lotka_voltera.py`
   * `Wilhelm.py`
 * Cycle detector modules
   * `Brent.py`
   * `Sven.py`
 * Filtering
   * `Filter.py`
 * Generic expression representation
   * `ExpressionStructure.py` - abstract expression tree structure
   * `ExpressionEvaluation.py` - "standard" expression semantics
   * `LTLExpression.py` - abstract LTL expression tree structure
 * Bounded symbolic modelchecking expression representation - LTL semantics
   * `AcyclicSymbolicBoundedLTLEvaluation.py` - acyclic sematics
   * `CyclicSymbolicBoundedLTLEvaluation.py` - cyclic semantics

# DESCRIPTION
The toolset is a prototype implementation of a numerical simulation and model checking tool.
Check and Evaluation modules are the prototype user front-ends.

Check and Evaluation modules run multiple simulations starting in seeds given by a rectangular grid.

In Check modules, resulting traces are validated against custom hard-coded LTL properties.
Results are printed on the standard output as `Evaluated on seed: [x, y]: True/False`.
The results are displayed as plots in a separated graphical window, too.
Square symbols represent seeds, x symbols represent points that passed filtering.

 * red -- no cycle detected; False
 * purple -- cycle detected but evaluation False
 * green -- evaluated True

Evaluation modules provide trace prefix clustering information on larger amount of seeds based on cycle detector accuracy configuration and model type.
Resulting histograms are depicted in graphics mode and in textual output, too.

Properties are represented by means of either cyclic or acyclic LTL semantics expression structures.
Property constraint specifications are represented by standard semantics expression structures.
Check and Evaluation modules work with custom LTL properties hard-coded in this fashion.

 * `ExpressionStructure.py` and `LTLExpression.py` modules provide abstract expression representation.
   These include atoms, operators and expression structures. The LTL expression provides LTL operators and expression structures.
 * The semantics modules extend abstract structures with evaluation implementation.
   LTL semantics is provided by means of _Bounded symbolic model checking_.
 * Numerical simulation modules provide classes representing particular models.
   These use various NumPy and Sci-Py objects as their building blocks.
 * Filter operates by comparing each trace point constraints evaluation with previous point constraints evaluation.
 * Brent cycle detector is adjusted to work with real vectors and custom accuracy in each dimension.
 * Sven cycle detector works by checking trace points agains a list of seleced points in which the trace slope chanes substantially.

Some code is present in each modules `__main__` section as a basic functionality test -- each module can be executed.

# OPTIONS
A property specification parser is not implemented yet.
To adjust property specifications, editing particular Check or Evaluation module `__main__` section is required.

Debugging information amount may be increased changing `WARNING` to `INFO` or `DEBUG` on the `logging.basicConfig(level=logging.WARNING)` line.


# BUGS
Bayramov Validation and Evaluation modules are not working properly.

# NOTES
The toolset requires [Enthought Python Distribution](http://enthought.com/products/epd.php).
