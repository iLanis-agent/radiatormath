# Radiator math

Radiator math sizes the radiator before the shopping trip: the room's
dimensions become the watts it asks for on a labeled scale, the catalog
rating gets corrected for the water temperature your system actually runs,
and the needed watts become a section count with headroom.

Live site: https://ilanis-agent.github.io/radiatormath/

## The three tools

- **Room plan** - `length x width x height x labeled factor` (W per m3),
  rounded, becomes the watts; BTU at a labeled 3.412 per watt. Size verdicts
  run small panel / standard panel / large or two panels / several radiators.
- **Delta plan** - mean water minus room is the delta-T; a labeled
  correction table (50 C: 1.0, 40 C: 0.75, 30 C: 0.51, 20 C: 0.30, below:
  0.12) turns the catalog rating into honest output.
- **Section plan** - `ceil(needed / per-section)` sections, the total they
  give and the headroom they leave; over 16 sections reads as a long column.

## Limits

Every norm is labeled and illustrative. Real heat loss moves with windows,
walls and weather. This is arithmetic, not a design: a heating engineer
sizes the real system, and the manufacturer rates the real hardware.

## Files

- `index.html` - landing page with the labeled norms
- `app.html` - the three calculators
- `engine.js` - shared calculation and render logic (browser + node)
- `oracle.py` - python mirror of the engine, writes `expected.json`
- `test.js` - runs the engine against `expected.json` (18 cases, 111 checks)

Run the tests: `python3 oracle.py && node test.js`
