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

    - `name`: (string) The name of the catalog.
    - `description`: (string) A description of the catalog.
    - `doi`: (string, url) The full URL to the publication DOI related to this catalog.

2. Events level

    - `name`: (string) The name of the event using the convention `GWyymmdd_hhmmss`.
    - `gps`: (float) The GPS time of the detection.
    - `description`: (string | null) A short description of this event.
    - `detectors`: (list(string))
    - `strain_channel`: (string | null) The strain channel name used for the analysis.

3. Search level

    - `pipeline_name`: (string) The name of the search pipeline.
    - `pastro`: The probability of astronomical origin, assuming a compact binary.
    - `far`: The False Alarm Rate in unites of events per year.

4. PE sets level

    - `name`: (string) The pipeline used to generate the parameter estimations.
    - `waveform_family`: (string) The name of the waveform family used in the estimation.
    - `data_url`: (string, url) The full URL to the posterior sample tarball online.

5. Parameters level

    - `name`: (string) Name of the parameter being estimated. See allowed values below.
    - `best`: (float) Best value of the parameter. Median value of the posterior distribution.
    - `upper`: (float) Upper bound of the 90% confidence region.
    - `lower`: (float) Lower bound of the 90% confidence region.
    - `upper_limit`: (bool) Whether this best value is an upper limit bound.
    - `lower_limit`: (bool) Whether this best value is an lower limit bound.
    - `sigfigs`: (int) Number of significant figures of the best value.
    - `unit`: The unit the `best` value was measured in. See below for allowed values.
    - `links`: (object | null) Links to external resources. This section can be ommited.

6. Links level (optional)

    - `url`: (string, url) URL to external resources like skymaps or posterior samples.
    - `content_type`: (string) Allowed values: ["posterior_samples", "skymap"].
    - `description`: (string) A brief description of the resource.

## Notes

Allowed values for PE `name` keys are:

* `chirp_mass_source`: The chirp mass of the binary as measured in the source frame.
* `chirp_mass`: The chirp mass of the binary in detector frame.
* `mass_1_source`: The source mass of the heavier compact object in the merger, as measured in the source frame.
* `mass_2_source`: The source mass of the lighter compact object in the merger, as measured in the source frame.
* `total_mass_source`: The total mass of the binary as measured in the source frame.
* `final_mass_source`: The mass of the remnant compact object after merger, assuming a binary black hole model, and measured in the source frame.
* `chi_eff`: Spin parameter indicating the effective inspiral spin.
* `luminosity_distance`: The luminosity distance to the source.
* `redshift`: The calculated redshift.
* `network_matched_filter_snr`: The network Signal to Noise Ratio of the Matched Filtering.

Other values for `name` are permitted but will generate a warning message.

### Units

All masses MUST be in units of solar masses. Acceptable values for solar mass abbreviation are the ones accepted by [astropy units](https://docs.astropy.org/en/stable/units/ref_api.html#module-astropy.units.astrophys) module: [`solMass`, `M_sun`, `Msun`].

The `luminosity_distance` `unit` key MUST have the value `Mpc`.

***

A list for all PE names used by ligo is listed here:

https://lscsoft.docs.ligo.org/pesummary/stable/gw/parameters.html

A list of waveform family names can be found here: (incorrect, update)

https://lscsoft.docs.ligo.org/lalsuite/
