# Civilization Simulator

A dependency-free Python base project that generates a fictional civilization's
history over 1,000 years. It advances one year at a time and prints a detailed
report for each century.

## Run

Requires Python 3.9 or newer:

```sh
python3 simulator.py
python3 simulator.py --seed 42
```

The same seed always produces the same history. Redirect output to a file to
save it, for example: `python3 simulator.py --seed 42 > history.txt`.

Each report includes the government, cities and their populations, local wealth
and religions, known technologies, discoveries and wars during that century,
and a chronological record of events and decade-by-decade censuses. Wealth is
an abstract accumulated economic measure, not a currency. Wars are simplified
single-year events between cities, rather than a model of ongoing conflicts.

## Tests

```sh
python3 -m unittest
```
