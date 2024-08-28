"""
Dataclasses for organizing a catalog of parameter estimation results in
a format compatible with the Gravitational Wave Open Science Center.
"""
import dataclasses
import logging
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
    Summary of the measurement of a single parameter estimation.

    Fields
    ------
    parameter_name: str
        Parameter name.

    median: float
        Median value.

    upper_95: float
        95th percentile minus median.

    lower_05: float
        5th percentile minus median.

    is_upper_bound, is_lower_bound: bool
        True if this value is an upper or lower bound, False otherwise.

    decimal_places: int
        Number of places after the decimal point to display.

    unit: str or None
        The physical unit of the parameter. Set to ``None`` for dimensionless units.
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
        return cls(
            parameter_name=parameter_name, unit=UNITS.get(parameter_name), **kwargs
        )


@dataclasses.dataclass
class Link:
    """
    Links to external resources like skymaps or other documents.

    Fields
    ------
    url: str
        URL to external resource.

    content_type: str
        The type of the resource: "skymap", "documentation", etc.

    description: str
        A brief description of the resource.

    For a link to posterior samples, use ``ParameterSet.data_url`` instead.
    """

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

    parameters: list of ``ParameterValue``
        Contains entries reporting `pastro`, `far`, `snr`, etc.
    """

    pipeline_name: str
    parameters: list[ParameterValue]

    @classmethod
    def from_json(cls, search):
        parameters = [ParameterValue(**p) for p in search.pop("parameters")]
        return SearchResult(**search, parameters=parameters)


@dataclasses.dataclass
class ParameterSet:
    """Summary of a single parameter-estimation run.

    Fields
    ------
    pe_set_name: str
        Name of the parameter-estimation pipeline.

    data_url: str, url
        The full URL to the file that stores posterior samples.

    waveform_family: str
        The name of the waveform family used for the estimation.

    parameters: list of ``ParameterValue``
        Contains entries reporting `mass_1_source`, `chirp_mass`, `luminosity_distance`, etc.

    links: list of ``Link`` objects, or None
        Links to external resources.
    """

    pe_set_name: str
    data_url: str
    waveform_family: str
    parameters: list[ParameterValue]
    is_preferred: bool = False
    links: list[Link] = None

    @classmethod
    def from_samples(
        cls,
        samples: pd.DataFrame,
        pe_set_name,
        data_url,
        waveform_family,
        is_preferred,
        links=None,
    ):
        """
        Constructor from a ``pandas.DataFrame`` of posterior samples.
        """
        parameters = [ParameterValue.from_series(*item) for item in samples.items()]
        return cls(
            pe_set_name=pe_set_name,
            data_url=data_url,
            waveform_family=waveform_family,
            parameters=parameters,
            links=links,
            is_preferred=is_preferred,
        )

    @classmethod
    def from_json(cls, peset):
        parameters = [ParameterValue(**p) for p in peset.pop("parameters")]
        links = [Link(**u) for u in peset.pop("links", [])]
        return ParameterSet(**peset, parameters=parameters, links=links)


@dataclasses.dataclass
class Event:
    """Parameter estimation runs for a single event.

    Fields
    ------
    event_name: str
        The name of the event using the convention `GWyymmdd_hhmmss`.

    gps: float
        The GPS time of the detection.

    event_description: str
        A short description of this event.

    detectors: list[str]
        A list of detector data used for this event.

    search: ``SearchResult``
        A ``SearchResult`` object.

    pe_sets: ``ParameterSet``
        A ``ParameterSet`` object.
    """

    event_name: str
    gps: float
    detectors: list[str]
    search: list[SearchResult]
    pe_sets: list[ParameterSet]
    event_description: str = ""

    def __post_init__(self):
        # Events cannot have empty search list
        if len(self.search) == 0:
            raise ValueError("Search list is empty.")
        # Events can have empty PE sets
        if len(self.pe_sets) == 0:
            return
        # If events have PE sets, exactly one should be preferred
        n_preferred = np.count_nonzero([pe_set.is_preferred for pe_set in self.pe_sets])
        if n_preferred != 1:
            raise ValueError(
                f"Exactly one of the `pe_sets` should be preferred, got {n_preferred}."
            )

    @classmethod
    def from_json(cls, event):
        searches = event.pop("search")
        pe_sets = event.pop("pe_sets")
        return Event(
            **event,
            search=[SearchResult.from_json(s) for s in searches],
            pe_sets=[ParameterSet.from_json(pe_set) for pe_set in pe_sets],
        )


@dataclasses.dataclass
class Catalog:
    """Contains events detected/analyzed by a pipeline.

    Fields
    ------
    schema_version: str
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

    def __post_init__(self):
        if len(self.events) == 0:
            raise ValueError("Event list is empty.")

    def to_json(self, filename):
        """Write catalog to JSON file."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(dataclasses.asdict(self), file, indent=2)

    @classmethod
    def from_json(cls, catalog):
        events = catalog.pop("events")
        return Catalog(**catalog, events=[Event.from_json(event) for event in events])


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
        return {
            "median": float(f"{value:.2g}"),
            "lower_05": float(f"{-error[0]:.2g}"),
            "upper_95": float(f"{error[1]:.2g}"),
            "decimal_places": max(0, _first_decimal_place(value) + 1),
        }

    decimal_places = _first_decimal_place(min_error)
    if f"{min_error:e}".startswith("1"):
        decimal_places += 1

    def truncate(val):
        rounded = round(val, decimal_places)
        if decimal_places > 0:
            return rounded
        return int(rounded)

    truncated_value = truncate(value)
    err_minus = truncate(value - error[0] - truncated_value)
    err_plus = truncate(value + error[1] - truncated_value)
    return {
        "median": truncated_value,
        "lower_05": err_minus,
        "upper_95": err_plus,
        "decimal_places": max(0, decimal_places),
    }


def _first_decimal_place(value) -> int:
    return int(np.ceil(-np.log10(np.abs(value))))


def _set_logger():
    import sys

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def validate_schema(upload_json):
    """Return True if catalog passes validation."""
    Catalog.from_json(upload_json)
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="validateschema",
        description="Validate the upload json schema for a GWOSC community catalog.",
    )
    parser.add_argument("filename", help="Json file to check")
    args = parser.parse_args()
    _set_logger()
    with open(args.filename) as fp:
        newcat = json.load(fp)
    validate_schema(newcat)


if __name__ == "__main__":
    main()
