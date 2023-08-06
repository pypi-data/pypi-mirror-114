#!/usr/bin/env python3# (C) Copyright 2021 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#
from __future__ import annotations

import climetlab as cml
import pandas as pd
import xarray as xr
from climetlab import Dataset
from climetlab.normalize import DateListNormaliser

__version__ = "0.1.0"

URL = "https://storage.ecmwf.europeanweather.cloud"

PATTERN = "{url}/NOGWD_L91_PUBLIC/nc/{date}.nc"


class nogwd(Dataset):
    name = "NOGWD 91 level dataset"
    home_page = "https://git.ecmwf.int/projects/MLFET/repos/maelstrom-nogwd"
    licence = "CC BY 4.0, see https://apps.ecmwf.int/datasets/licences/general/ "
    documentation = (
        "Contains the input/output dataset for learning non-orographic gravity wave \n"
        "drag, as described in https://arxiv.org/abs/2101.08195 \n"
        "Data is grouped by forecast start date. \n"
        "Data has been preprocessed into inputs 'x' and outputs 'y'. \n"
        "'x' contains vertical profiles of winds & temperature plus surface values \n"
        "of pressure and geopotential. \n"
        "'y' contains the the wind increments due to parametrised non-orographic \n"
        "gravity wave drag. The machine learning task is to predict y given x. \n"
        "Unlike many ML tasks within the field of weather and climate, this task \n"
        "can be predicted independently for each column of atmosphere. \n"
        "Data can be accessed either by forecast start-date or dataset type. \n"
        "With neither argument provided, the first file is loaded, corresponding \n"
        "to 2015-01-01 (the 'tier-1' dataset). Incorrect dates will be flagged. \n"
        "Other dataset types are 'training', 'validation' & 'testing' corresponding \n"
        "to the date groups outlined in https://arxiv.org/abs/2101.08195"
    )
    citation = (
        "Chantry, Matthew, et al. 'Machine learning emulation of gravity wave drag in "
        "numerical weather forecasting.' Journal of Advances in Modeling Earth Systems "
        "(2020): e2021MS002477."
    )
    terms_of_use = (
        "By downloading data from this dataset, you agree to the terms and conditions defined at "
        "https://apps.ecmwf.int/datasets/licences/general/ "
        "If you do not agree with such terms, do not download the data. "
    )
    subset_dates = {
        "tier-1": "2015-01-01",
        "training": [
            i.strftime("%Y-%m-%d")
            for i in pd.date_range(start="2015-01-01", end="2015-12-01", freq="30D")
        ],
        "validation": ["2016-02-25", "2016-06-24", "2016-12-21"],
        "testing": ["2017-02-19", "2017-07-19", "2017-11-16"],
    }
    all_datelist = [
        "2015-01-01",
        "2015-01-31",
        "2015-03-02",
        "2015-04-01",
        "2015-05-01",
        "2015-05-31",
        "2015-06-30",
        "2015-07-30",
        "2015-08-29",
        "2015-09-28",
        "2015-10-28",
        "2015-11-27",
        "2016-02-25",
        "2016-06-24",
        "2016-12-21",
        "2017-02-19",
        "2017-07-19",
        "2017-11-16",
    ]
    default_datelist = "2015-01-01"

    def __init__(self, date=None, subset=None):
        if subset is None:
            if date is None:
                print("No subset or date provided, using 'tier-1/2015-01-01'")
                date = "2015-01-01"
            self.date = self.parse_date(date)
        else:
            if subset not in self.subset_dates.keys():
                raise ValueError(f"{subset} is not in {self.subset_dates.keys()}")
            self.date = self.parse_date(self.subset_dates[subset])

        request = dict(url=URL, date=self.date)
        self.source = cml.load_source("url-pattern", PATTERN, request, merger=Merger())

    def parse_date(self, date):
        if date is None:
            date = self.default_datelist
        date = DateListNormaliser("%Y-%m-%d")(date)
        for d in date:
            if d not in self.all_datelist:
                raise ValueError(
                    f"{d} is not in the available list of dates {self.all_datelist}"
                )
        return date


class Merger:
    def __init__(self, engine="netcdf4", concat_dim="examples", options=None):
        self.engine = engine
        self.concat_dim = concat_dim
        self.options = options if options is not None else {}

    def to_xarray(self, paths, **kwargs):
        return xr.open_mfdataset(
            paths,
            engine=self.engine,
            concat_dim=self.concat_dim,
            combine="nested",
            **self.options,
        )
