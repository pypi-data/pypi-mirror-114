use std::collections::HashMap;

pub(crate) fn mutual_information_internal(
    lhs: Vec<f64>,
    lhs_length: i32,
    rhs: Vec<f64>,
    rhs_length: i32,
) -> f64 {
    let mut joined_histogram_frequency: HashMap<(usize, usize), f64> = HashMap::new();

    let (lhs_freq, lhs_bins) = histogram(
        &lhs,
        (
            lhs.clone().into_iter().fold(std::f64::MAX, f64::min),
            lhs.clone().into_iter().fold(std::f64::MIN, f64::max),
        ),
    );

    let (rhs_freq, rhs_bins) = histogram(
        &rhs,
        (
            rhs.clone().into_iter().fold(std::f64::MAX, f64::min),
            rhs.clone().into_iter().fold(std::f64::MIN, f64::max),
        ),
    );

    for ((_, lhs_bin), (_, rhs_bin)) in lhs_bins.into_iter().zip(rhs_bins) {
        joined_histogram_frequency
            .entry((lhs_bin, rhs_bin))
            .and_modify(|e| *e += 1.0_f64)
            .or_insert(1.0_f64);
    }

    joined_histogram_frequency
        .keys()
        .fold(0.0_f64, |acc, (lhs_bin, rhs_bin)| {
            let joint_prob = match joined_histogram_frequency.get(&(*lhs_bin, *rhs_bin)) {
                Some(frequency) => *frequency / f64::from(lhs_length),
                None => panic!("No Key found for Frequency"),
            };
            let lhs_prob = lhs_freq[*lhs_bin] as f64 / f64::from(lhs_length);
            let rhs_prob = rhs_freq[*rhs_bin] as f64 / f64::from(rhs_length);
            acc + joint_prob * (joint_prob / (lhs_prob * rhs_prob)).log(2.0)
        })
}

fn fold_data<T: 'static, A, B>(data: &[T], fold: A, initialise: B) -> T
where
    A: Fn(T, T) -> T,
    B: FnOnce() -> T,
    T: std::clone::Clone,
{
    let mut state = initialise();
    for elem in data {
        state = fold(state, elem.clone());
    }
    state
}

/// Histogram
/// #Arguments
/// `input` - Slice of Variable Data
/// `bounds` - Min and Max of Variable Data
/// #Returns
/// Vector of Frequency, Bin.
fn histogram(input: &[f64], bounds: (f64, f64)) -> (Vec<f64>, Vec<(f64, usize)>) {
    let mean = fold_data(input, |a, b| a + b, || 0.0) as f64 / input.len() as f64;

    let standard_deviation = (fold_data(
        input,
        |a, b| {
            let x = b - mean;
            a + x * x
        },
        || 0.0,
    ) / input.len() as f64)
        .sqrt();

    // Using Scott's Normal Reference Rule for bin selection
    let bin_width = (standard_deviation * 3.5) / (input.len() as f64).powf(1.0 / 3.0);
    let max_val = bounds.1;
    let min_val = bounds.0;
    let est_bins: usize = ((max_val - min_val) / bin_width) as usize + 1;

    let histogram_parts: Vec<f64> = (0..=(est_bins as usize))
        .map(|i| min_val + bin_width * (i as f64))
        .collect();

    let mut probabilities: Vec<f64> = vec![0.0_f64; est_bins];
    let mut row_histogram: Vec<usize> = Vec::with_capacity(input.len());

    for elem_val in input {
        let histogram_bin: usize = find_bucket(&histogram_parts, *elem_val);
        row_histogram.push(histogram_bin);
        probabilities[histogram_bin] += 1.0_f64;
    }

    (
        probabilities.clone(),
        row_histogram
            .iter()
            .map(|idx| (probabilities[*idx], *idx))
            .collect::<Vec<(f64, usize)>>(),
    )
}

fn find_bucket<T>(data: &[T], elem: T) -> usize
where
    T: std::cmp::PartialOrd,
{
    let index_guess = (data.len() - 1) / 2;
    match elem >= data[index_guess]
        && (index_guess == 0 || index_guess + 1 == data.len() || elem < data[index_guess + 1])
    {
        true => index_guess,
        false => match elem >= data[index_guess] {
            true => index_guess + 1 + find_bucket(&data[(index_guess + 1)..data.len()], elem),
            false => find_bucket(&data[0..=index_guess], elem),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use proptest::prelude::*;
    #[test]
    fn mutual_information_proptest() {
        proptest! {
            fn mutual_information_inputs(s in "([0-9]{1,4}\\.[0-9]{1,6} ){1,100}[0-9]{1,4}\\.[0-9]{1,6}") {
                let input = s
                    .split_whitespace()
                    .map(|r| str::parse::<f64>(r).unwrap())
                    .collect::<Vec<f64>>();
                let bounds = (
                        input.clone().into_iter().fold(std::f64::MAX, f64::min),
                        input.clone().into_iter().fold(std::f64::MIN, f64::max)
                        );
                let (_, hist_bins) = histogram(
                        &input,
                        bounds
                        );
                assert!(!hist_bins.is_empty());
            }
        }
    }
}
