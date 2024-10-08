# JSON Schema

## Example

An example of the schema can be found below and the description of the keys after the example.

```json
{
  "schema_version": "1.0",
  "catalog_name": "string",
  "catalog_description": "string",
  "doi": "https://doi.org/12345/",
  "release_date": "YYYY-MM-DD",
  "events": [
    {
      "event_name": "GWYYMMDD_HHMMSS",
      "gps": 1234567890.1,
      "event_description": "string or null",
      "detectors": ["H1", "L1"],
      "search": [
        {
          "pipeline_name": "string",
          "parameters": [
            {
              "parameter_name": "far",
              "median": 0.00001,
              "is_upper_bound": true,
              "decimal_places": 5,
              "unit": "1/year"
            },
            {
              "parameter_name": "pastro",
              "median": 0.99,
              "is_lower_bound": true,
              "decimal_places": 2
            },
            {
              "parameter_name": "snr",
              "median": 9.34,
              "upper_95": 0.01,
              "lower_05": 0.01,
              "decimal_places": 2
            }
          ]
        }
      ],
      "pe_sets": [
        {
          "pe_set_name": "string",
          "waveform_family": "IMRPhenomPv3HM",
          "data_url": "https://zenodo.org/",
          "is_preferred": true,
          "parameters": [
            {
              "parameter_name": "mass_1_source",
              "median": 3.34,
              "upper_95": 0.01,
              "lower_05": 0.01,
              "is_upper_bound": false,
              "is_lower_bound": false,
              "decimal_places": 2,
              "unit": "M_sun"
            },
            {
              "parameter_name": "luminosity_distance",
              "median": 130,
              "upper_95": 5,
              "lower_05": 2,
              "is_upper_bound": false,
              "is_lower_bound": false,
              "decimal_places": 0,
              "unit": "Mpc"
            }
          ],
          "links": [
            {
              "url": "https://example.com",
              "content_type": "posterior_samples",
              "description": "string"
            },
            {
              "url": "https://example.com",
              "content_type": "skymap",
              "description": "string"
            }
          ]
        }
      ]
    }
  ]
}
```

## Description of the keys

1. Root level

    - `schema_version`: (string) The version of the schema used. Useful for backwards compatibility.
    - `catalog_name`: (string) The name of the catalog.
    - `catalog_description`: (string) A description of the catalog.
    - `doi`: (string, url) The full URL to the publication DOI related to this catalog.
    - `release_date`: The date of the public release of the data in the format `YYYY-MM-DD`.

2. Events level

    - `event_name`: (string) The name of the event using the convention `GWyymmdd_hhmmss`.
    - `gps`: (float) The GPS time of the detection.
    - `event_description`: (string) A short description of this event.
    - `detectors`: (list(string)) A list of detector data used for this event.

3. Search level

    - `pipeline_name`: (string) The name of the search pipeline.

4. PE sets level

    - `pe_set_name`: (string) The pipeline used to generate the parameter estimations.
    - `waveform_family`: (string) The name of the waveform family used in the estimation.
    - `data_url`: (string, url) The full URL to the file that stores posterior samples.
    - `is_preferred`: (bool) `true` if this set should be the preferred one to pick parameter values from.
        Exactly one of the PE sets must be preferred in order for results to be properly displayed
        in the catalog table. If this key is omitted, it defaults to `false`.

A list of waveform family names can be found in the lalsuite code site [https://lscsoft.docs.ligo.org/lalsuite/](https://lscsoft.docs.ligo.org/lalsuite/).

5. Parameters level

    - `parameter_name`: (string) Name of the parameter being estimated. See allowed values below.
    - `median`: (float) Median value of the posterior distribution.
    - `upper_95`: (float) Upper bound of the 95% confidence region.
    - `lower_05`: (float) Lower bound of the 95% confidence region.
    - `is_upper_bound`: (bool) `true` if this value is an upper bound, `false` otherwise. Defaults to `false` if omitted.
    - `is_lower_bound`: (bool) `true` if this value is an upper bound, `false` otherwise. Defaults to `false` if omitted.
    - `decimal_places`: (int) Number of decimal places of the best value to display, must be >= 0.
    - `unit`: The physical unit of the `median` value. See below for allowed values.
    - `links`: (object | null) Links to external resources. This section can be omitted.

6. Links level (optional)

    Note: For a link to posterior samples, use `data_url` under PE sets level.

    - `url`: (string, url) URL to external resource.
    - `content_type`: (string) The type of the resource: "skymap", "documentation", etc.
    - `description`: (string) A brief description of the resource.

## Notes

Allowed values for PE `parameter_name` keys are:

* `chirp_mass_source`: The chirp mass of the binary as measured in the source frame.
* `chirp_mass`: The chirp mass of the binary in detector frame.
* `mass_1_source`: The source mass of the heavier compact object in the merger, as measured in the source frame.
* `mass_2_source`: The source mass of the lighter compact object in the merger, as measured in the source frame.
* `total_mass_source`: The total mass of the binary as measured in the source frame.
* `final_mass_source`: The mass of the remnant compact object after merger, assuming a binary black hole model, and measured in the source frame.
* `chi_eff`: Spin parameter indicating the effective inspiral spin.
* `luminosity_distance`: The luminosity distance to the source.
* `redshift`: The calculated redshift.

A list for all PE standard names used by ligo is listed at LSC Soft site [https://lscsoft.docs.ligo.org/pesummary/stable/gw/parameters.html](https://lscsoft.docs.ligo.org/pesummary/stable/gw/parameters.html).

Allowed values for search `parameter_name` keys are:

* `snr`: The network Signal to Noise Ratio of the Matched Filtering.
* `pastro`: The probability of astronomical origin, assuming a compact binary.
* `far`: The False Alarm Rate of the detection in events per year.

Other values for `name` are permitted but will generate a warning message.

In case of being more than one search pipeline, the chosen figures to display will be the best values for the whole set.

### Units

All masses MUST be in units of solar masses. Acceptable values for solar mass abbreviation are the ones accepted by [astropy units](https://docs.astropy.org/en/stable/units/ref_api.html#module-astropy.units.astrophys) module: [`solMass`, `M_sun`, `Msun`].

The `luminosity_distance` `unit` key MUST have the value `Mpc`.

The `far` `unit` key MUST have the value `1/year`.

For dimensionless units, the key can be omitted or set to `null`.
