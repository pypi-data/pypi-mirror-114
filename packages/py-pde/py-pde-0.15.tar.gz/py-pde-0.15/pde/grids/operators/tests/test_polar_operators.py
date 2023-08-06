"""
.. codeauthor:: David Zwicker <david.zwicker@ds.mpg.de>
"""

import numpy as np
import pytest

from pde import CartesianGrid, PolarSymGrid, ScalarField, Tensor2Field, VectorField
from pde.grids.operators import polar_sym as ops


def test_findiff():
    """test operator for a simple polar grid"""
    grid = PolarSymGrid(1.5, 3)
    _, _, r2 = grid.axes_coords[0]
    assert grid.discretization == (0.5,)
    s = ScalarField(grid, [1, 2, 4])
    v = VectorField(grid, [[1, 2, 4], [0] * 3])

    # test gradient
    grad = s.gradient(bc="value")
    np.testing.assert_allclose(grad.data[0, :], [1, 3, -6])
    grad = s.gradient(bc="derivative")
    np.testing.assert_allclose(grad.data[0, :], [1, 3, 2])

    # test divergence
    div = v.divergence(bc="value")
    np.testing.assert_allclose(div.data, [5, 17 / 3, -6 + 4 / r2])
    div = v.divergence(bc="derivative")
    np.testing.assert_allclose(div.data, [5, 17 / 3, 2 + 4 / r2])


def test_conservative_laplace():
    """test and compare the two implementation of the laplace operator"""
    grid = PolarSymGrid(1.5, 8)
    f = ScalarField.random_uniform(grid)

    bcs = grid.get_boundary_conditions("natural")
    lap = ops.make_laplace(bcs)
    np.testing.assert_allclose(f.apply(lap).integral, 0, atol=1e-12)


@pytest.mark.parametrize(
    "make_op,field,rank",
    [
        (ops.make_laplace, ScalarField, 0),
        (ops.make_divergence, VectorField, 0),
        (ops.make_gradient, ScalarField, 0),
        (ops.make_tensor_divergence, Tensor2Field, 1),
    ],
)
def test_small_annulus(make_op, field, rank):
    """test whether a small annulus gives the same result as a sphere"""
    grids = [
        PolarSymGrid((0, 1), 8),
        PolarSymGrid((1e-8, 1), 8),
        PolarSymGrid((0.1, 1), 8),
    ]

    f = field.random_uniform(grids[0])

    res = [make_op(g.get_boundary_conditions(rank=rank))(f.data) for g in grids]

    np.testing.assert_almost_equal(res[0], res[1], decimal=5)
    assert np.linalg.norm(res[0] - res[2]) > 1e-3


def test_grid_laplace():
    """test the polar implementation of the laplace operator"""
    grid_sph = PolarSymGrid(7, 8)
    grid_cart = CartesianGrid([[-5, 5], [-5, 5]], [12, 11])

    a_1d = ScalarField.from_expression(grid_sph, "cos(r)")
    a_2d = a_1d.interpolate_to_grid(grid_cart)

    b_2d = a_2d.laplace("natural")
    b_1d = a_1d.laplace("natural")
    b_1d_2 = b_1d.interpolate_to_grid(grid_cart)

    i = slice(1, -1)  # do not compare boundary points
    np.testing.assert_allclose(b_1d_2.data[i, i], b_2d.data[i, i], rtol=0.2, atol=0.2)


@pytest.mark.parametrize("r_inner", (0, 1))
def test_gradient_squared(r_inner):
    """compare gradient squared operator"""
    grid = PolarSymGrid((r_inner, 5), 64)
    field = ScalarField.random_harmonic(grid, modes=1)
    s1 = field.gradient("natural").to_scalar("squared_sum")
    s2 = field.gradient_squared("natural", central=True)
    np.testing.assert_allclose(s1.data, s2.data, rtol=0.1, atol=0.1)
    s3 = field.gradient_squared("natural", central=False)
    np.testing.assert_allclose(s1.data, s3.data, rtol=0.1, atol=0.1)
    assert not np.array_equal(s2.data, s3.data)


def test_grid_div_grad():
    """compare div grad to laplacian for polar grids"""
    grid = PolarSymGrid(2 * np.pi, 16)
    r = grid.axes_coords[0]
    arr = np.cos(r)

    laplace = grid.get_operator("laplace", "derivative")
    grad = grid.get_operator("gradient", "derivative")
    div = grid.get_operator("divergence", "value")
    a = laplace(arr)
    b = div(grad(arr))
    res = -np.sin(r) / r - np.cos(r)

    # do not test the radial boundary points
    np.testing.assert_allclose(a[1:-1], res[1:-1], rtol=0.1, atol=0.1)
    np.testing.assert_allclose(b[1:-1], res[1:-1], rtol=0.1, atol=0.1)


def test_poisson_solver_polar():
    """test the poisson solver on Polar grids"""
    grid = PolarSymGrid(4, 8)
    for bc_val in ["natural", {"value": 1}]:
        bcs = grid.get_boundary_conditions(bc_val)
        poisson = grid.get_operator("poisson_solver", bcs)
        laplace = grid.get_operator("laplace", bcs)

        d = np.random.random(grid.shape)
        d -= ScalarField(grid, d).average  # balance the right hand side
        res = laplace(poisson(d))
        np.testing.assert_allclose(res, d, rtol=1e-6, err_msg=f"bcs = {bc_val}")

    grid = PolarSymGrid([2, 4], 8)
    for bc_val in ["natural", {"value": 1}]:
        bcs = grid.get_boundary_conditions(bc_val)
        poisson = grid.get_operator("poisson_solver", bcs)
        laplace = grid.get_operator("laplace", bcs)

        d = np.random.random(grid.shape)
        d -= ScalarField(grid, d).average  # balance the right hand side
        res = laplace(poisson(d))
        np.testing.assert_allclose(res, d, rtol=1e-6, err_msg=f"bcs = {bc_val}")


def test_examples_scalar_polar():
    """compare derivatives of scalar fields for polar grids"""
    grid = PolarSymGrid(1, 32)
    sf = ScalarField.from_expression(grid, "r**3")

    # gradient
    res = sf.gradient([{"derivative": 0}, {"derivative": 3}])
    expect = VectorField.from_expression(grid, ["3 * r**2", 0])
    np.testing.assert_allclose(res.data, expect.data, rtol=0.1, atol=0.1)

    # gradient squared
    expect = ScalarField.from_expression(grid, "9 * r**4")
    for c in [True, False]:
        res = sf.gradient_squared([{"derivative": 0}, {"derivative": 3}], central=c)
        np.testing.assert_allclose(res.data, expect.data, rtol=0.1, atol=0.1)

    # laplace
    res = sf.laplace([{"derivative": 0}, {"derivative": 3}])
    expect = ScalarField.from_expression(grid, "9 * r")
    np.testing.assert_allclose(res.data, expect.data, rtol=0.1, atol=0.1)


def test_examples_vector_polar():
    """compare derivatives of vector fields for polar grids"""
    grid = PolarSymGrid(1, 32)
    vf = VectorField.from_expression(grid, ["r**3", "r**2"])

    # divergence
    res = vf.divergence([{"derivative": 0}, {"value": 1}])
    expect = ScalarField.from_expression(grid, "4 * r**2")
    np.testing.assert_allclose(res.data, expect.data, rtol=0.1, atol=0.1)

    # # vector Laplacian
    # res = vf.laplace([{"derivative": 0}, {"value": 1}])
    # expect = VectorField.from_expression(grid, ["8 * r", "3"])
    # np.testing.assert_allclose(res.data, expect.data, rtol=0.1, atol=0.1)

    # vector gradient
    res = vf.gradient([{"derivative": 0}, {"value": [1, 1]}])
    expr = [["3 * r**2", "-r"], ["2 * r", "r**2"]]
    expect = Tensor2Field.from_expression(grid, expr)
    np.testing.assert_allclose(res.data, expect.data, rtol=0.1, atol=0.1)


def test_examples_tensor_polar():
    """compare derivatives of tensorial fields for polar grids"""
    grid = PolarSymGrid(1, 32)
    tf = Tensor2Field.from_expression(grid, [["r**3"] * 2] * 2)

    # tensor divergence
    res = tf.divergence([{"derivative": 0}, {"value": [1, 1]}])
    expect = VectorField.from_expression(grid, ["3 * r**2", "5 * r**2"])
    np.testing.assert_allclose(res.data, expect.data, rtol=0.1, atol=0.1)
