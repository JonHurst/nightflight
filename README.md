# nightflight

This is a very small library that leverages the astral package to calculate how
much of a flight occurs during regulatory night time (30 minutes before sunset to
30 minutes after sunrise).

This calculation is somewhat complicated because sunset and sunrise are a
function of location, and location is changing rapidly during a flight.

Positions and times during the flight are approximated by assuming that the
flight follows a great circle track between origin and destination and that
velocity is constant throughout.

The latter assumption is likely the greatest source of error, since average
velocity along the great circle track will be much lower during the initial and
terminal manoeuvring phases.

The assumption of great circle track may also be erroneous on very long
trips. If a trip starts on exactly opposite sides of the planet, there are an
infinite number of equally efficient tracks to choose from, so when the
situation is close to this, the actual track flown may end up being radically
different from that assumed.

The main function takes n_vectors (vectors normal to the tangent plane at a
given location) as arguments to avoid dealing with singularities. A database of
n_vectors for airfields as designated by their three letter IATA code is
included. This data is a processed version of the database generously provided
by openflights.org (see <https://openflights.org/data.html>). The `make_locations`
module has a `to_nvec` function to convert an arbitrary latitude and longitude
to an n_vector .
