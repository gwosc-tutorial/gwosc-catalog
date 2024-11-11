"""
Dataclasses for organizing a catalog of parameter estimation results in
a format compatible with the Gravitational Wave Open Science Center.
"""

import dataclasses
import warnings
import logging
import json
import re
import numpy as np
import pandas as pd
from . import __version__


__all__ = [
    "ParameterValue",
    "Link",
    "SearchResult",
    "ParameterSet",
    "Event",
    "Catalog",
    "validate_schema",
]


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
        Name of the parameter being estimated.

    best: float
        Value for a parameter (often the median value of the
        posterior distribution).

    upper_error: float
        Size of the upper error-bar of the 90% credible region.
        OK to use different uncertainty definition if noted in documentation.

    lower_error: float
        Size of the lower error-bar of the 90% credible region.
        OK to use a different uncertainty definition if noted in documentation.

    is_upper_bound: bool
        True if this value is an upper bound, False otherwise.
        Defaults to False if omitted.
        Setting this to True diplays a less-than sign before the value.

    is_lower_bound: bool
        True if this value is an upper bound, False otherwise.
        Defaults to False if omitted.
        Setting this to True displays a greater-than sign before the value.

    decimal_places: int
        Number of decimal places of the best value to display, must be >= 0.
        Displayed values will be rounded to this number of decimal places.

    unit: str or None
        The physical unit of the best value.
        Set to ``None`` for dimensionless units.
    """

    parameter_name: str
    decimal_places: int
    best: float
    upper_error: float = None
    lower_error: float = None
    is_upper_bound: bool = False
    is_lower_bound: bool = False
    unit: str = None

    def __post_init__(self):
        if self.parameter_name in [
            "chirp_mass_source",
            "chirp_mass",
            "mass_1_source",
            "mass_2_source",
            "total_mass_source",
            "final_mass_source",
        ]:
            mass_units = ["solMass", "M_sun", "Msun"]
            if self.unit not in mass_units:
                raise ValueError(
                    f"{self.parameter_name} parameter needs to have one "
                    f"of {mass_units} string for `unit`."
                )

        if self.parameter_name == "luminosity_distance" and self.unit != "Mpc":
            raise ValueError("luminosity_distance parameter needs to have Mpc `unit`.")

        if self.parameter_name == "far" and self.unit != "1/year":
            raise ValueError("far parameter needs to have '1/year' `unit`.")

        if self.is_upper_bound and self.is_lower_bound:
            raise ValueError("Both `is_upper_bound` and `is_lower_bound` set to True.")

    @classmethod
    def from_series(cls, parameter_name: str, series: pd.Series):
        """Constructor from posterior samples."""
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
    def from_json(cls, search: dict):
        """Constructor from a dict."""
        s = search.copy()
        params = [ParameterValue(**p) for p in s.pop("parameters")]
        return SearchResult(**s, parameters=params)


@dataclasses.dataclass
class ParameterSet:
    """Summary of a single parameter-estimation run.

    Fields
    ------
    pe_set_name: str
        The pipeline name used to generate the parameter estimations.

    data_url: str, url
        This should point to the source data for the analysis of each event.
        It typically points to a posterior sample file if available.

    waveform_family: str
        The waveform approximant used for this parameter set.

    parameters: list of ``ParameterValue``
        Contains entries reporting `mass_1_source`, `chirp_mass`,
        `luminosity_distance`, etc.

    is_preferred: (bool; optional)
        Used to display parameter values on the "Event List" view.
        If omitted, it defaults to False.

    links: list of ``Link`` objects, or None
        Links to external resources.
    """

    pe_set_name: str
    waveform_family: str
    parameters: list[ParameterValue]
    data_url: str = None
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
    def from_json(cls, peset: dict):
        """Constructor from a dict."""
        ps = peset.copy()
        parameters = [ParameterValue(**p) for p in ps.pop("parameters")]
        links = [Link(**u) for u in ps.pop("links", [])]
        return ParameterSet(**ps, parameters=parameters, links=links)


@dataclasses.dataclass
class Event:
    """Parameter estimation runs for a single event.

    Fields
    ------
    event_name: str
        The name of the event using the convention `GWyymmdd_hhmmss`.

    gps: float
        The GPS time of the detection. Geocenter times are preferred.

    event_description: str or None
        Can be used for any user notes for a particular event.
        This appears in a box on the Event Detail View.

    gracedb_id: str or None
        The associated GraceDB superevent ID if any.
        This is an optional key but we recommend adding it whenever possible.

    detectors: list[str]
        A list of detectors for which strain data should be publicly
        released for this event.
        This parameter is not necessary for groups outside the LVK.

    search: ``SearchResult``
        A ``SearchResult`` object.

    pe_sets: ``ParameterSet``
        A ``ParameterSet`` object.
    """

    event_name: str
    gps: float
    search: list[SearchResult]
    gracedb_id: str = None
    pe_sets: list[ParameterSet] = None
    detectors: list[str] = None
    event_description: str = None

    def __post_init__(self):
        # Event name should have format GWYYMMDD_HHMMSS
        if not bool(re.match(r"^GW\d{6}_\d{6}$", self.event_name)):
            raise ValueError("Event name should have format GWYYMMDD_HHMMSS")
        # Detectors validation
        if self.detectors is not None:
            for detector in self.detectors:
                if detector not in ["H1", "L1", "V1", "K1", "G1"]:
                    raise ValueError(f"Unrecognized detector short name: {detector}")
        # Events cannot have empty search list
        if len(self.search) == 0:
            raise ValueError("Search list is empty.")
        # Events can have empty PE sets
        if self.pe_sets is None:
            return
        elif len(self.pe_sets) == 0:
            return
        # If events have PE sets, exactly one should be preferred
        n_preferred = np.count_nonzero([pe_set.is_preferred for pe_set in self.pe_sets])
        if n_preferred != 1:
            raise ValueError(
                f"Exactly one of the `pe_sets` should be preferred, got {n_preferred}."
            )

    @classmethod
    def from_json(cls, event: dict):
        """Constructor from a dict."""
        e = event.copy()
        searches = e.pop("search")
        pe_sets = e.pop("pe_sets", [])
        return Event(
            **e,
            search=[SearchResult.from_json(s) for s in searches],
            # Make a list of ParameterSets only if it's non-empty
            pe_sets=[ParameterSet.from_json(pe_set) for pe_set in pe_sets] or None,
        )


@dataclasses.dataclass
class Catalog:
    """Contains events detected/analyzed by a pipeline.

    Fields
    ------
    schema_version: str
        The version of the schema used. Autopopulated.

    catalog_name: str
        The name of the catalog.

    release_date: str
        The date of the public release of the data in the format YYYY-MM-DD.

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
        if not bool(re.match(r"^\d{4}-\d{2}-\d{2}$", self.release_date)):
            raise ValueError("Catalog release_date not in YYYY-MM-DD format.")
        _, m, d = self.release_date.split("-")
        if int(m) not in range(1, 13) or int(d) not in range(1, 32):
            raise ValueError("Catalog release_date error.")
        if self.schema_version != __version__:
            warnings.warn(
                f"Schema version provided {self.schema_version} is different from current: {__version__}",
                UserWarning,
                stacklevel=1,
            )

    def to_json(self, filename):
        """Write catalog to JSON file."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(dataclasses.asdict(self), file, indent=2)

    @classmethod
    def from_json(cls, catalog):
        c = catalog.copy()
        events = c.pop("events")
        return Catalog(**c, events=[Event.from_json(event) for event in events])


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
            "lower_error": float(f"{-error[0]:.2g}"),
            "upper_error": float(f"{error[1]:.2g}"),
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
        "best": truncated_value,
        "lower_error": err_minus,
        "upper_error": err_plus,
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
    """Parse a JSON filename and validate its contents."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="validateschema",
        description="Validate the upload json schema for a GWOSC community catalog.",
    )
    parser.add_argument("filename", help="Json file to check")
    args = parser.parse_args()
    _set_logger()
    with open(args.filename, encoding="utf-8") as fp:
        newcat = json.load(fp)
    validate_schema(newcat)


if __name__ == "__main__":
    main()
