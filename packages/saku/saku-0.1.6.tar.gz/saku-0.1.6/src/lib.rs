use pyo3::prelude::*;
use regex::{Captures, Regex};

#[pyclass]
pub struct SentenceTokenizer {
    period: String,
    alt_period: String,
    period_newline: String,
    pattern: Regex,
}

#[pymethods]
impl SentenceTokenizer {
    const DEFAULT_PERIOD: &'static str = "。";
    const DEFAULT_ALT_PERIOD: &'static str = "__PERIOD__";
    const DEFAULT_PATTERN_STR: &'static str = r"（.*?）|「.*?」|『.*?』";

    #[new]
    fn __new__(
        period: Option<String>,
        pattern: Option<String>,
        patterns: Option<Vec<String>>,
        alt_period: Option<String>,
    ) -> PyResult<Self> {
        let period = period.unwrap_or(Self::DEFAULT_PERIOD.to_string());
        let period_newline = format!("{}\n", &period);
        let pattern = pattern.map(|p| Regex::new(&p).unwrap()).unwrap_or({
            patterns
                .map(|patterns| Regex::new(&patterns.join("|")).unwrap())
                .unwrap_or(Regex::new(Self::DEFAULT_PATTERN_STR).unwrap())
        });
        let alt_period = alt_period.unwrap_or(Self::DEFAULT_ALT_PERIOD.to_string());
        Ok(Self {
            period,
            period_newline,
            pattern,
            alt_period,
        })
    }

    fn tokenize(
        &self,
        mut text: String,
        preserve_newline: Option<bool>,
    ) -> PyResult<Vec<String>> {
        let preserve_newline = preserve_newline.unwrap_or(false);
        if !preserve_newline {
            text = text.replace("\n", "").replace("\r", "");
        };
        Ok(self
            .pattern
            .replace_all(&text, |caps: &Captures| {
                caps[0].replace(&self.period, &self.alt_period)
            })
            .trim()
            .replace(&self.period, &self.period_newline)
            .split("\n")
            .map(|s| s.trim().to_string())
            .collect())
    }
}

#[pymodule]
fn saku(_: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<SentenceTokenizer>()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
    }

}
