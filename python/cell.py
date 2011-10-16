# Size of variable arrays:
sizeAlgebraic = 53
sizeStates = 22
sizeConstants = 83
from math import *
from numpy import *

def createLegends():
    legend_states = [""] * sizeStates
    legend_rates = [""] * sizeStates
    legend_algebraic = [""] * sizeAlgebraic
    legend_voi = ""
    legend_constants = [""] * sizeConstants
    legend_VOI = "time in component environment (hour)"
    legend_constants[0] = "eps in component E (dimensionless)"
    legend_constants[1] = "K1 in component A (per_hour)"
    legend_constants[2] = "K1a in component A (per_hour)"
    legend_constants[3] = "K2 in component A (per_hour)"
    legend_constants[4] = "K2a in component A (per_hour)"
    legend_constants[5] = "K2aa in component A (per_hour)"
    legend_constants[6] = "K3 in component A (per_hour)"
    legend_constants[7] = "K3a in component A (per_hour)"
    legend_constants[8] = "K4 in component A (per_hour)"
    legend_constants[9] = "J1 in component A (dimensionless)"
    legend_constants[10] = "J3 in component A (dimensionless)"
    legend_constants[11] = "J4 in component A (dimensionless)"
    legend_algebraic[1] = "v_20 in component A (per_hour)"
    legend_algebraic[21] = "v_21 in component A (per_hour)"
    legend_algebraic[0] = "v_42 in component A (per_hour)"
    legend_algebraic[22] = "v_19 in component A (per_hour)"
    legend_constants[12] = "GA in component A (dimensionless)"
    legend_constants[13] = "GB in component A (dimensionless)"
    legend_constants[14] = "GE in component A (dimensionless)"
    legend_algebraic[12] = "V_2 in component A (per_hour)"
    legend_algebraic[13] = "V_4 in component A (per_hour)"
    legend_states[0] = "Cdh1 in component A (dimensionless)"
    legend_constants[15] = "Cdc20 in component D (dimensionless)"
    legend_states[1] = "CYCA in component D (dimensionless)"
    legend_states[2] = "CYCB in component A (dimensionless)"
    legend_states[3] = "CYCE in component D (dimensionless)"
    legend_constants[16] = "k15 in component B (per_hour)"
    legend_constants[17] = "k16 in component B (per_hour)"
    legend_constants[18] = "k17 in component B (per_hour)"
    legend_constants[19] = "k17a in component B (per_hour)"
    legend_constants[20] = "k18 in component B (per_hour)"
    legend_constants[21] = "K9 in component B (per_hour)"
    legend_constants[22] = "J17 in component B (dimensionless)"
    legend_constants[23] = "J15 in component B (dimensionless)"
    legend_algebraic[14] = "v_1 in component B (per_hour)"
    legend_algebraic[15] = "v_2 in component B (per_hour)"
    legend_algebraic[2] = "v_34 in component B (per_hour)"
    legend_algebraic[5] = "v_39 in component B (per_hour)"
    legend_algebraic[3] = "v_41 in component B (per_hour)"
    legend_states[4] = "DRG in component B (dimensionless)"
    legend_states[5] = "ERG in component B (dimensionless)"
    legend_constants[24] = "K19 in component C (per_hour)"
    legend_constants[25] = "K19a in component C (per_hour)"
    legend_constants[26] = "K20 in component C (per_hour)"
    legend_constants[27] = "K21 in component C (dimensionless)"
    legend_constants[28] = "K22 in component C (per_hour)"
    legend_constants[29] = "K23a in component C (per_hour)"
    legend_constants[30] = "K23 in component C (per_hour)"
    legend_constants[31] = "K26 in component C (per_hour)"
    legend_constants[32] = "K26R in component C (per_hour)"
    legend_algebraic[16] = "v_29 in component C (per_hour)"
    legend_algebraic[23] = "v_30 in component C (per_hour)"
    legend_algebraic[25] = "v_43 in component C (per_hour)"
    legend_algebraic[27] = "v_44 in component C (per_hour)"
    legend_algebraic[29] = "v_45 in component C (per_hour)"
    legend_algebraic[31] = "v_46 in component C (per_hour)"
    legend_algebraic[33] = "v_47 in component C (per_hour)"
    legend_algebraic[35] = "v_48 in component C (per_hour)"
    legend_algebraic[37] = "v_49 in component C (per_hour)"
    legend_algebraic[40] = "v_50 in component C (per_hour)"
    legend_algebraic[42] = "v_51 in component C (per_hour)"
    legend_algebraic[44] = "v_52 in component C (per_hour)"
    legend_constants[33] = "LA in component C (dimensionless)"
    legend_constants[34] = "LB in component C (dimensionless)"
    legend_constants[35] = "LD in component C (dimensionless)"
    legend_constants[36] = "LE in component C (dimensionless)"
    legend_constants[37] = "FE in component C (dimensionless)"
    legend_constants[38] = "FB in component C (dimensionless)"
    legend_states[6] = "Rb in component C (dimensionless)"
    legend_states[7] = "PPRb in component C (dimensionless)"
    legend_states[8] = "E2F in component C (dimensionless)"
    legend_states[9] = "PE2F in component C (dimensionless)"
    legend_states[10] = "E2FRb in component C (dimensionless)"
    legend_states[11] = "PE2FRb in component C (dimensionless)"
    legend_algebraic[4] = "PP1A in component C (dimensionless)"
    legend_constants[39] = "PP1T in component C (dimensionless)"
    legend_constants[40] = "CYCDT in component C (dimensionless)"
    legend_constants[41] = "K5 in component D (per_hour)"
    legend_constants[42] = "K6a in component D (per_hour)"
    legend_constants[43] = "K6 in component D (per_hour)"
    legend_constants[44] = "K7a in component D (per_hour)"
    legend_constants[45] = "K7 in component D (per_hour)"
    legend_constants[46] = "K8a in component D (per_hour)"
    legend_constants[47] = "K8 in component D (per_hour)"
    legend_constants[48] = "K10 in component D (per_hour)"
    legend_constants[49] = "k24 in component D (per_hour)"
    legend_constants[50] = "k24r in component D (per_hour)"
    legend_constants[51] = "K25 in component D (per_hour)"
    legend_constants[52] = "K25R in component D (per_hour)"
    legend_constants[53] = "K29 in component D (per_hour)"
    legend_constants[54] = "K30 in component D (per_hour)"
    legend_constants[55] = "J8 in component D (dimensionless)"
    legend_algebraic[26] = "v_3 in component D (per_hour)"
    legend_algebraic[28] = "v_4 in component D (per_hour)"
    legend_algebraic[30] = "v_5 in component D (per_hour)"
    legend_algebraic[32] = "v_6 in component D (per_hour)"
    legend_algebraic[34] = "v_7 in component D (per_hour)"
    legend_algebraic[36] = "v_8 in component D (per_hour)"
    legend_algebraic[38] = "v_9 in component D (per_hour)"
    legend_algebraic[41] = "v_10 in component D (per_hour)"
    legend_algebraic[43] = "v_11 in component D (per_hour)"
    legend_algebraic[45] = "v_12 in component D (per_hour)"
    legend_algebraic[46] = "v_13 in component D (per_hour)"
    legend_algebraic[49] = "v_14 in component D (per_hour)"
    legend_algebraic[48] = "v_15 in component D (per_hour)"
    legend_algebraic[51] = "v_16 in component D (per_hour)"
    legend_algebraic[39] = "v_17 in component D (per_hour)"
    legend_algebraic[47] = "v_18 in component D (per_hour)"
    legend_algebraic[50] = "v_36 in component D (per_hour)"
    legend_algebraic[52] = "v_38 in component D (per_hour)"
    legend_constants[79] = "v_40 in component D (per_hour)"
    legend_constants[56] = "HA in component D (dimensionless)"
    legend_constants[57] = "HB in component D (dimensionless)"
    legend_constants[58] = "HE in component D (dimensionless)"
    legend_constants[59] = "YE in component D (dimensionless)"
    legend_constants[60] = "YB in component D (dimensionless)"
    legend_states[12] = "p27 in component D (dimensionless)"
    legend_algebraic[17] = "V_6 in component D (per_hour)"
    legend_algebraic[24] = "V_8 in component D (per_hour)"
    legend_states[13] = "MASS in component E (dimensionless)"
    legend_states[14] = "CA in component D (dimensionless)"
    legend_states[15] = "CD in component D (dimensionless)"
    legend_states[16] = "CE in component D (dimensionless)"
    legend_states[17] = "CYCD in component D (dimensionless)"
    legend_constants[61] = "CYCET in component D (dimensionless)"
    legend_constants[62] = "K27 in component E (per_hour)"
    legend_constants[63] = "K28 in component E (per_hour)"
    legend_algebraic[6] = "v_31 in component E (per_hour)"
    legend_algebraic[18] = "v_32 in component E (per_hour)"
    legend_algebraic[7] = "v_33 in component E (per_hour)"
    legend_constants[64] = "r31switch in component E (dimensionless)"
    legend_constants[65] = "MU in component E (per_hour)"
    legend_states[18] = "GM in component E (dimensionless)"
    legend_constants[66] = "K11a in component F (per_hour)"
    legend_constants[67] = "K11 in component F (per_hour)"
    legend_constants[68] = "K12 in component F (per_hour)"
    legend_constants[69] = "K13 in component F (per_hour)"
    legend_constants[70] = "K14 in component F (per_hour)"
    legend_constants[71] = "K31 in component F (per_hour)"
    legend_constants[72] = "K32 in component F (per_hour)"
    legend_constants[73] = "K33 in component F (per_hour)"
    legend_constants[74] = "K34 in component F (per_hour)"
    legend_constants[75] = "J13 in component F (dimensionless)"
    legend_constants[76] = "J14 in component F (dimensionless)"
    legend_constants[77] = "J31 in component F (dimensionless)"
    legend_constants[78] = "J32 in component F (dimensionless)"
    legend_algebraic[8] = "v_22 in component F (per_hour)"
    legend_algebraic[9] = "v_23 in component F (per_hour)"
    legend_algebraic[19] = "v_24 in component F (per_hour)"
    legend_algebraic[11] = "v_25 in component F (per_hour)"
    legend_algebraic[10] = "v_26 in component F (per_hour)"
    legend_constants[80] = "v_27 in component F (per_hour)"
    legend_constants[81] = "v_28 in component F (per_hour)"
    legend_algebraic[20] = "v_35 in component F (per_hour)"
    legend_constants[82] = "v_37 in component F (per_hour)"
    legend_states[19] = "IEP in component F (dimensionless)"
    legend_states[20] = "PPX in component F (dimensionless)"
    legend_states[21] = "Cdc20T in component F (dimensionless)"
    legend_rates[0] = "d/dt Cdh1 in component A (dimensionless)"
    legend_rates[2] = "d/dt CYCB in component A (dimensionless)"
    legend_rates[4] = "d/dt DRG in component B (dimensionless)"
    legend_rates[5] = "d/dt ERG in component B (dimensionless)"
    legend_rates[7] = "d/dt PPRb in component C (dimensionless)"
    legend_rates[8] = "d/dt E2F in component C (dimensionless)"
    legend_rates[9] = "d/dt PE2F in component C (dimensionless)"
    legend_rates[6] = "d/dt Rb in component C (dimensionless)"
    legend_rates[10] = "d/dt E2FRb in component C (dimensionless)"
    legend_rates[11] = "d/dt PE2FRb in component C (dimensionless)"
    legend_rates[14] = "d/dt CA in component D (dimensionless)"
    legend_rates[15] = "d/dt CD in component D (dimensionless)"
    legend_rates[16] = "d/dt CE in component D (dimensionless)"
    legend_rates[1] = "d/dt CYCA in component D (dimensionless)"
    legend_rates[17] = "d/dt CYCD in component D (dimensionless)"
    legend_rates[3] = "d/dt CYCE in component D (dimensionless)"
    legend_rates[12] = "d/dt p27 in component D (dimensionless)"
    legend_rates[18] = "d/dt GM in component E (dimensionless)"
    legend_rates[13] = "d/dt MASS in component E (dimensionless)"
    legend_rates[21] = "d/dt Cdc20T in component F (dimensionless)"
    legend_rates[19] = "d/dt IEP in component F (dimensionless)"
    legend_rates[20] = "d/dt PPX in component F (dimensionless)"
    return (legend_states, legend_algebraic, legend_voi, legend_constants)

def initConsts():
    constants = [0.0] * sizeConstants; states = [0.0] * sizeStates;
    constants[0] = 1
    constants[1] = 0.6
    constants[2] = 0.1
    constants[3] = 20
    constants[4] = 0.05
    constants[5] = 1
    constants[6] = 140
    constants[7] = 7.5
    constants[8] = 40
    constants[9] = 0.1
    constants[10] = 0.01
    constants[11] = 0.04
    constants[12] = 0.3
    constants[13] = 1
    constants[14] = 0
    states[0] = 0.000653278
    constants[15] = 0.00220177
    states[1] = 1.4094
    states[2] = 2.72898
    states[3] = 0.0229112
    constants[16] = 0.25
    constants[17] = 0.25
    constants[18] = 10
    constants[19] = 0.35
    constants[20] = 10
    constants[21] = 2.5
    constants[22] = 0.3
    constants[23] = 0.1
    states[4] = 0.900533
    states[5] = 0.0121809
    constants[24] = 20
    constants[25] = 0
    constants[26] = 10
    constants[27] = 1
    constants[28] = 1
    constants[29] = 0.005
    constants[30] = 1
    constants[31] = 10000
    constants[32] = 200
    constants[33] = 3
    constants[34] = 5
    constants[35] = 3.3
    constants[36] = 5
    constants[37] = 25
    constants[38] = 2
    states[6] = 0.000190871
    states[7] = 9.97574
    states[8] = 0.989986
    states[9] = 3.98594
    states[10] = 0.00478911
    states[11] = 0.0192822
    constants[39] = 1
    constants[40] = 0.010976
    constants[41] = 20
    constants[42] = 10
    constants[43] = 100
    constants[44] = 0
    constants[45] = 0.6
    constants[46] = 0.1
    constants[47] = 2
    constants[48] = 5
    constants[49] = 1000
    constants[50] = 10
    constants[51] = 1000
    constants[52] = 10
    constants[53] = 0.05
    constants[54] = 20
    constants[55] = 0.1
    constants[56] = 0.5
    constants[57] = 1
    constants[58] = 0.5
    constants[59] = 1
    constants[60] = 0.05
    states[12] = 0.00922806
    states[13] = 1.68776
    states[14] = 0.0356927
    states[15] = 0.010976
    states[16] = 0.000542587
    states[17] = 0.43929
    constants[61] = 0.000542587
    constants[62] = 0.2
    constants[63] = 0.2
    constants[64] = 1
    constants[65] = 0.061
    states[18] = 1.35565
    constants[66] = 0
    constants[67] = 1.5
    constants[68] = 1.5
    constants[69] = 5
    constants[70] = 2.5
    constants[71] = 0.7
    constants[72] = 1.8
    constants[73] = 0.05
    constants[74] = 0.05
    constants[75] = 0.005
    constants[76] = 0.005
    constants[77] = 0.01
    constants[78] = 0.01
    states[19] = 0.154655
    states[20] = 1
    states[21] = 2.36733
    constants[79] = constants[0]*constants[41]
    constants[80] = (constants[70]*constants[15])/(constants[76]+constants[15])
    constants[81] = constants[68]*constants[15]
    constants[82] = constants[0]*constants[73]
    return (states, constants)

def computeRates(voi, states, constants):
    rates = [0.0] * sizeStates; algebraic = [0.0] * sizeAlgebraic
    algebraic[7] = constants[0]*constants[65]*states[18]
    rates[13] = algebraic[7]
    algebraic[8] = constants[74]*states[20]
    rates[20] = constants[82]-algebraic[8]
    algebraic[15] = constants[20]*states[4]
    algebraic[3] = constants[0]*((constants[18]*((states[4]/constants[22])**2.00000))/(((states[4]/constants[22])**2.00000)+1.00000)+constants[19]*states[5])
    rates[4] = algebraic[3]-algebraic[15]
    algebraic[14] = constants[17]*states[5]
    algebraic[2] = (constants[0]*constants[16])/(((states[4]/constants[23])**2.00000)+1.00000)
    rates[5] = algebraic[2]-algebraic[14]
    algebraic[6] = constants[62]*states[13]*constants[64]
    algebraic[18] = constants[63]*states[18]
    rates[18] = algebraic[6]-algebraic[18]
    algebraic[11] = constants[68]*states[21]
    algebraic[20] = constants[0]*constants[66]+constants[67]*states[2]
    rates[21] = algebraic[20]-algebraic[11]
    algebraic[9] = (constants[71]*states[2]*(1.00000-states[19]))/((constants[77]-states[19])+1.00000)
    algebraic[19] = (constants[72]*states[20]*states[19])/(constants[78]+states[19])
    rates[19] = algebraic[9]-algebraic[19]
    algebraic[1] = ((constants[7]+constants[6]*constants[15])*(1.00000-states[0]))/((constants[10]-states[0])+1.00000)
    algebraic[13] = constants[8]*(constants[12]*states[1]+constants[13]*states[2]+constants[14]*states[3])
    algebraic[21] = (algebraic[13]*states[0])/(constants[11]+states[0])
    rates[0] = algebraic[1]-algebraic[21]
    algebraic[0] = constants[0]*((constants[1]*((states[2]/constants[9])**2.00000))/(((states[2]/constants[9])**2.00000)+1.00000)+constants[2])
    algebraic[12] = constants[5]*constants[15]+constants[4]*(1.00000-states[0])+constants[3]*states[0]
    algebraic[22] = algebraic[12]*states[2]
    rates[2] = algebraic[0]-algebraic[22]
    algebraic[16] = states[10]*constants[26]*(constants[40]*constants[35]+constants[33]*states[1]+constants[34]*states[2]+constants[36]*states[3])
    algebraic[23] = states[11]*constants[26]*(constants[40]*constants[35]+constants[33]*states[1]+constants[34]*states[2]+constants[36]*states[3])
    algebraic[25] = states[6]*constants[26]*(constants[40]*constants[35]+constants[33]*states[1]+constants[34]*states[2]+constants[36]*states[3])
    algebraic[4] = constants[39]/(constants[27]*constants[37]*(states[1]+states[3]+constants[38]*states[2])+1.00000)
    algebraic[27] = states[7]*(constants[25]*(constants[39]-algebraic[4])+constants[24]*algebraic[4])
    rates[7] = (algebraic[16]+algebraic[23]+algebraic[25])-algebraic[27]
    algebraic[29] = states[10]*constants[32]
    algebraic[31] = states[8]*(constants[29]+constants[30]*(states[1]+states[2]))
    algebraic[33] = states[9]*constants[28]
    algebraic[35] = states[8]*states[6]*constants[31]
    rates[8] = ((algebraic[16]+algebraic[29]+algebraic[33])-algebraic[31])-algebraic[35]
    algebraic[26] = constants[48]*states[15]
    algebraic[34] = constants[49]*states[12]*states[17]
    algebraic[36] = constants[50]*states[15]
    algebraic[17] = constants[42]+constants[43]*(constants[56]*states[1]+constants[57]*states[2]+constants[58]*states[3])
    algebraic[39] = algebraic[17]*states[15]
    rates[15] = ((algebraic[34]-algebraic[36])-algebraic[39])-algebraic[26]
    algebraic[5] = constants[0]*constants[21]*states[4]
    algebraic[28] = constants[48]*states[17]
    rates[17] = ((algebraic[5]+algebraic[39]+algebraic[36])-algebraic[34])-algebraic[28]
    algebraic[37] = states[11]*constants[32]
    algebraic[40] = states[6]*states[9]*constants[31]
    rates[9] = ((algebraic[23]+algebraic[37]+algebraic[31])-algebraic[33])-algebraic[40]
    rates[6] = (((algebraic[27]+algebraic[29]+algebraic[37])-algebraic[35])-algebraic[40])-algebraic[25]
    algebraic[42] = states[11]*constants[28]
    algebraic[44] = states[10]*(constants[29]+constants[30]*(states[1]+states[2]))
    rates[10] = (((algebraic[42]+algebraic[35])-algebraic[44])-algebraic[16])-algebraic[29]
    rates[11] = (((algebraic[44]+algebraic[40])-algebraic[42])-algebraic[23])-algebraic[37]
    algebraic[32] = constants[51]*states[12]*states[1]
    algebraic[41] = constants[54]*constants[15]*states[14]
    algebraic[45] = constants[52]*states[14]
    algebraic[47] = algebraic[17]*states[14]
    rates[14] = ((algebraic[32]-algebraic[45])-algebraic[47])-algebraic[41]
    algebraic[38] = constants[54]*constants[15]*states[1]
    algebraic[50] = constants[0]*constants[53]*states[8]*states[13]
    rates[1] = ((algebraic[50]-algebraic[38])-algebraic[32])+algebraic[45]+algebraic[47]
    algebraic[30] = constants[51]*states[12]*states[3]
    algebraic[43] = constants[52]*states[16]
    algebraic[24] = (constants[47]*(constants[59]*(states[1]+states[3])+constants[60]*states[2]))/(constants[61]+constants[55])+constants[46]
    algebraic[46] = algebraic[24]*states[16]
    algebraic[48] = algebraic[17]*states[12]
    rates[12] = (((((constants[79]+algebraic[26]+algebraic[36])-algebraic[48])-algebraic[30])-algebraic[32])-algebraic[34])+algebraic[43]+algebraic[45]+algebraic[46]+algebraic[41]
    algebraic[51] = algebraic[17]*states[16]
    rates[16] = ((algebraic[30]-algebraic[43])-algebraic[46])-algebraic[51]
    algebraic[49] = algebraic[24]*states[3]
    algebraic[52] = constants[0]*(constants[44]+constants[45]*states[8])
    rates[3] = ((algebraic[52]-algebraic[49])-algebraic[30])+algebraic[43]+algebraic[51]
    return(rates)

def computeAlgebraic(constants, states, voi):
    algebraic = array([[0.0] * len(voi)] * sizeAlgebraic)
    states = array(states)
    voi = array(voi)
    algebraic[7] = constants[0]*constants[65]*states[18]
    algebraic[8] = constants[74]*states[20]
    algebraic[15] = constants[20]*states[4]
    algebraic[3] = constants[0]*((constants[18]*((states[4]/constants[22])**2.00000))/(((states[4]/constants[22])**2.00000)+1.00000)+constants[19]*states[5])
    algebraic[14] = constants[17]*states[5]
    algebraic[2] = (constants[0]*constants[16])/(((states[4]/constants[23])**2.00000)+1.00000)
    algebraic[6] = constants[62]*states[13]*constants[64]
    algebraic[18] = constants[63]*states[18]
    algebraic[11] = constants[68]*states[21]
    algebraic[20] = constants[0]*constants[66]+constants[67]*states[2]
    algebraic[9] = (constants[71]*states[2]*(1.00000-states[19]))/((constants[77]-states[19])+1.00000)
    algebraic[19] = (constants[72]*states[20]*states[19])/(constants[78]+states[19])
    algebraic[1] = ((constants[7]+constants[6]*constants[15])*(1.00000-states[0]))/((constants[10]-states[0])+1.00000)
    algebraic[13] = constants[8]*(constants[12]*states[1]+constants[13]*states[2]+constants[14]*states[3])
    algebraic[21] = (algebraic[13]*states[0])/(constants[11]+states[0])
    algebraic[0] = constants[0]*((constants[1]*((states[2]/constants[9])**2.00000))/(((states[2]/constants[9])**2.00000)+1.00000)+constants[2])
    algebraic[12] = constants[5]*constants[15]+constants[4]*(1.00000-states[0])+constants[3]*states[0]
    algebraic[22] = algebraic[12]*states[2]
    algebraic[16] = states[10]*constants[26]*(constants[40]*constants[35]+constants[33]*states[1]+constants[34]*states[2]+constants[36]*states[3])
    algebraic[23] = states[11]*constants[26]*(constants[40]*constants[35]+constants[33]*states[1]+constants[34]*states[2]+constants[36]*states[3])
    algebraic[25] = states[6]*constants[26]*(constants[40]*constants[35]+constants[33]*states[1]+constants[34]*states[2]+constants[36]*states[3])
    algebraic[4] = constants[39]/(constants[27]*constants[37]*(states[1]+states[3]+constants[38]*states[2])+1.00000)
    algebraic[27] = states[7]*(constants[25]*(constants[39]-algebraic[4])+constants[24]*algebraic[4])
    algebraic[29] = states[10]*constants[32]
    algebraic[31] = states[8]*(constants[29]+constants[30]*(states[1]+states[2]))
    algebraic[33] = states[9]*constants[28]
    algebraic[35] = states[8]*states[6]*constants[31]
    algebraic[26] = constants[48]*states[15]
    algebraic[34] = constants[49]*states[12]*states[17]
    algebraic[36] = constants[50]*states[15]
    algebraic[17] = constants[42]+constants[43]*(constants[56]*states[1]+constants[57]*states[2]+constants[58]*states[3])
    algebraic[39] = algebraic[17]*states[15]
    algebraic[5] = constants[0]*constants[21]*states[4]
    algebraic[28] = constants[48]*states[17]
    algebraic[37] = states[11]*constants[32]
    algebraic[40] = states[6]*states[9]*constants[31]
    algebraic[42] = states[11]*constants[28]
    algebraic[44] = states[10]*(constants[29]+constants[30]*(states[1]+states[2]))
    algebraic[32] = constants[51]*states[12]*states[1]
    algebraic[41] = constants[54]*constants[15]*states[14]
    algebraic[45] = constants[52]*states[14]
    algebraic[47] = algebraic[17]*states[14]
    algebraic[38] = constants[54]*constants[15]*states[1]
    algebraic[50] = constants[0]*constants[53]*states[8]*states[13]
    algebraic[30] = constants[51]*states[12]*states[3]
    algebraic[43] = constants[52]*states[16]
    algebraic[24] = (constants[47]*(constants[59]*(states[1]+states[3])+constants[60]*states[2]))/(constants[61]+constants[55])+constants[46]
    algebraic[46] = algebraic[24]*states[16]
    algebraic[48] = algebraic[17]*states[12]
    algebraic[51] = algebraic[17]*states[16]
    algebraic[49] = algebraic[24]*states[3]
    algebraic[52] = constants[0]*(constants[44]+constants[45]*states[8])
    algebraic[10] = (constants[69]*states[19]*(states[21]-constants[15]))/((constants[75]-constants[15])+states[21])
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
