import numpy as np
from numpy.linalg import inv as npinv


def inverse(inn):
    # print 'calling optimal_estimation_core_pure_python: inverse'
    try:
        out=npinv(inn)
    except np.linalg.LinAlgError:
        # TODO
        # Is this always smart?
        #or better to flag ..
        out=np.zeros_like(inn)
    return out

def right_inverse(inn):
    # print 'calling optimal_estimation_core_pure_python: right_inverse'
    return np.dot(inn.T, inverse(np.dot(inn, inn.T)))

def left_inverse(inn):
    # print 'calling optimal_estimation_core_pure_python: left_inverse'
    return np.dot(inverse(np.dot(inn.T, inn)), inn.T)

#bit useless
#Todo refactor
def clipper(a, b, x):
    # print 'calling optimal_estimation_core_pure_python: clipper'
    return np.clip(x, a, b)



def norm_error_weighted_x(ix, sri):
    # see Rodgers for details
    # ix : increment of x = x_i -x_i+1
    # sri: inverse of retrieval error co-variance
    # print 'calling optimal_estimation_core_pure_python: norm_error_weighted_x'
    return np.dot(ix.T, np.dot(sri, ix))

def norm_y(inn):
    return (inn * inn).mean()





#######################################################################
#######################################################################
#######################################################################
#######################################################################
###Gauss Newton Operator
def newton_operator(a, b, x, y, k):
    '''

    :param a: lower limit of x np.array with 1 dimension
    :param b: upper limit of x np.array with same length  as a
    :param x: state vector
    :param y: fnc(x)
    :param k: dfnc(x)
    :return: cnx (clipped) root of fnc for the linear case, last y=fnc(x), last increment of x
    '''
    # print 'calling optimal_estimation_core_pure_python: newton_operator'
    ki = left_inverse(k)
    incr_x = np.dot(ki, y)
    cnx = clipper(a, b, x - incr_x)
    return cnx, incr_x, None, None
def newton_cost(x,fnc):
    '''
    L2 norm
    :param x:
    :param fnc:
    :return:
    '''
    # print 'calling optimal_estimation_core_pure_python: newton_cost'
    y=fnc(x)
    cost = np.dot(y.T, y)
    return cost
def newton_ret_err_cov_i(x,dfnc):
    return None
def newton_ret_err_cov(x,dfnc):
    return None

def newton_gain_aver_cost(x, y, k):
    '''
    Calculates Gain, averagiong kernel matrix and cost
    :param y:
    :param x:
    :param k:
    :return:
    '''
    # print 'calling optimal_estimation_core_pure_python: newton_gain_aver_cost'
    # gain matrix
    gain = left_inverse(k)
    # averaging kernel
    aver = np.identity(x.size)
    # cost function
    cost = np.dot(y.T, y)
    return gain, aver, cost


#######################################################################
#######################################################################
#######################################################################
#######################################################################
###Gauss Newton with measurement error
def newton_operator_with_se(a, b, x, y, k, sei):
    '''

    :param a: lower limit of x np.array with 1 dimension
    :param b: upper limit of x np.array with same length  as a
    :param x: state vector
    :param y: fnc(x)
    :param k: dfnc(x)
    :param sei: inverse of measurement error co-variance
    :return: cnx (clipped) root of fnc for the linear case, last y=fnc(x), last increment of x, last
            retrieval error co.-variance
    '''
    # print 'calling optimal_estimation_core_pure_python: newton_operator_with_se'
    #print 'sei',sei
    kt_sei = np.dot(k.T, sei)
    #print 'kt_sei',kt_sei
    ret_err_cov_i = (np.dot(kt_sei, k))
    #print 'ret_err_cov_i',ret_err_cov_i
    ret_err_cov = inverse(ret_err_cov_i)
    #print 'ret_err_cov',ret_err_cov
    kt_sei_y = np.dot(kt_sei, y)
    #print 'kt_sei_y',kt_sei_y
    incr_x = np.dot(ret_err_cov, kt_sei_y)
    #print 'nx',x - incr_x
    cnx = clipper(a, b, x - incr_x)
    #print 'cnx',cnx
    return cnx, incr_x, ret_err_cov_i, ret_err_cov
def newton_se_ret_err_cov_i(k,sei):
    kt_sei = np.dot(k.T, sei)
    # inverse retrieval error co-variance
    kt_sei_k = np.dot(kt_sei, k)
    return kt_sei_k
def newton_se_ret_err_cov(k,sei):
    return inverse(newton_se_ret_err_cov_i(k,sei))
def newton_se_cost(x,y,sei):
    cost = np.dot(y.T, np.dot(sei, y))
    return cost
def newton_se_gain_aver_cost(x, y, k, sei,ret_err_cov):
    #retrieval error co-varince
    gain = np.dot(ret_err_cov, np.dot(k.T, sei))
    # averaging kernel
    # aver=np.dot(gain,k)
    aver = np.identity(x.size)
    # cost function
    cost = np.dot(y.T, np.dot(sei, y))
    return gain, aver, cost

#######################################################################
#######################################################################
#######################################################################
#######################################################################
###Optimal estmation with Gauss Newton
def optimal_estimation_gauss_newton_operator(a, b, x, y, k, sei, sai, xa):
    '''

    :param a: lower limit of x np.array with 1 dimension
    :param b: upper limit of x np.array with same length  as a
    :param x: state vector
    :param y: fnc(x)
    :param k: dfnc(x)
    :param sei: inverse of measurement error co-variance
    :param sai: inverse of prior error co-variance
    :param xa: prior
    :return: cnx (clipped) optimal solution for  fnc-1 for the linear case, last y=fnc(x), last increment of x, last
            retrieval error co.-variance
    '''
    # print 'calling optimal_estimation_core_pure_python: optimal_estimation_gauss_newton_operator'
    kt_sei = np.dot(k.T, sei)
    kt_sei_k = (np.dot(kt_sei, k))
    # inverse retrieval error co-variance
    ret_err_cov_i = sai + kt_sei_k
    # retrieval error co-variance
    ret_err_cov = inverse(ret_err_cov_i)
    kt_sei_y = np.dot(kt_sei, y)
    sai_dx = np.dot(sai, xa - x)
    incr_x = np.dot(ret_err_cov, kt_sei_y - sai_dx)
    cnx = clipper(a, b, x - incr_x)
    return cnx, incr_x, ret_err_cov_i, ret_err_cov
def oe_ret_err_cov_i(k,sei,sai):
    kt_sei = np.dot(k.T, sei)
    kt_sei_k = np.dot(kt_sei, k)
    # inverse retrieval error co-variance
    ret_err_cov_i = sai + kt_sei_k
    return ret_err_cov_i
def oe_ret_err_cov(k,sei,sai):
    return inverse(oe_ret_err_cov_i(k,sei,sai))
def oe_cost(x,xa,fnc,sei,sai):
    y=fnc(x)
    cost = np.dot((xa - x).T, np.dot(sai, xa - x)) + \
        np.dot(y.T, np.dot(sei, y))
    return cost
def oe_gain_aver_cost(x, y, k, xa, sei, sai,ret_err_cov):
    # gain matrix
    gain = np.dot(ret_err_cov, np.dot(k.T, sei))
    # averaging kernel
    aver = np.dot(gain, k)
    # cost function
    cost = np.dot((xa - x).T, np.dot(sai, xa - x)) + \
        np.dot(y.T, np.dot(sei, y))
    return gain, aver, cost
