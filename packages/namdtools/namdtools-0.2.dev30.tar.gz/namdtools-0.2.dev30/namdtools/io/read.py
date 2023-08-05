"""
read.py
language: Python3
author: C. Lockhart <chrisblockhart@gmail.com>
"""

from namdtools.core import Log


# Read output from NAMD run
# Convert to object? Store raw output?
def read_log(fname, glob=None):
    """
    Read output from NAMD.

    Parameters
    ----------
    fname : str
        Name of NAMD output file.
    glob : bool or dict
        Does `fname` need to be globbed? If a boolean, uses :ref:`glob`. If dictionary, uses :ref:`vglob`.
        (Default: None)

    Returns
    -------
    Log
    """

    # Import to save time
    import pandas as pd

    # If glob, change fname to include all globbed files
    if glob:
        from molecular.io.utilities import Path, vglob  #

        # Convert glob to a empty dictionary if necessary
        if not isinstance(glob, dict):
            glob = {}

        # Glob first; if glob is empty, throw an error
        fname_glob = vglob(fname, errors='raise', **glob)
        if not fname_glob:
            raise FileNotFoundError(fname)

        # Sort glob
        # fnames = sorted(fname_glob)
        fnames = fname_glob
    else:
        fnames = [fname]

    # Cycle over fnames and read in
    # df = None
    # for fname in fnames:
    #     data = _read_log(fname)
    #     if df is None:
    #         df = data
    #     else:
    #         df = pd.concat([df, data], ignore_index=True)
    data = list(map(_read_log, fnames))
    if glob:
        data = [table.assign(**Path(fname).metadata) for fname, table in zip(fnames, data)]

    # Concatenate
    data = data[0] if len(data) == 1 else pd.concat(data, ignore_index=ignore_index)

    # Return
    return Log(data)


def _read_log(fname):
    """


    Parameters
    ----------
    fname : str
        Name of NAMD output file.

    Returns
    -------

    """

    # Import pandas if not already loaded (to speed up namdtools in general)
    import pandas as pd

    # Initialize DataFrame information
    columns = None
    records = []

    # Read through log file and extract energy records
    # TODO read in with regex
    with open(fname, 'r') as stream:
        for line in stream.readlines():
            # Read first ETITLE
            if columns is None and line[:6] == 'ETITLE':
                columns = line.lower().split()[1:]

            # Save each energy record
            if line[:6] == 'ENERGY':
                records.append(line.split()[1:])

    # What if our file doesn't contain ETITLE? Should this return an error, or can we assume the columns?
    columns = ['ts', 'bond', 'angle', 'dihed', 'imprp', 'elect', 'vdw', 'boundary', 'misc', 'kinetic', 'total',
               'temp', 'potential', 'total3', 'tempavg', 'pressure', 'gpressure', 'volume', 'pressavg', 'gpressavg']

    # Return DataFrame
    return pd.DataFrame(records, columns=columns).set_index(columns[0]).astype(float)
