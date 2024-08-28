from ccverify import validate_schema
import pytest

catalog_example = {
    "schema_version": "1.0",
    "catalog_name": "string",
    "catalog_description": "string",
    "doi": "https://doi.org/12345/",
    "events": [],
    "release_date": "2024-02-04",
}

event_example = {
    "event_name": "GW241230_010000",
    "gps": 1234567890.1,
    "event_description": "string or null",
    "detectors": ["H1", "L1"],
    "search": [],
    "pe_sets": [],
}

search_example = {
    "pipeline_name": "string",
    "parameters": [],
}

far_example = {
    "parameter_name": "far",
    "median": 0.00001,
    "is_upper_bound": True,
    "decimal_places": 5,
    "unit": "1/year",
}

pastro_example = {
    "parameter_name": "pastro",
    "median": 0.99,
    "is_lower_bound": True,
    "decimal_places": 2,
}

snr_example = {
    "parameter_name": "snr",
    "median": 9.34,
    "upper_95": 0.01,
    "lower_05": 0.01,
    "decimal_places": 2,
}

pe_set_example = {
    "pe_set_name": "string",
    "waveform_family": "IMRPhenomPv3HM",
    "data_url": "https://zenodo.org/",
    "parameters": [],
    "links": [],
    "is_preferred": True,
}

pe_mass1_example = {
    "parameter_name": "mass_1_source",
    "median": 3.34,
    "upper_95": 0.01,
    "lower_05": 0.01,
    "is_upper_bound": False,
    "is_lower_bound": False,
    "decimal_places": 2,
    "unit": "M_sun",
}

pe_distance_example = {
    "parameter_name": "luminosity_distance",
    "median": 130,
    "upper_95": 5,
    "lower_05": 2,
    "is_upper_bound": False,
    "is_lower_bound": False,
    "decimal_places": 0,
    "unit": "Mpc",
}


link_example = {
    "url": "https://example.com",
    "content_type": "posterior_samples",
    "description": "string",
}


def test_valid_full_schema():
    s = search_example.copy()
    s["parameters"].extend([far_example, snr_example, pastro_example])
    ps = pe_set_example.copy()
    ps["parameters"].extend([pe_mass1_example, pe_distance_example])
    ps["links"].append(link_example)
    e = event_example.copy()
    e["search"].append(s)
    e["pe_sets"].append(ps)
    c = catalog_example.copy()
    c["events"].append(e)
    validate_schema(c)


def test_global_keys():
    bad_keys = {"a": 1, "b": 2}
    with pytest.raises((KeyError, ValueError)):
        validate_schema(bad_keys)
