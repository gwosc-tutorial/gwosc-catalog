# JSON Schema

## Example

An example of the schema can be found below and the description of the keys after the example.

```json
{
  "schema_version": "0.1.0a3",
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
      "gracedb_id": "S220911ab",
      "search": [
        {
          "pipeline_name": "string",
          "parameters": [
            {
              "parameter_name": "far",
              "best": 0.00001,
              "is_upper_bound": true,
              "decimal_places": 5,
              "unit": "1/year"
            },
            {
              "parameter_name": "pastro",
              "best": 0.99,
              "is_lower_bound": true,
              "decimal_places": 2
            },
            {
              "parameter_name": "snr",
              "best": 9.34,
              "upper_error": 0.01,
              "lower_error": 0.01,
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

## Overview

This format will be used to create catalogs in the GWOSC Event Portal.  In many cases, looking
at examples in the Event Portal can show how various keys are used.

### Release List View

The [Release List View](https://gwosc.org/eventapi/html/) shows the name of each catalog
(`catalog_name`) along with the `catalog_description`.

### Event List View

The [Event List View](https://gwosc.org/eventapi/html/GWTC-3-confident/)
shows the name of each
event (`event_name`), along with a list of parameters for each event.
It will also display the `catalog_description` and `catalog_name`.
This view will display the values of all parameters
with names that match the list of "Recognized Parameters" below.

### Event Detail View

The [Event Detail View](https://gwosc.org/eventapi/html/GWTC-3-confident/GW200129_065458/v1/)
shows information about a single event.  The page lists each search and PE Set, along with
all parameters associated with each one, including both recognized parameters and
any additional parameters (see "Notes" below).

The `data_url` is displayed for each PE set as a link to the "Source File".  This should point
to the data release for each event, and usually points to a posterior sample file if available.
Additional `links` may optionally be added as well, which can point to any associated files
or documentation that may help a user better understand the data.


## Description of the keys

Keys marked "optional" are not required to be inlcuded; other keys are required.  

1. Root level

    - `schema_version`: (string) The version of the schema used. Useful for backwards compatibility.
    - `catalog_name`: (string) The name of the catalog.
    - `catalog_description`: (string) A description of the catalog.
    - `doi`: (string, url) The full URL to the publication DOI related to this catalog.
    - `release_date`: The date of the public release of the data in the format `YYYY-MM-DD`.

2. Events level

    - `event_name`: (string) The name of the event using the convention `GWyymmdd_hhmmss`.
    - `gps`: (float) The GPS time of the detection.  Geocenter times are preferred.
    - `event_description`: (string; optional) Can be used for any user notes for a particular event.  This appears in a box on the Event Detail View. 
    - `detectors`: (list(string); optional) A list of detectors for which strain data should be
    publicly released for this event.  This parameter is not necessary for groups outside the LVK.
    - `gracedb_id`: (str; optional) The associated GraceDB superevent ID if any.
    This is an optional key but we recommend adding it whenever possible.

3. Search level

    - `pipeline_name`: (string) The name of the search pipeline.

4. PE sets level (Optional)

    - `pe_set_name`: (string) The pipeline used to generate the parameter estimations.
    - `waveform_family`: (string) Indicates the waveform approximant used for a PE set.  In LVK data
    sets, this is a key that points to the associated posterior samples within the data release file.
    - `data_url`: (string, url; optional)  This should point to the source data for the analysis of each event.  It 
    typically points to a posterior sample file if available.   
    - `is_preferred`: (bool; optional) The `is_preferred` PE set will be used to
    display parameter values on the "Event List" view.  
        Exactly one of the PE sets must have `is_preferred = true` in order for
	"Recognized Parameter" values to be properly displayed
        in the Event List. If this key is omitted, it defaults to `false`.

5. Parameters level

    - `parameter_name`: (string) Name of the parameter being estimated. See allowed values below.
    - `best`: (float) Value for a parameter (often the median value of the posterior distribution)
    - `upper_error`: (float; optional) Size of the upper error-bar of the 90% credible region.  OK to use different uncertainty definition if noted in documentation.
    - `lower_error`: (float; optional) Size of the lower error-bar of the 90% credible region.  OK to use a different uncertainty definition if noted in documentation.
    - `is_upper_bound`: (bool; optional) `true` if this value is an upper bound, `false` otherwise. Defaults to `false` if omitted.  Setting this to `true` diplays a less-than sign before the value.
    - `is_lower_bound`: (bool; optional) `true` if this value is an upper bound, `false` otherwise. Defaults to `false` if omitted.  Setting this to `true` displays a greater-than sign before the value.
    - `decimal_places`: (int) Number of decimal places of the best value to display, must be >= 0.  Displayed values will be rounded to this number of decimal places.
    - `unit`: The physical unit of the `median` value. See below for allowed values.
    - `links`: (object; optional) Links to any additional documentation or files that are helpful for the user.

6. Links level (optional)

    - `url`: (string, url) URL to external resource.
    - `content_type`: (string) The type of the resource: "skymap", "documentation", etc.
    - `description`: (string) A brief description of the resource.

## Notes

### Recgonized parameters

Recognized values for PE `parameter_name` keys are:

* `chirp_mass_source`: The chirp mass of the binary as measured in the source frame.
* `mass_1_source`: The source mass of the heavier compact object in the merger, as measured in the source frame.
* `mass_2_source`: The source mass of the lighter compact object in the merger, as measured in the source frame.
* `total_mass_source`: The total mass of the binary as measured in the source frame.
* `final_mass_source`: The mass of the remnant compact object after merger, assuming a binary black hole model, and measured in the source frame.
* `chi_eff`: Spin parameter indicating the effective inspiral spin.
* `luminosity_distance`: The luminosity distance to the source.
* `redshift`: The calculated redshift.


A list of parameters commonly used in PE by the LVK collaboration is at [https://lscsoft.docs.ligo.org/pesummary/stable/gw/parameters.html](https://lscsoft.docs.ligo.org/pesummary/stable/gw/parameters.html).

Recognized values for search `parameter_name` keys are:

* `snr`: The network Signal to Noise Ratio of the signal.
* `pastro`: The probability of astronomical origin, assuming a compact binary.
* `far`: The False Alarm Rate of the detection in events per year.
* `chirp_mass`: The chirp mass of the binary in detector frame.

Other values for `name` are permitted and will be displayed on the Event Detail page, with the exceptions of
"p_astro" and "network_matched_filter_snr", which are reserve keywords and should not be used.

If multiple search pipeline results are included, the most significant values for `snr`, `pastro`, and `far` will
be displayed on the Event List page.  If multiple PE sets are included, the values from the PE set marked as
`is_preferred` = `true` will be displayed on the Event List page.

If the `snr` is available both from PE and search pipelines, then the
value from the preferred PE pipeline will be used on the Event List page.

### Units

In most cases, we accept any units recognized by [astropy units](https://docs.astropy.org/en/stable/units/ref_api.html#module-astropy.units.astrophys), and we will convert to our preferred units.

Preferred units are:

 * Mass in solar masses (`Msun`)
 * Distance in `Mpc`
 * False Alarm Rate in `1/year`
 * For dimenonless quantities, units can be omitted or set to `null`
 
