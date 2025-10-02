# WienerAttackRSA

**Implementation of Wiener's RSA attack**

Implementation of Wiener's RSA attack: recover `e` from `d` and `N`, recover `d` from `e` and `N`, and recover prime factors from `(d, N)` or from `(e, d, N)` when the RSA key is vulnerable to Wiener's continued-fraction attack.

---

## Table of contents

* [Overview](#overview)
* [Features](#features)
* [Files / Modules](#files--modules)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)

  * [As a library](#as-a-library)
  * [Example](#example)
* [API reference](#api-reference)
* [How it works (short)](#how-it-works-short)
* [Limitations & security](#limitations--security)
* [Testing](#testing)
* [Contributing](#contributing)
* [License](#license)
* [Author / Credits](#author--credits)

---

## Overview

This repository contains a straight-forward Python implementation of Wiener's attack on RSA. The attack exploits cases where the private exponent `d` is unusually small relative to the modulus `N` (more precisely, when `d < N^{0.25}` under certain conditions), using continued fractions to recover the private key or factors.

The code in this repository includes functions to:

* recover a small `d` given `(e, N)`;
* recover a small `e` (if `d` is known and large) and the prime factors `p, q`;
* recover the prime factors `p, q` given `e, d, N` by searching for a valid `k` such that `e*d = k*phi(N) + 1`.

---

## Features

* Pure Python implementation (no heavy external dependencies).
* Uses continued fractions to generate convergents and test candidate keys.
* Provides small helper functions to get `e`, `d`, and prime factors when keys are vulnerable.

---

## Files / Modules

This README documents the main functions which were taken from the original implementation. The code expects two helper modules to be available in the import path:

* `ContinuedFractions` — functions for converting rationals to continued fraction and computing convergents.
* `Arithmetic` — helper utilities such as `is_perfect_square`.

> The original script used a local sys.path append (see the repository code). Ensure that the helper modules (`ContinuedFractions.py` and `Arithmetic.py`) are present in the repo or available on `PYTHONPATH`.

---

## Requirements

* Python 3.8+
* Standard library modules: `sys`, `math`.
* Local modules: `ContinuedFractions`, `Arithmetic` (provided with the repository or implemented separately).

No third-party packages are required by the core algorithm.

---

## Installation

Clone the repository and ensure the helper modules are available:

```bash
git clone <your-repo-url>
cd WienerAttackRSA
# Make sure ContinuedFractions.py and Arithmetic.py are in the same folder or on PYTHONPATH
```

You can run the functions directly from the files or import them from a package entrypoint if you arrange the code as a proper Python package.

---

## Usage

### As a library

Import the functions from the module and call them from your script or an interactive shell.

```python
# sample usage
from WienerAttackRSA import wiener_attack, get_small_d, get_small_e_and_factors, get_factor

# Example placeholders for e, d and N (replace with actual integers)
e = 65537
N = 0x00  # replace with modulus

# Try to find a small private exponent d from (e, N)
d = get_small_d(e, N)
if d is not None:
    print("Found d:", d)

# If you already have d and N, try to recover e and/or p, q
# e_recovered, p, q = get_small_e_and_factors(d, N)

# If you have e and d, attempt to factor N
# p, q = get_factor(N, e, d)
```

### Example

A simple illustrative example (this is *not* a real vulnerable RSA key — replace with values that are known to be vulnerable if you want to test):

```python
from WienerAttackRSA import get_small_d, get_factor

# vulnerable example values (toy)
e = 17993
N = 90581

d = get_small_d(e, N)
print('Recovered d:', d)

if d:
    p, q = get_factor(N, e, d)
    print('p, q =', p, q)
```

---

## API reference

All functions return `None` (or tuples containing `None`) when they fail to find a vulnerable key.

### `wiener_attack(e, N, max_k=2**20)`

* **Description**: Convenience wrapper that attempts to recover `d` and then factors.
* **Parameters**:

  * `e` — public exponent (int)
  * `N` — RSA modulus (int)
  * `max_k` — maximum `k` value to try when deriving `phi(N)` from the equation `e*d = k*phi(N) + 1` (int, default `2**20` in wrapper)
* **Returns**: `(p, q)` or `(None, None)` if unsuccessful.

### `get_small_e_and_factors(d, N)`

* **Description**: Given a (large) `d` and `N`, attempts to find a small `e` and return `(e, p, q)`.
* **Returns**: `(e, p, q)` on success, otherwise `(None, None, None)`.

### `get_small_d(e, n)`

* **Description**: Applies Wiener continued fraction attack to find the private exponent `d` given `(e, n)`.
* **Returns**: `d` (int) if found, otherwise `None`.

### `get_factor(N, e, d, max_k=1000)`

* **Description**: Given `e`, `d`, and `N`, tries small `k` values to reconstruct `phi(N)` and solve for prime factors `p, q`.
* **Parameters**: `max_k` (default 1000) is the search bound for `k`.
* **Returns**: `(p, q)` on success, otherwise `(None, None)`.

---

## How it works (short)

Wiener's attack uses continued fraction convergents of `e/N` (or `d/N` depending on which value is known) to produce rational approximations `k/d` (or `k/e`) that can reveal small private exponents. If the private exponent `d` is small enough compared to `N` (typically `d < N^{0.25}` under classical assumptions), one of the convergents will yield values satisfying `e*d - 1 = k*phi(N)` and from that `phi(N)` then factors `p` and `q` can be computed.

---

## Limitations & security

* This attack only works when the RSA key is *weak* in the sense described above (small `d`). It does **not** break properly chosen RSA keys.
* Use this code only for educational purposes, testing with your own keys, or authorized security research. Do not use it to attack keys you do not own or are not permitted to test.

---

## Testing

Add unit tests in a `tests/` directory and include known vulnerable test vectors to automate verification. Example test scenarios:

* Known small-`d` RSA keys where the code should recover `d` and factors.
* Negative tests using strong RSA keys where the functions should return `None`.

---

## Contributing

Contributions are welcome! If you want to improve the code, please:

1. Fork the repository.
2. Create a feature branch.
3. Add tests for new behavior.
4. Open a pull request describing your changes.

---

## License

This project is provided under the MIT License — please include an appropriate `LICENSE` file in the repository if you adopt this README.

---

## Author / Credits

~ alocin
---
