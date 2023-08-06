# TheProofIsTrivial

Python port of the javascript based website
[TheProofIsTrivial](http://www.theproofistrivial.com/).

## Installation

```bash
pip install theproofistrivial
```

## Usage

### Python Library

```python
import theproofistrivial

quote = theproofistrivial.QuoteGenerator()
output = quote.create()

print(output)
```

The result is a list:

```
['The proof is trivial! Just biject it to a',
 'combinatorial',
 'field',
 'whose elements are',
 'associative',
 'linear transformations']
```

You can then process the list to make a single string or leave as is:

```python
# Single line string
output = " ".join(output)

# Multi line string
output = "\n".join(output)
```

### Command Line

```bash
theproofistrivial -h
```

```
usage: __main__.py [-h] [-o]

optional arguments:
  -h, --help     show this help message and exit
  -o, --oneline  show output as a single line
```

```bash
theproofistrivial
```

```
The proof is trivial! Just view the problem as a
computable
hypergraph
whose elements are
total
unbounded-fan-in circuits
```

```bash
theproofistrivial -o
```

```
The proof is trivial! Just biject it to an associative semigroup whose elements are perfect manifolds
```
