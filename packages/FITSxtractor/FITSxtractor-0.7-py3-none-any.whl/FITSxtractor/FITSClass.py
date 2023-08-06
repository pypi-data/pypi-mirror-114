#!/usr/bin/env python3
"""
This class will be used as a dataclass for the XML metadata from FITS output files.
In order for it to do so, one can add or remove certain objects.

@Author: ovanov
@date:   06.07.21
"""

from dataclasses import asdict, dataclass, field

@dataclass(order=True)
class FITS_obj:
    """
    This Class uses defautlt values of "None" strings instead of bools in order for them to be shown in 
    the python dataframes as "None" and not empty cells (which can cause sorting problems). The list values
    are used to store multiple values, if there are more than one in a file.
    The dataclass attributes represent the values in each XML structured FITS output file. The order, in which
    they are placed, resembles the columns which will be printed into a file.
    """

    filepath: str = "None"
    size: str = "None"
    md5checksum: str = "None"
    status: str = "None"
    identity_format: list = field(default_factory=list)
    mimetype: list = field(default_factory=list)
    puid: str = field(default_factory=list)
    well_formed: str = "None"
    well_formed_stat: str = "None"