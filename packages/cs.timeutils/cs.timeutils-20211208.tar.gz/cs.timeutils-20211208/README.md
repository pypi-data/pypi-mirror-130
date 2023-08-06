Convenience routines for timing.

*Latest release 20211208*:
Move the TimeoutError definiton to cs.gimmicks.

## Function `ISOtime(gmtime)`

Produce an ISO8601 timestamp string from a UNIX time.

## Function `sleep(delay)`

time.sleep() sometimes sleeps significantly less that requested.
This function calls time.sleep() until at least `delay` seconds have
elapsed, trying to be precise.

## Function `time_from_ISO(isodate, islocaltime=False)`

Parse an ISO8601 date string and return seconds since the epoch.
If islocaltime is true convert using localtime(tm) otherwise use
gmtime(tm).

## Function `time_func(func, *args, **kw)`

Run the supplied function and arguments.
Return a the elapsed time in seconds and the function's own return value.

## Function `tm_from_ISO(isodate)`

Parse an ISO8601 date string and return a struct_time.

# Release Log



*Release 20211208*:
Move the TimeoutError definiton to cs.gimmicks.

*Release 20190220*:
Backport for older Pythons.

*Release 20190101*:
Define TimeoutError only if missing.

*Release 20170608*:
Trivial changes, nothing semantic.

*Release 20150116*:
PyPI initial prep.
