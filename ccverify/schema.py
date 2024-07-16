"""
Dataclasses for organizing a catalog of parameter estimation results in
a format compatible with the Gravitational Wave Open Science Center.
"""
import dataclasses
import json
import numpy as np
import pandas as pd
from . import __version__


UNITS = dict.fromkeys(
    (
        "chirp_mass_source",
        "chirp_mass",
        "mass_1_source",
        "mass_2_source",
        "total_mass_source",
    ),
    "Msun",
) | {"luminosity_distance": "Mpc", "far": "1/year"}


@dataclasses.dataclass
class ParameterValue:
    """
    Summary of the measurement of a single parameter.

    Fields
    ------
    parameter_name: str
        Parameter name.

    median: float
        Median.

    upper_95: float
        95th percentile minus median.

    lower_05: float
        5th percentile minus median.

    is_upper_bound, is_lower_bound: bool

    decimal_places: int
        Number of places after the decimal point to display.

    unit: str or None
    """
    parameter_name: str
    decimal_places: int
    median: float
    upper_95: float = None
    lower_05: float = None
    is_upper_bound: bool = False
    is_lower_bound: bool = False
    unit: str = None

    @classmethod
    def from_series(cls, parameter_name: str, series: pd.Series):
        q05, median, q95 = series.quantile((0.05, 0.5, 0.95))
        error = median - q05, q95 - median
        kwargs = _condition_value_and_error(median, error)
        return cls(parameter_name=parameter_name,
                   unit=UNITS.get(parameter_name), **kwargs)


@dataclasses.dataclass
class Link:
    url: str
    content_type: str
    description: str


@dataclasses.dataclass
class SearchResult:
    """
    Summary of the significance of an event obtained by a search
    pipeline.

    Fields
    ------
    pipeline_name: str
        Name of the search pipeline.

    search_statistics: list of ``ParameterValue``
        Contains entries reporting `pastro`, `far`, `network_snr`, etc.
    """
    pipeline_name: str
    search_statistics: list[ParameterValue]


@dataclasses.dataclass
class ParameterSet:
    """Summary of a single parameter-estimation run."""
    pe_set_name: str
    data_url: str
    waveform_family: str
    parameters: list[ParameterValue]
    links: list[Link] = None

    @classmethod
    def from_samples(cls,
                     samples: pd.DataFrame,
                     pe_set_name,
                     data_url,
                     waveform_family,
                     links=None):
        """
        Constructor from a ``pandas.DataFrame`` of posterior samples.
        """
        parameters = [ParameterValue.from_series(*item)
                      for item in samples.items()]
        return cls(pe_set_name=pe_set_name,
                   data_url=data_url,
                   waveform_family=waveform_family,
                   parameters=parameters,
                   links=links,
                  )


@dataclasses.dataclass
class Event:
    """Parameter estimation runs for a single event."""
    event_name: str
    gps: float
    detectors: list[str]
    search: list[SearchResult]
    pe_sets: list[ParameterSet]
    event_description: str = ""


@dataclasses.dataclass
class Catalog:
    """Contains events detected/analyzed by a pipeline.

    Fields
    ------
    version: str
        The schema version.

    catalog_name: str
        The name of the catalog.

    release_date: str
        Release date of the catalog in YYYY-MM-DD format.

    catalog_description: str
        A description of the catalog.

    doi: str
        The full URL to the publication DOI related to this catalog.

    events: list of ``Event``
    """
    catalog_name: str
    release_date: str
    catalog_description: str
    doi: str
    events: list[Event]
    schema_version: str = __version__

    def to_json(self, filename):
        """Write catalog to JSON file."""
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(dataclasses.asdict(self), file, indent=2)


def _condition_value_and_error(value, error) -> dict:
    """
    Pass a value and its uncertainty, return a dictionary with
    value, error and significant figures given by the uncertainties.

    Parameters
    ----------
    value: float
    error: (err_minus, err_plus)
    """
    error = np.abs(error)
    min_error = np.min(error)

    if min_error == 0:
        return {'median': float(f'{value:.2g}'),
                'lower_05': float(f'{-error[0]:.2g}'),
                'upper_95': float(f'{error[1]:.2g}'),
                'decimal_places': max(0, _first_decimal_place(value) + 1)}

    decimal_places = _first_decimal_place(min_error)
    if f'{min_error:e}'.startswith('1'):
        decimal_places += 1

    def truncate(val):
        rounded = round(val, decimal_places)
        if decimal_places > 0:
            return rounded
        return int(rounded)

    truncated_value = truncate(value)
    err_minus = truncate(value - error[0] - truncated_value)
    err_plus = truncate(value + error[1] - truncated_value)
    return {'median': truncated_value,
            'lower_05': err_minus,
            'upper_95': err_plus,
            'decimal_places': max(0, decimal_places)}


def _first_decimal_place(value) -> int:
    return int(np.ceil(-np.log10(np.abs(value))))
