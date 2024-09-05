import pytest
from ccverify import validate_schema, ParameterValue, Event

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
    "Example catalog should pass."
    e = event_example.copy()
    s = search_example.copy()
    s["parameters"] = [far_example, snr_example, pastro_example]
    e["search"] = [s]
    ps = pe_set_example.copy()
    ps["parameters"] = [pe_mass1_example, pe_distance_example]
    ps["links"] = [link_example]
    e["pe_sets"] = [ps]
    c = catalog_example.copy()
    c["events"] = [e]
    validate_schema(c)


def test_empty_events():
    "Catalog with no events should fail."
    with pytest.raises(ValueError):
        validate_schema(catalog_example)


def test_empty_pe_sets():
    "Event with no pe_sets should pass."
    e = event_example.copy()
    s = search_example.copy()
    s["parameters"] = [far_example, snr_example, pastro_example]
    e["search"] = [s]
    e["pe_sets"] = []
    c = catalog_example.copy()
    c["events"] = [e]
    validate_schema(c)


def test_empty_search():
    "Catalog with an empty search should fail."
    e = event_example.copy()
    e["search"] = []
    ps = pe_set_example.copy()
    ps["parameters"] = [pe_mass1_example, pe_distance_example]
    ps["links"] = [link_example]
    e["pe_sets"] = [ps]
    c = catalog_example.copy()
    c["events"] = [e]
    with pytest.raises(ValueError):
        validate_schema(c)


def test_empty_links():
    "Catalog with empty links should pass."
    e = event_example.copy()
    s = search_example.copy()
    s["parameters"] = [far_example, snr_example, pastro_example]
    e["search"] = [s]
    ps = pe_set_example.copy()
    ps["parameters"] = [pe_mass1_example, pe_distance_example]
    ps["links"] = []
    e["pe_sets"] = [ps]
    c = catalog_example.copy()
    c["events"] = [e]
    validate_schema(c)


def test_missing_links():
    "Catalog with missing links should pass."
    e = event_example.copy()
    s = search_example.copy()
    s["parameters"] = [far_example, snr_example, pastro_example]
    e["search"] = [s]
    ps = pe_set_example.copy()
    ps["parameters"] = [pe_mass1_example, pe_distance_example]
    ps.pop("links", None)
    e["pe_sets"] = [ps]
    c = catalog_example.copy()
    c["events"] = [e]
    validate_schema(c)


def test_event_name_format():
    "Unrecognized event name format."
    e = event_example.copy()
    s = search_example.copy()
    s["parameters"] = [far_example, snr_example, pastro_example]
    e["search"] = [s]
    ps = pe_set_example.copy()
    ps["parameters"] = [pe_mass1_example, pe_distance_example]
    ps["links"] = [link_example]
    e["pe_sets"] = [ps]
    c = catalog_example.copy()
    c["events"] = [e]
    e["event_name"] = "S123483"
    with pytest.raises(ValueError):
        validate_schema(c)


def test_catalog_release_date_format():
    "Unrecognized catalog release_date format."
    e = event_example.copy()
    s = search_example.copy()
    s["parameters"] = [far_example, snr_example, pastro_example]
    e["search"] = [s]
    ps = pe_set_example.copy()
    ps["parameters"] = [pe_mass1_example, pe_distance_example]
    ps["links"] = [link_example]
    e["pe_sets"] = [ps]
    c = catalog_example.copy()
    c["events"] = [e]
    c["release_date"] = "2024-01-01T00:00:00"
    with pytest.raises(ValueError):
        validate_schema(c)


def test_event_detector_names():
    "Unrecognized event detector."
    e = event_example.copy()
    s = search_example.copy()
    s["parameters"] = [far_example, snr_example, pastro_example]
    e["search"] = [s]
    ps = pe_set_example.copy()
    ps["parameters"] = [pe_mass1_example, pe_distance_example]
    ps["links"] = [link_example]
    e["pe_sets"] = [ps]
    c = catalog_example.copy()
    c["events"] = [e]
    e["detectors"] = ["HANFORD"]
    with pytest.raises(ValueError):
        validate_schema(c)


def test_mass_unit():
    "Mass unit should be solar mass."
    with pytest.raises(ValueError):
        unit = pe_mass1_example.pop("unit")
        ParameterValue(**pe_mass1_example)
    pe_mass1_example["unit"] = unit
    ParameterValue(**pe_mass1_example)


def test_distance_unit():
    "Distance unit should be Mpc."
    with pytest.raises(ValueError):
        unit = pe_distance_example.pop("unit")
        ParameterValue(**pe_distance_example)
    pe_distance_example["unit"] = unit
    ParameterValue(**pe_distance_example)


def test_far_unit():
    "FAR unit should be '1/year'."
    with pytest.raises(ValueError):
        unit = far_example.pop("unit")
        ParameterValue(**far_example)
    far_example["unit"] = unit
    ParameterValue(**far_example)


def test_unique_pe_set():
    "Exactly one PE set should be preferred."
    pe_sets = []
    for i in range(3):
        ps = pe_set_example.copy()
        ps["pe_set_name"] = f"Pipeline {i + 1}"
        ps.pop("is_preferred")
        ps["parameters"] = [pe_mass1_example.copy(), pe_distance_example.copy()]
        pe_sets.append(ps)
    e = event_example.copy()
    e["search"] = [search_example.copy()]
    e["search"][0]["parameters"] = [far_example.copy()]
    e["pe_sets"] = pe_sets
    with pytest.raises(ValueError):
        Event.from_json(e)
    e["pe_sets"][1]["is_preferred"] = True
    Event.from_json(e)
    e["pe_sets"][2]["is_preferred"] = True
    with pytest.raises(ValueError):
        Event.from_json(e)
