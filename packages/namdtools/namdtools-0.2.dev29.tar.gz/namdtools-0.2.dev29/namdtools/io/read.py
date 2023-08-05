"""
read.py
language: Python3
author: C. Lockhart <chrisblockhart@gmail.com>
"""

from namdtools.core import Log


# Read output from NAMD run
# Convert to object? Store raw output?
def read_log(fname, glob=False):
    """
    Read output from NAMD.

    Parameters
    ----------
    fname : str
        Name of NAMD output file.
    glob : bool
        Allow for glob read.

    Returns
    -------
    pandas.DataFrame
        Data from NAMD output.
    """

    # Import to save time
    import pandas as pd
    if glob:
        from glob import glob as glob_
        fnames = sorted(glob_(fname))
    else:
        fnames = [fname]

    # Read all files
    df = None
    for fname in fnames:
        data = _read_log(fname)
        if df is None:
            df = data
        else:
            df = pd.concat([df, data], ignore_index=True)

    # Return
    return Log(df)


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
