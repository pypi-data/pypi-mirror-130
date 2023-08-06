from ls_setup import *

def test_lxb():
    n = 5
    L = jnp.eye(n)
    b = jnp.ones(n)
    x = cnb.solve_Lx_b(L, b)
    assert jnp.allclose(b, x)

def test_ltxb():
    n = 5
    L = jnp.eye(n)
    b = jnp.ones(n)
    x = cnb.solve_LTx_b(L, b)
    assert jnp.allclose(b, x)

def test_uxb():
    n = 5
    L = jnp.eye(n)
    b = jnp.ones(n)
    x = cnb.solve_Ux_b(L, b)
    assert jnp.allclose(b, x)

def test_utxb():
    n = 5
    L = jnp.eye(n)
    b = jnp.ones(n)
    x = cnb.solve_UTx_b(L, b)
    assert jnp.allclose(b, x)

def test_spd_chol():
    n = 5
    L = jnp.eye(n)
    b = jnp.ones(n)
    x = cnb.solve_spd_chol(L, b)
    assert jnp.allclose(b, x)

