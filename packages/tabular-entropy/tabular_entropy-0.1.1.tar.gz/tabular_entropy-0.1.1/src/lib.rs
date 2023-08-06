use pyo3::prelude::*;

mod mutual_info;
use mutual_info::mutual_information_internal;

use pyo3::{exceptions::PyValueError, PyErr, Python};

#[pyfunction]
/// Calculate Mutual Information for Two paired Vectors
///
/// Will fail if the two vectors are not the same length.
fn mutual_information(a: Vec<f64>, b: Vec<f64>) -> PyResult<f64> {
    let a_len = a.len();
    if a_len == b.len() {
        Ok(mutual_information_internal(
            a,
            a_len as i32,
            b,
            a_len as i32,
        ))
    } else {
        Err(Python::with_gil(|py| {
            PyErr::from_instance(
                PyValueError::new_err(format!(
                    "Input A {} and B {} did not match in size",
                    a.len(),
                    b.len()
                ))
                .instance(py),
            )
        }))
    }
}

#[pymodule]
fn tabular_entropy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(mutual_information))?;
    Ok(())
}
