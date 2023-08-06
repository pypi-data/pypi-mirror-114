cimport cython
cimport numpy as np

ctypedef np.float64_t data_type_t

cpdef data_type_t logpmf(data_type_t x, data_type_t a, data_type_t b) nogil
cpdef data_type_t pmf(data_type_t x, data_type_t a, data_type_t b) nogil

cpdef data_type_t log_likelihood(data_type_t [:] data, data_type_t a, data_type_t b) nogil
cpdef data_type_t neg_log_likelihood_exp_hyper(data_type_t [:] par, data_type_t [:] data, data_type_t lam) nogil

cpdef data_type_t [:] mle_ab(data_type_t [:] par, double n, double s1, double s2)