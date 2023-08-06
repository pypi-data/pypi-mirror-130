# SecrLib

SecrLib is a python library.

To install :
pip install SecrLib

To import :
example (
    from Secr import logs
)

## Logging :

log(fname, content)
// Logs something to a file
logcopy(fname, ffname)
// copys a file to another file
logcopyremove(fname, ffname)
// Copys a log to a file, then deletes the first file
logmake(fname)
// makes a file
logdelete(fname)
// deletes a file

## Math :
slope(x2, y2, x1, y2)
// calculates the slope of a set of coordinates