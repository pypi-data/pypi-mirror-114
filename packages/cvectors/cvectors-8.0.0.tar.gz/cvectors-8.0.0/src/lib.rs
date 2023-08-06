use pyo3::{
    basic::CompareOp,
    exceptions::{PyIndexError, PyTypeError, PyValueError, PyZeroDivisionError},
    prelude::*,
    types::{PyComplex, PyIterator, PyString},
    wrap_pyfunction, PyNumberProtocol, PyObjectProtocol, PySequenceProtocol,
};
use std::f64::consts::TAU;
use std::iter::Iterator;
/// Convert an angle to radians.
#[pyfunction]
#[pyo3(text_signature = "(angle, /, unit)")]
fn angle(angle: f64, unit: &str) -> PyResult<f64> {
    match unit {
        "d" | "deg" | "degrees" | "degree" | "°" => Ok(angle * TAU / 360.0),
        "r" | "rad" | "radian" | "radians" => Ok(angle),
        "g" | "grad" | "gradians" | "gradian" | "gons" | "gon" | "grades" | "grade" => {
            Ok(angle * TAU / 400.0)
        }
        "mins" | "min" | "minutes" | "minute" | "'" | "′" => Ok(angle * TAU / 21600.0),
        "secs" | "sec" | "seconds" | "second" | "\"" | "″" => Ok(angle * TAU / 1296000.0),
        "turn" | "turns" => Ok(angle * TAU),
        _ => Err(PyValueError::new_err(format!(
            "invalid angle unit: '{}'",
            unit
        ))),
    }
}

/// A two-dimensional vector.
#[pyclass(module = "cvectors", subclass)]
#[pyo3(text_signature = "($self, /, x, y)")]
struct Vector {
    /// The horizontal component of the vector.
    #[pyo3(get)]
    x: f64,
    /// The vertical component of the vector.
    #[pyo3(get)]
    y: f64,
}

#[pymethods]
impl Vector {
    /// Create a Vector from a single argument or x, y pair.
    #[new]
    pub fn new(py: Python, x: PyObject, y: Option<f64>) -> PyResult<Self> {
        if let Some(yv) = y {
            Ok(Vector {
                x: x.extract(py)?,
                y: yv,
            })
        } else {
            {
                let x = x.as_ref(py);
                if let Ok(complex) = x.downcast::<PyComplex>() {
                    return Ok(Vector {
                        x: complex.real(),
                        y: complex.imag(),
                    });
                }
                if let Ok(_) = x.downcast::<PyString>() {
                    return Err(PyTypeError::new_err("cannot create Vector from string"));
                }
                let x = match x.call_method0("__iter__") {
                    Ok(y) => y,
                    Err(_) => {
                        return Err(PyTypeError::new_err(
                            "single argument Vector must be Vector, complex or iterable",
                        ))
                    }
                };
                let mut list = x.downcast::<PyIterator>().unwrap().iter().unwrap();
                if let (Some(value0), Some(value1)) = (list.next(), list.next()) {
                    if let Some(_) = list.next() {
                        Err(PyValueError::new_err(
                            "iterable is too long to create Vector",
                        ))
                    } else {
                        Ok(Vector {
                            x: value0?.extract()?,
                            y: value1?.extract()?,
                        })
                    }
                } else {
                    Err(PyValueError::new_err(
                        "iterable is too short to create Vector",
                    ))
                }
            }
        }
    }
    /// Create a Vector from polar coordinates.
    #[staticmethod]
    #[pyo3(text_signature = "(r, theta)")]
    fn from_polar(r: f64, theta: f64) -> Self {
        let (y, x) = theta.sin_cos();
        Vector { x: r * x, y: r * y }
    }
    /// Return the dot product of self and other.
    #[pyo3(text_signature = "($self, other, /)")]
    fn dot(&self, other: &Vector) -> f64 {
        self.x * other.x + self.y * other.y
    }
    /// Return the perp dot product of self and other.
    ///
    /// This is the signed area of the parallelogram they define. It is
    /// also one of the 'cross products' that can be defined on 2D
    /// vectors.
    #[pyo3(text_signature = "($self, other, /)")]
    fn perp_dot(&self, other: &Vector) -> f64 {
        self.x * other.y - self.y * other.x
    }
    /// Return the Vector, rotated anticlockwise by pi / 2.
    ///
    /// This is one of the 'cross products' that can be defined on 2D
    /// vectors. Use -Vector.perp() for a clockwise rotation.
    #[pyo3(text_signature = "($self, /)")]
    fn perp(&self) -> Vector {
        Vector {
            x: -self.y,
            y: self.x,
        }
    }
    /// Return a self, rotated by angle anticlockwise.
    ///
    /// Use negative angles for a clockwise rotation.
    #[pyo3(text_signature = "($self, /, angle)")]
    fn rotate(&self, angle: f64) -> Vector {
        Vector::from_polar(self.r(), self.theta() + angle)
    }
    /// Return a Vector with the same direction, but unit length.
    #[pyo3(text_signature = "($self, /)")]
    fn hat(&self) -> Vector {
        let r = self.r();
        Vector {
            x: self.x / r,
            y: self.y / r,
        }
    }
    /// Get the vector as (x, y).
    #[pyo3(text_signature = "($self, /)")]
    fn rec(&self) -> (f64, f64) {
        (self.x, self.y)
    }
    /// Get the vector as (r, theta).
    #[pyo3(text_signature = "($self, /)")]
    fn pol(&self) -> (f64, f64) {
        (self.r(), self.theta())
    }
    /// Get the vector with both components rounded, as a tuple.
    #[pyo3(text_signature = "($self, /, ndigits=None)")]
    fn round(&self, py: Python, ndigits: Option<i32>) -> (PyObject, PyObject) {
        if let Some(i) = ndigits {
            let power = 10.0_f64.powi(i);
            (
                ((power * self.x).round() / power).into_py(py),
                ((power * self.y).round() / power).into_py(py),
            )
        } else {
            (
                (self.x.round() as i32).into_py(py),
                (self.y.round() as i32).into_py(py),
            )
        }
    }
    /// The radius of the vector.
    #[getter]
    fn r(&self) -> f64 {
        self.x.hypot(self.y)
    }
    /// The angle of the vector, anticlockwise from the horizontal.
    ///
    /// Negative values are clockwise. Returns values in the range
    /// [-pi, pi]. See documentation of cmath.phase for details.
    #[getter]
    fn theta(&self) -> f64 {
        self.y.atan2(self.x)
    }
}
#[pyproto]
impl PyObjectProtocol for Vector {
    fn __str__(&self) -> String {
        format!("({:?} {:?})", self.x, self.y)
    }
    fn __repr__(&self) -> String {
        format!("Vector({:?}, {:?})", self.x, self.y)
    }
    fn __bool__(&self) -> bool {
        self.x != 0.0 || self.y != 0.0
    }
    fn __richcmp__(&self, other: PyRef<'p, Self>, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Eq => Ok(self.x == other.x && self.y == other.y),
            CompareOp::Ne => Ok(self.x != other.x || self.y != other.y),
            CompareOp::Lt => Err(PyTypeError::new_err(
                "'<' not supported between instances of 'Vector' and 'Vector'",
            )),
            CompareOp::Gt => Err(PyTypeError::new_err(
                "'>' not supported between instances of 'Vector' and 'Vector'",
            )),
            CompareOp::Le => Err(PyTypeError::new_err(
                "'<=' not supported between instances of 'Vector' and 'Vector'",
            )),
            CompareOp::Ge => Err(PyTypeError::new_err(
                "'>=' not supported between instances of 'Vector' and 'Vector'",
            )),
        }
    }
}
#[pyproto]
impl PySequenceProtocol for Vector {
    fn __len__(&self) -> usize {
        2
    }
    fn __getitem__(&self, index: isize) -> PyResult<f64> {
        match index {
            0 => Ok(self.x),
            1 => Ok(self.y),
            _ => Err(PyIndexError::new_err("Vector index out of range")),
        }
    }
}
#[pyproto]
impl PyNumberProtocol for Vector {
    fn __neg__(&self) -> Vector {
        Vector {
            x: -self.x,
            y: -self.y,
        }
    }
    fn __add__(lhs: PyRef<'p, Self>, rhs: PyRef<'p, Self>) -> Vector {
        Vector {
            x: lhs.x + rhs.x,
            y: lhs.y + rhs.y,
        }
    }
    fn __sub__(lhs: PyRef<'p, Self>, rhs: PyRef<'p, Self>) -> Vector {
        Vector {
            x: lhs.x - rhs.x,
            y: lhs.y - rhs.y,
        }
    }
    fn __mul__(lhs: PyRef<'p, Self>, rhs: f64) -> Vector {
        Vector {
            x: lhs.x * rhs,
            y: lhs.y * rhs,
        }
    }
    fn __rmul__(&self, other: f64) -> Vector {
        Vector {
            x: self.x * other,
            y: self.y * other,
        }
    }
    fn __truediv__(lhs: PyRef<'p, Self>, rhs: f64) -> PyResult<Vector> {
        if rhs == 0.0 {
            Err(PyZeroDivisionError::new_err("Vector division by zero"))
        } else {
            Ok(Vector {
                x: lhs.x / rhs,
                y: lhs.y / rhs,
            })
        }
    }
    fn __abs__(&self) -> f64 {
        self.r()
    }
}
#[pymodule]
fn cvectors(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Vector>()?;
    m.add_function(wrap_pyfunction!(angle, m)?).unwrap();
    Ok(())
}
