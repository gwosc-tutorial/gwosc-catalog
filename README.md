# Schemator

This repo is to develop and test a script that checks that the json schema for uploading community catalogs is correct.

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
                            "sigfigs": 2
                        },
                        {
                            "name": "mass_2_source",
                            "best": 13.4,
                            "upper": 5,
                            "lower": 2,
                            "upper_limit": false,
                            "lower_limit": false,
                            "sigfigs": 1
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

## Notes

- Event description is optional (can be null)
- Catalog description is mandatory
- PE set type is either "search" or "pe"
- data-url is a link to the posterior samples file
- links section can be entirely ommited

Acceptable values for PE name keys are:

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

All masses MUST be in units of solar masses.

The `luminosity_distance` key MUST be in units of Mpc.

***

A list for all PE names used by ligo is listed here:

https://lscsoft.docs.ligo.org/pesummary/stable/gw/parameters.html
