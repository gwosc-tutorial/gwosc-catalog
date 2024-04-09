# Schemator

This repo is to develop and test a script that checks that the json schema for uploading community catalogs is correct.

## Installation

1. Clone repo

    `git clone https://git.ligo.org/gwosc/schemator.git`

2. Install

    `cd schemator; pip install .`

3. Check upload schema

    `ccverify path/to/mycatalog.json`

## Example

```json
{
    "name": "4-OGC",
    "description": "4-OGC includes 7 BBH mergers which were not previously reported ...",
    "doi": "https://doi.org/10.3847/1538-4357/aca591",
    "events": [
        {
            "name": "GW190218_110655",
            "gps": 1234523233.3,
            "description": null,
            "detectors": [
                "H1",
                "L1"
            ],
            "strain_channel": "string",
            "pe_sets": [
                {
                    "name": "ogc-pipeline",
                    "type": "pe",
                    "waveform-family": "IMRPhenomPv3HM",
                    "data-url": "https://zenodo.org/api/records/...",
                    "parameters": [
                        {
                            "name": "mass_1_source",
                            "best": 3.34,
                            "upper": 1,
                            "lower": 1,
                            "upper_limit": false,
                            "lower_limit": false,
                            "sigfigs": 2,
                            "unit": "M_sun"
                        },
                        {
                            "name": "luminosity_distance",
                            "best": 130.4,
                            "upper": 5,
                            "lower": 2,
                            "upper_limit": false,
                            "lower_limit": false,
                            "sigfigs": 4,
                            "unit": "Mpc"
                        },
                        // ... more parameter estimations
                    ],
                    "links": [
                        {
                            "url": "https://dcc.ligo.org/LIGO-P1800370/public",
                            "content-type": "posterior-samples",
                            "description": "DCC entry containing posterior samples for this PE run"
                        },
                        {
                            "url": "https://dcc.ligo.org/public/0169/P2000223/005/all_skymaps.tar",
                            "content-type": "skymap",
                            "description": "Tarball with skymap files"
                        },
                        // ... more links
                    ]
                },
                // ... more PE sets
            ]
        },
        // ... more events
    ]
}
```

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

3. PE sets level

    - `name`: (string) The pipeline used to generate the parameter estimations.
    - `type`: (string) Allowed values: ["pe", "search"]
    - `waveform-family`: (string) The name of the waveform family used in the estimation.
    - `data-url`: (string, url) The full URL to the posterior sample tarball online.

4. Parameters level

    - `name`: (string) Name of the parameter being estimated. See allowed values below.
    - `best`: (float) Best value of the parameter. Median value of the posterior distribution.
    - `upper`: (float) Upper bound of the 90% confidence region.
    - `lower`: (float) Lower bound of the 90% confidence region.
    - `upper_limit`: (bool) Whether this best value is an upper limit bound.
    - `lower_limit`: (bool) Whether this best value is an lower limit bound.
    - `sigfigs`: (int) Number of significant figures of the best value.
    - `unit`: The unit the `best` value was measured in. See below for allowed values.
    - `links`: (object | null) Links to external resources. This section can be ommited.

5. Links level (optional)

    - `url`: (string, url) URL to external resources like skymaps or posterior samples.
    - `content-type`: (string) Allowed values: ["posterior-samples", "skymap"].
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
* `far`: The False Alarm Rate of the detection in events per year.
* `p_astro`: The probability of astronomical origin, assuming a compact binary.

Other values for `name` are permitted but will generate a warning message.

### Units

All masses MUST be in units of solar masses. Acceptable values for solar mass abbreviation are the ones accepted by [astropy units](https://docs.astropy.org/en/stable/units/ref_api.html#module-astropy.units.astrophys) module: [`solMass`, `M_sun`, `Msun`].

The `luminosity_distance` `unit` key MUST have the value `Mpc`.

***

A list for all PE names used by ligo is listed here:

https://lscsoft.docs.ligo.org/pesummary/stable/gw/parameters.html

A list of waveform family names can be found here: (incorrect, update)

https://lscsoft.docs.ligo.org/lalsuite/
