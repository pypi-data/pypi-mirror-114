# Varius
[![test](https://github.com/ChenchaoZhao/varius/actions/workflows/lint-test.yaml/badge.svg)](https://github.com/ChenchaoZhao/varius/actions/workflows/lint-test.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://pypip.in/v/varius/badge.png)](https://pypi.python.org/pypi/varius)

Perform computations using various versions of variables

Varius is the Latin word for "various."

## Install

`pip install varius`

## Usage Examples

```python
import varius
from varius import *

# default variables
cst = vr('cost [usd]', 100)
rev = vr('revenue [usd]', 300)

# expressions: if values are not given the expressions will be symbolic
pft = ex('profit [usd]', rev - cst)
pmg = ex('profit margin', pft.expr/rev)

# show() will display the variables or expressions based on your python env
# if in jupyter notebooks, they will be displayed as beautiful latex equations otherwise as plain texts

with note('default') as d:
    show(cst, rev, pft, pmg)
    pft.grad()
    pmg.grad()
    print(d)

# new case
with note('20% discount', copy='default') as d:
    rev(rev['default'] * 0.8)
    show(cst, rev, pft, pmg)
    pft.grad()
    pmg.grad()
    print(d)


# another case
with note('50% discount', copy='default') as d:
    rev(rev['default'] * 0.5)
    show(cst, rev, pft, pmg)
    pft.grad()
    pmg.grad()
    print(d)

```

You will get summaries as follows:

```
Scope version: default
  Variables:
    (cost [usd]) = 100
    (revenue [usd]) = 300
  Expressions:
    (profit [usd]) = 200
    (profit margin) = 2/3
    ∂ [(profit [usd])] / ∂ [(cost [usd])] = -1
    ∂ [(profit [usd])] / ∂ [(revenue [usd])] = 1
    ∂ [(profit margin)] / ∂ [(cost [usd])] = -1/300
    ∂ [(profit margin)] / ∂ [(revenue [usd])] = 1/900

Scope version: 20% discount
  Variables:
    (cost [usd]) = 100
    (revenue [usd]) = 240.0
  Expressions:
    ∂ [(profit [usd])] / ∂ [(cost [usd])] = -1
    ∂ [(profit [usd])] / ∂ [(revenue [usd])] = 1
    ∂ [(profit margin)] / ∂ [(cost [usd])] = -0.00416666666666667
    ∂ [(profit margin)] / ∂ [(revenue [usd])] = 0.00173611111111111
    (profit [usd]) = 140.000000000000
    (profit margin) = 0.583333333333333    

Scope version: 50% discount
  Variables:
    (cost [usd]) = 100
    (revenue [usd]) = 150.0
  Expressions:
    ∂ [(profit [usd])] / ∂ [(cost [usd])] = -1
    ∂ [(profit [usd])] / ∂ [(revenue [usd])] = 1
    ∂ [(profit margin)] / ∂ [(cost [usd])] = -0.00666666666666667
    ∂ [(profit margin)] / ∂ [(revenue [usd])] = 0.00444444444444445
    (profit [usd]) = 50.0000000000000
    (profit margin) = 0.333333333333333
```
