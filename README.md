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
