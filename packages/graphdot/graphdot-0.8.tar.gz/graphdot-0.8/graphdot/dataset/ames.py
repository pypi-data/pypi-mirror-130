#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from ._get import get


def AMES(overwrite=False):
    '''Ames bacteria mutagenicity test data from multiple sources.
    Data source: 10.1021/ci300400a, around 8000 molecules, SMILES format.
    '''
    return get(
        'https://ndownloader.figshare.com/files/4108681',
        'ci300400a_si_001.xls',
        overwrite=overwrite,
        parser=lambda f: pd.read_excel(f, sheet_name=None, header=1)
    )
