# Size of variable arrays:
# from: http://models.cellml.org/exposure/9d48e39f893b5f1e98e53778f606c2c2/bhalla_iyengar_1999_d.cellml/@@cellml_codegen/Python
sizeAlgebraic = 0
sizeStates = 11
sizeConstants = 30
from math import *
from numpy import *

def createLegends():
    legend_states = [""] * sizeStates
    legend_rates = [""] * sizeStates
    legend_algebraic = [""] * sizeAlgebraic
    legend_voi = ""
    legend_constants = [""] * sizeConstants
    legend_VOI = "t in component environment (s)"
    legend_constants[0] = "kf5 in component RAF (per_um_s)"
    legend_constants[1] = "kb5 in component RAF (per_s)"
    legend_constants[2] = "km1 in component RAF (um)"
    legend_constants[3] = "km2 in component RAF (um)"
    legend_constants[4] = "km3 in component RAF (um)"
    legend_constants[5] = "km4 in component RAF (um)"
    legend_constants[6] = "Vmax1 in component RAF (per_s)"
    legend_constants[7] = "Vmax2 in component RAF (per_s)"
    legend_constants[8] = "Vmax3 in component RAF (per_s)"
    legend_constants[9] = "Vmax4 in component RAF (per_s)"
    legend_constants[10] = "PKC in component undefinedvariables (um)"
    legend_constants[11] = "PP2A in component RAF (um)"
    legend_states[0] = "MAPK_star in component MAPK (um)"
    legend_states[1] = "Raf in component RAF (um)"
    legend_states[2] = "Raf_star in component RAF (um)"
    legend_states[3] = "Raf_star_star in component RAF (um)"
    legend_states[4] = "GTPRas in component RAF (um)"
    legend_states[5] = "GTPRasRaf_star in component RAF (um)"
    legend_constants[12] = "km6 in component MAPKK (um)"
    legend_constants[13] = "km7 in component MAPKK (um)"
    legend_constants[14] = "km8 in component MAPKK (um)"
    legend_constants[15] = "km9 in component MAPKK (um)"
    legend_constants[16] = "Vmax6 in component MAPKK (per_s)"
    legend_constants[17] = "Vmax7 in component MAPKK (per_s)"
    legend_constants[18] = "Vmax8 in component MAPKK (per_s)"
    legend_constants[19] = "Vmax9 in component MAPKK (per_s)"
    legend_constants[20] = "PP2A in component MAPKK (um)"
    legend_states[6] = "MAPKK in component MAPKK (um)"
    legend_states[7] = "MAPKK_star in component MAPKK (um)"
    legend_states[8] = "MAPKK_star_star in component MAPKK (um)"
    legend_constants[21] = "km10 in component MAPK (um)"
    legend_constants[22] = "km11 in component MAPK (um)"
    legend_constants[23] = "km12 in component MAPK (um)"
    legend_constants[24] = "km13 in component MAPK (um)"
    legend_constants[25] = "Vmax10 in component MAPK (per_s)"
    legend_constants[26] = "Vmax11 in component MAPK (per_s)"
    legend_constants[27] = "Vmax12 in component MAPK (per_s)"
    legend_constants[28] = "Vmax13 in component MAPK (per_s)"
    legend_states[9] = "MAPK in component MAPK (um)"
    legend_states[10] = "MAPK_tyr in component MAPK (um)"
    legend_constants[29] = "MKP1 in component MAPK (um)"
    legend_rates[5] = "d/dt GTPRasRaf_star in component RAF (um)"
    legend_rates[4] = "d/dt GTPRas in component RAF (um)"
    legend_rates[1] = "d/dt Raf in component RAF (um)"
    legend_rates[2] = "d/dt Raf_star in component RAF (um)"
    legend_rates[3] = "d/dt Raf_star_star in component RAF (um)"
    legend_rates[6] = "d/dt MAPKK in component MAPKK (um)"
    legend_rates[7] = "d/dt MAPKK_star in component MAPKK (um)"
    legend_rates[8] = "d/dt MAPKK_star_star in component MAPKK (um)"
    legend_rates[9] = "d/dt MAPK in component MAPK (um)"
    legend_rates[10] = "d/dt MAPK_tyr in component MAPK (um)"
    legend_rates[0] = "d/dt MAPK_star in component MAPK (um)"
    return (legend_states, legend_algebraic, legend_voi, legend_constants)

def initConsts():
    constants = [0.0] * sizeConstants; states = [0.0] * sizeStates;
    constants[0] = 0.00004
    constants[1] = 0.5
    constants[2] = 66.666666667
    constants[3] = 25.64166667
    constants[4] = 15.6565
    constants[5] = 15.6565
    constants[6] = 4
    constants[7] = 10
    constants[8] = 6
    constants[9] = 6
    constants[10] = 0.1
    constants[11] = 0.224
    states[0] = 0
    states[1] = 0.1
    states[2] = 0
    states[3] = 0
    states[4] = 0.1
    states[5] = 0
    constants[12] = 0.159091667
    constants[13] = 0.159091667
    constants[14] = 15.6565
    constants[15] = 15.6565
    constants[16] = 0.105
    constants[17] = 0.105
    constants[18] = 6
    constants[19] = 6
    constants[20] = 0.224
    states[6] = 0.18
    states[7] = 0
    states[8] = 0
    constants[21] = 0.046296667
    constants[22] = 0.046296667
    constants[23] = 0.066666667
    constants[24] = 0.066666667
    constants[25] = 0.15
    constants[26] = 0.15
    constants[27] = 1
    constants[28] = 1
    states[9] = 0.36
    states[10] = 0
    constants[29] = 0.032
    return (states, constants)

def computeRates(voi, states, constants):
    rates = [0.0] * sizeStates; algebraic = [0.0] * sizeAlgebraic
    rates[5] = states[4]*states[2]*(constants[0]*1.00000)-states[5]*constants[1]
    rates[4] = -states[4]*states[2]*(constants[0]*1.00000)+states[5]*constants[1]
    rates[1] = (-constants[10]*states[1]*constants[6])/(constants[2]+states[1])+(states[2]*constants[11]*constants[8])/(constants[4]+states[2])
    rates[2] = (((constants[10]*states[1]*constants[6])/(constants[2]+states[1])-(states[2]*constants[11]*constants[8])/(constants[4]+states[2]))-(states[2]*states[0]*constants[7])/(constants[3]+states[2]))+(states[3]*constants[11]*constants[9])/(constants[5]+states[3])
    rates[3] = (states[2]*states[0]*constants[7])/(constants[3]+states[2])-(states[3]*constants[11]*constants[9])/(constants[5]+states[3])
    rates[6] = (-states[6]*constants[16]*states[5])/(constants[12]+states[6])+(states[7]*constants[18]*constants[20])/(constants[14]+states[7])
    rates[7] = (((states[6]*constants[16]*states[5])/(constants[12]+states[6])-(states[7]*constants[18]*constants[20])/(constants[14]+states[7]))-(states[7]*constants[17]*states[5])/(constants[13]+states[7]))+(states[8]*constants[19]*constants[20])/(constants[15]+states[8])
    rates[8] = (states[7]*constants[17]*states[5])/(constants[13]+states[7])-(states[8]*constants[19]*constants[20])/(constants[15]+states[8])
    rates[9] = (-states[9]*constants[25]*states[8])/(constants[21]+states[9])+(states[10]*constants[27]*constants[29])/(constants[23]+states[10])
    rates[10] = (((states[9]*constants[25]*states[8])/(constants[21]+states[9])-(states[10]*constants[27]*constants[29])/(constants[23]+states[10]))-(states[10]*constants[26]*states[8])/(constants[22]+states[10]))+(states[0]*constants[28]*constants[29])/(constants[24]+states[0])
    rates[0] = (states[10]*constants[26]*states[8])/(constants[22]+states[10])-(states[0]*constants[28]*constants[29])/(constants[24]+states[0])
    return(rates)

def computeAlgebraic(constants, states, voi):
    algebraic = array([[0.0] * len(voi)] * sizeAlgebraic)
    states = array(states)
    voi = array(voi)
    return algebraic

def solve_model():
    """Solve model with ODE solver"""
    from scipy.integrate import ode
    # Initialise constants and state variables
    (init_states, constants) = initConsts()

    # Set timespan to solve over
    voi = linspace(0, 10, 500)

    # Construct ODE object to solve
    r = ode(computeRates)
    r.set_integrator('vode', method='bdf', atol=1e-06, rtol=1e-06, max_step=1)
    r.set_initial_value(init_states, voi[0])
    r.set_f_params(constants)

    # Solve model
    states = array([[0.0] * len(voi)] * sizeStates)
    states[:,0] = init_states
    for (i,t) in enumerate(voi[1:]):
        if r.successful():
            r.integrate(t)
            states[:,i+1] = r.y
        else:
            break

    # Compute algebraic variables
    algebraic = computeAlgebraic(constants, states, voi)
    return (voi, states, algebraic)

def plot_model(voi, states, algebraic):
    """Plot variables against variable of integration"""
    import pylab
    (legend_states, legend_algebraic, legend_voi, legend_constants) = createLegends()
    pylab.figure(1)
    pylab.plot(voi,vstack((states,algebraic)).T)
    pylab.xlabel(legend_voi)
    pylab.legend(legend_states + legend_algebraic, loc='best')
    pylab.show()

if __name__ == "__main__":
    (voi, states, algebraic) = solve_model()
    plot_model(voi, states, algebraic)
