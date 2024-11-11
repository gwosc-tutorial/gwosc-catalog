from ccverify import validate_schema, __version__ as schema_version
from deepdiff.diff import DeepDiff

example_catalog = {
    "schema_version": schema_version,
    "catalog_name": "string",
    "catalog_description": "string",
    "doi": "https://doi.org/12345/",
    "events": [
        {
            "event_name": "GW241230_010000",
            "gps": 1234567890.1,
            "event_description": "string or null",
            "detectors": ["H1", "L1"],
            "search": [
                {
                    "pipeline_name": "string",
                    "parameters": [
                        {
                            "parameter_name": "far",
                            "best": 0.00001,
                            "is_upper_bound": True,
                            "decimal_places": 5,
                            "unit": "1/year",
                        },
                        {
                            "parameter_name": "pastro",
                            "best": 0.99,
                            "is_lower_bound": True,
                            "decimal_places": 2,
                        },
                    ],
                }
            ],
            "pe_sets": [],
        },
        {
            "event_name": "GW241231_010000",
            "gps": 1234567891.1,
            "event_description": "string or null",
            "detectors": ["H1", "L1"],
            "search": [
                {
                    "pipeline_name": "string",
                    "parameters": [
                        {
                            "parameter_name": "far",
                            "best": 0.00001,
                            "is_upper_bound": True,
                            "decimal_places": 5,
                            "unit": "1/year",
                        },
                        {
                            "parameter_name": "pastro",
                            "best": 0.99,
                            "is_lower_bound": True,
                            "decimal_places": 2,
                        },
                    ],
                }
            ],
            "pe_sets": [
                {
                    "pe_set_name": "string",
                    "waveform_family": "IMRPhenomPv3HM",
                    "data_url": "https://zenodo.org/",
                    "parameters": [
                        {
                            "parameter_name": "mass_1_source",
                            "best": 3.34,
                            "upper_error": 0.01,
                            "lower_error": 0.01,
                            "is_upper_bound": False,
                            "is_lower_bound": False,
                            "decimal_places": 2,
                            "unit": "M_sun",
                        }
                    ],
                    "links": [],
                    "is_preferred": True,
                }
            ],
        },
    ],
    "release_date": "2024-02-04",
}


def test_validation_idempotent():
    "Test that validation does not modify its input."
    catalog_before = example_catalog
    validate_schema(example_catalog)
    validate_schema(example_catalog)
    ddiff = DeepDiff(catalog_before, example_catalog, ignore_order=True)
    assert ddiff == {}
