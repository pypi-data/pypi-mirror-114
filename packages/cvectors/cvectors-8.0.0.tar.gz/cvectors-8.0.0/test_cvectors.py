import math
import random

import pytest

from cvectors import Vector, angle


def random_vectors(n=1000):
    for _ in range(n):
        components = []
        for _ in range(2):
            if random.randrange(50):
                components.append(
                    random.uniform(
                        -(2 ** random.randint(-5, 5)), 2 ** random.randrange(-5, 5)
                    )
                )
            else:
                components.append(0)
        yield Vector(*components)


def test_equality():
    assert Vector(1, 2) == Vector(1, 2)
    assert Vector(9, -2) == Vector(9, -2)
    assert Vector(0, 0) == Vector(0, -0)


def test_plus():
    assert Vector(2, 3) + Vector(9, 1) == Vector(11, 4)
    assert Vector(0, -3) + Vector(-3, 1) == Vector(-3, -2)


def test_add_distributes():
    for v1, v2 in zip(random_vectors(), random_vectors()):
        assert v1 + v2 == Vector(v1.x + v2.x, v1.y + v2.y)


def test_minus():
    assert Vector(3, 1) - Vector(2, 6) == Vector(1, -5)
    assert Vector(9, 0) - Vector(20, -1) == Vector(-11, 1)


def test_minus_distributes():
    for v1, v2 in zip(random_vectors(), random_vectors()):
        assert v1 - v2 == Vector(v1.x - v2.x, v1.y - v2.y)


def test_scale():
    assert Vector(9, -1) * 2 == Vector(18, -2)
    assert Vector(5, -6) * 0 == Vector(0, 0)
    assert Vector(-3, 2) * -8 == Vector(24, -16)
    assert isinstance(Vector(9, 0) * 3, Vector)
    assert isinstance(-8 * Vector(3, -2), Vector)


def test_div_scale():
    assert Vector(-8, 10) / 4 == Vector(-2, 2.5)
    assert isinstance(Vector(9, 0) / 10, Vector)
    with pytest.raises(TypeError):
        1 / Vector(3, 2)


def test_from_complex():
    for v in random_vectors():
        assert v == Vector(complex(v.x, v.y))
    assert Vector(2 + 3j) == Vector(2, 3)
    assert Vector(1j) == Vector(0, 1)


def test_from_iterable():
    assert Vector((-1, 5)) == Vector(-1, 5)
    assert Vector([-3, 9]) == Vector(-3, 9)
    for v in random_vectors():
        assert v == Vector((v.x, v.y)) == Vector([v.x, v.y])


def test_from_bad_iterable():
    with pytest.raises(ValueError):
        Vector([1])
    with pytest.raises(ValueError):
        Vector([1, 2, 3])


def test_from_random_stuff():
    with pytest.raises(TypeError):

        class Foo:
            pass

        Vector(Foo())
    with pytest.raises(TypeError):
        Vector(lambda x: 0)
    with pytest.raises(TypeError):
        Vector(int)
    with pytest.raises(TypeError):
        Vector("bar")
    with pytest.raises(TypeError):
        Vector(y=3)
    with pytest.raises(TypeError):
        Vector(x="6", y="-3")


def test_repr_():
    assert repr(Vector(5.0, 6.0)) == "Vector(5.0, 6.0)"


def test_str():
    assert str(Vector(-1.0, 1.0)) == "(-1.0 1.0)"


def test_iteration():
    for v in random_vectors():
        for component in v:
            assert component in {v.x, v.y}


def test_properties():
    assert Vector((2, 3)).x == 2
    assert Vector((9, -3)).y == -3


def test_r():
    assert Vector(3, -4).r == abs(Vector(3, -4)) == 5
    assert Vector(0, 0).r == abs(Vector(0, 0)) == 0
    assert Vector.from_polar(r=-1, theta=2).r == 1

    for v in random_vectors():
        assert v.r == abs(v)


def test_theta():
    assert Vector((1, 1)).theta == math.pi / 4
    assert Vector((0, -1)).theta == -math.pi / 2
    assert Vector((-1, -1)).theta == -3 * math.pi / 4
    assert Vector.from_polar(r=2, theta=1).theta == 1


def test_polar_creation():
    assert Vector.from_polar(r=2, theta=0) == Vector(2, 0)
    assert Vector.from_polar(3, math.pi).rec() == pytest.approx(Vector(-3, 0).rec())
    assert Vector.from_polar(theta=0, r=-1) == Vector(-1, 0)
    assert Vector.from_polar(r=0, theta=501).r == 0


def test_getitem():
    vec = Vector(3, -9)
    assert vec[0] == vec[-2] == 3
    assert vec[1] == vec[-1] == -9
    with pytest.raises(IndexError):
        vec[3]
        vec[-3]


def test_slice():
    vec = Vector(-1, 6)
    with pytest.raises(TypeError):
        vec[:]
    with pytest.raises(TypeError):
        vec[0:1]

    for v in random_vectors():
        with pytest.raises(TypeError):
            Vector(v[:])
        with pytest.raises(TypeError):
            v[:1]
        with pytest.raises(TypeError):
            v[1:]


def test_dot():
    assert Vector(-1, 2).dot(Vector(1, 4)) == 7
    assert Vector(0, -2).dot(Vector(9, -1)) == 2


def test_perp_dot():
    assert Vector(-1, 1).perp_dot(Vector(1, 1)) == -2
    assert Vector(0, 1).perp_dot(Vector(0, 1)) == 0


def test_perp():
    assert Vector(3, 1).perp() == Vector(-1, 3)
    assert Vector(-2, 4).perp() == Vector(-4, -2)


def test_round():
    assert Vector(2.3, 1.9).round() == (2, 2)
    assert Vector(1.49, -0.2).round() == (1, 0)
    for i in range(2):
        assert isinstance(Vector(-12.1, 15).round(0)[i], float)
        assert isinstance(Vector(-12.1, 15).round()[i], int)
    assert Vector(5.1209, -3.3211).round(1) == (5.1, -3.3)
    assert Vector(5.1209, -3.3211).round(1) == (5.1, -3.3)


def test_rotate():
    assert Vector(2, 3).rotate(math.pi).rec() == pytest.approx(Vector(-2, -3).rec())
    assert Vector(2, 3).rotate(angle(90, "deg")).rec() == pytest.approx(Vector(-3, 2).rec())
    assert Vector(2, 3).rotate(angle(1, "turn")).rec() == pytest.approx(Vector(2, 3).rec())


def test_unary_minus():
    assert -Vector(-2, 0) == Vector(2, 0)


def test_angles():
    assert angle(30, "deg") == math.pi / 6
    assert angle(2, "turn") == 2 * math.tau
    assert angle(50, "g") == math.pi / 4
    assert angle(-60 * 60, "min") == -math.pi / 3
    assert angle(3600 * 90, "sec") == math.pi / 2
    assert angle(3600 * 90, "sec") == math.pi / 2
    assert angle(2, "rad") == 2
    with pytest.raises(ValueError):
        angle(1, "foo")
        angle(1, "degres")


def test_from_object():
    class Foo:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    with pytest.raises(TypeError):
        Vector(Foo(4, 9))


def test_rec():
    for _ in range(1000):
        x = random.uniform(-999, 999)
        y = random.uniform(-999, 999)
        assert Vector(x, y).rec() == (x, y)


def test_pol():
    for _ in range(1000):
        r = random.uniform(0, 999)
        theta = random.uniform(-math.pi, math.pi)
        pol = Vector.from_polar(r, theta).pol()
        assert math.isclose(r, pol[0])
        assert math.isclose(theta, pol[1])


def test_hat():
    assert Vector(-3, 4).hat() == Vector(-3 / 5, 4 / 5)
    for _ in range(1000):
        vec = Vector.from_polar(r=1, theta=random.uniform(-999, 999)).hat()
        assert vec.hat() == vec


def test_neg():
    for _ in range(1000):
        x = random.uniform(-999, 999)
        y = random.uniform(-999, 999)
        assert -Vector(x, y) == Vector(-x, -y)


def test_reversed():
    for _ in range(1000):
        vec = Vector(random.uniform(-999, 999), random.uniform(-999, 999))
        assert list(reversed(vec)) == list(reversed(list(vec)))


def test_float_perf(benchmark):
    benchmark(Vector, 1.5, 2.3)


def test_int_perf(benchmark):
    benchmark(Vector, -7, 35)


def test_list_perf(benchmark):
    benchmark(Vector, [93, -107.378])


def test_polar_perf(benchmark):
    benchmark(Vector.from_polar, 8.187, 2.17)


def test_components_perf(benchmark):
    def components(v):
        return v.x, v.y

    benchmark(components, Vector(-0.00319, 1.3789))


def test_add_perf(benchmark):
    def add(v1, v2):
        return v1 + v2

    benchmark(add, Vector(-113.131423, 13.1238), Vector(-39.23, 0.229))


def test_sub_perf(benchmark):
    def sub(v1, v2):
        return v1 - v2

    benchmark(sub, Vector(-19.129, -12.397), Vector(-45.21, 4912.397))


def test_mul_perf(benchmark):
    def mul(v, s):
        return v * s

    benchmark(mul, Vector(192.187, 52.137), 83.3897)


def test_div_perf(benchmark):
    def div(v, s):
        return v / s

    benchmark(div, Vector(71.278, -53.129), 67.12)


def test_abs_perf(benchmark):
    benchmark(abs, Vector(18.197, -12.13))


def test_neg_perf(benchmark):
    def neg(v):
        return -v

    benchmark(neg, Vector(81.12987, -789.871))


def test_r_perf(benchmark):
    def r(v):
        return v.r

    benchmark(r, Vector(-1293.138, 178341.18923))


def test_theta_perf(benchmark):
    def theta(v):
        return v.theta

    benchmark(theta, Vector(-1093.318, 89.13789))


def test_dot_perf(benchmark):
    def dot(v1, v2):
        return v1.dot(v2)

    benchmark(dot, Vector(-7.3417, -39.27), Vector(19.287, -71.73))


def test_perp_dot_perf(benchmark):
    def perp_dot(v1, v2):
        return v1.perp_dot(v2)

    benchmark(perp_dot, Vector(-2.1738, 3.197), Vector(1.19007, 6.179))


def test_perp_perf(benchmark):
    def perp(v):
        return v.perp()

    benchmark(perp, Vector(12.378, -17.1879))


def test_hat_perf(benchmark):
    def hat(v):
        return v.hat()

    benchmark(hat, Vector(61.378, 79.12879))


def test_rotate_perf(benchmark):
    def rotate(v, a):
        return v.rotate(a)

    benchmark(rotate, Vector(-3.12, 5.12), 5)


def test_rec_perf(benchmark):
    def rec(v):
        return v.rec()

    benchmark(rec, Vector(-6.13, 78.1378))


def test_pol_perf(benchmark):
    def pol(v):
        return v.pol()

    benchmark(pol, Vector(12.7283, 8.78))


def test_index_perf(benchmark):
    def index(v):
        return (v[0], v[1])

    benchmark(index, Vector(5.213, -7.12))


def test_iter_perf(benchmark):
    def iterate(v):
        for i in v:
            pass

    benchmark(iterate, Vector(-72.1, 6.12))


def test_repr_perf(benchmark):
    benchmark(repr, Vector(6.23, -7.72))


def test_str_perf(benchmark):
    benchmark(str, Vector(-4.2, 9))
