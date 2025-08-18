# Unit and Physical Quantity Calculation Package

This project is a Python package for SI unit and physical quantity calculation, supporting automatic unit conversion, parsing, and arithmetic. It is suitable for scientific computing, engineering, and education.

## Features

- Supports SI base units, derived units, and common prefixes (e.g., mm, km, μs)
- Parses complex unit expressions (e.g., `"kg*m^2/s^2"`, `"N*m"`, `"1/mol"`)
- Automatic unit conversion and compatibility checking
- Arithmetic operations on physical quantities (value + unit)
- Built-in physical constants (e.g., c, h, g, N_A)

## Installation

Simply copy the `SI/` directory into your project.

## Quick Start

```python
from SI import Unit, Quantity, Constants

# Unit parsing and conversion
a = 3 * Unit("m")
b = 5 * Unit("mm")
print(b.to("m"))  # 0.005

# Unit arithmetic
area = a * b / 2
print(area)       # 0.0075 m^2

# Quantity conversion
d = 1.30 * Unit("m")
t = d / Constants.c * 1.33
print(t.to("ns")) # Time for light to travel 1.33m in a medium, in ns

# Physical constants
print(Constants.c)    # Speed of light
print(Constants.h)    # Planck constant
print(Constants.N_A)  # Avogadro constant
```

## Main Modules

- `unit.py`: Unit parsing and arithmetic
- `quantity.py`: Physical quantity (value + unit) operations
- `unitsystem.py`: Unit system and lookup
- `constants.py`: Common physical constants

## Typical Usage

### Unit Expression Parsing

```python
u = Unit("kg*m^2/(A^2*s^3)")
print(u)
print(u.base_units)
print(u.factor)
```

### Automatic Unit Conversion

```python
q = Quantity(1000, Unit("mm"))
print(q.to("m"))  # 1.0
```

### Unit Compatibility

```python
Unit("m").is_compatible(Unit("mm"))  # True
Unit("m").is_compatible(Unit("s"))   # False
```

## Testing

You can write and run test cases in `test.py` or the `tests/` directory.

## License

MIT License

---

Feel free to submit issues or suggestions!
