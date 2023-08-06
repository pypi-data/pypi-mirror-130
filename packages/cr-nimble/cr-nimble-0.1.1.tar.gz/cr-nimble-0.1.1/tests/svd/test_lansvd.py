from svd_setup import *


def test_lanbpro1():
    A =  jnp.eye(4)
    r = cnb.svd.lanbpro_random_start(cnb.KEYS[0], A)
    state = cnb.svd.lanbpro_jit(A, 4, r)
    assert_allclose(state.alpha, 1., atol=atol)
    assert_allclose(state.beta[1:], 0., atol=atol)


def test_lansvd1():
    A =  jnp.eye(4)
    r = cnb.svd.lanbpro_random_start(cnb.KEYS[0], A)
    U, S, V, bnd, n_converged, state = cnb.svd.lansvd_simple_jit(A, 4, r)
    assert_allclose(state.alpha, 1., atol=atol)
    assert_allclose(state.beta[1:], 0., atol=atol)
