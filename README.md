# `gwosc-catalog`

This repo is to develop and test a script that checks that the json schema for uploading community catalogs is correct.

## Installation

1. Clone repo

    `git clone git@github.com:gwosc-tutorial/gwosc-catalog.git`

2. Install

    `cd gwosc-catalog; pip install .`

3. Check upload schema

    `ccverify path/to/mycatalog.json`

## Example

An example of the schema can be found in the `schema.json` file on this repo.

## Key Description

1. Root level

    - `schema_version`: (string) The version of the schema used. Useful for backwards compatibility.
    - `catalog_name`: (string) The name of the catalog.
    - `catalog_description`: (string) A description of the catalog.
    - `doi`: (string, url) The full URL to the publication DOI related to this catalog.

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

Allowed values for search `parameter_name` keys are:

* `snr`: The network Signal to Noise Ratio of the Matched Filtering.
* `pastro`: The probability of astronomical origin, assuming a compact binary.
* `far`: The False Alarm Rate of the detection in events per year.

Other values for `name` are permitted but will generate a warning message.

### Units

All masses MUST be in units of solar masses. Acceptable values for solar mass abbreviation are the ones accepted by [astropy units](https://docs.astropy.org/en/stable/units/ref_api.html#module-astropy.units.astrophys) module: [`solMass`, `M_sun`, `Msun`].

The `luminosity_distance` `unit` key MUST have the value `Mpc`.

The `far` `unit` key MUST have the value `1/year`.

For dimensionless units, the key can be omitted or set to `null`.

***

A list for all PE names used by ligo is listed here:

https://lscsoft.docs.ligo.org/pesummary/stable/gw/parameters.html

A list of waveform family names can be found here: (incorrect, update)

https://lscsoft.docs.ligo.org/lalsuite/
