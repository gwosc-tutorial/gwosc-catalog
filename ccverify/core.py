import json
import re
import logging


def _set_logger():
    import sys

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def verify_upload_schema(newcat):
    logger = logging.getLogger(__name__)

    mandatory_keys = ["catalog_name", "catalog_description", "doi", "events"]
    for akey in mandatory_keys:
        if akey not in newcat.keys():
            logger.warning(f"Mandatory key `{akey}` not found.")

    # Check for other unsupported keys
    other_keys = set(newcat.keys()) - set(mandatory_keys)
    if len(other_keys) != 0:
        logger.warning(f"Warning - Unrecognized keys: {other_keys}")

    # Parse events
    if "events" not in newcat.keys():
        return False
    events = newcat["events"]
    if len(events) == 0:
        logger.warning("No events found on `events` key.")
        return False
    for event in events:
        mandatory_keys = ["event_name", "gps", "event_description", "detectors",
                          "pe_sets", "search"]
        for akey in mandatory_keys:
            if akey not in event.keys():
                logger.warning(f"Event missing mandatory key `{akey}`.")

        if "name" in event.keys() and not bool(
            re.match(r"^GW\d{6}(?:_\d{6})?$", event["name"])
        ):
            logger.warning(f"Warning: Unusual name for event: {event['name']}")

        if "detectors" in event.keys():
            detectors = event["detectors"]
            allowed_detectors = ["H1", "L1", "V1", "G1", "K1"]
            if len(detectors) == 0:
                logger.warning("Empty list of detectors.")
            for det in detectors:
                if det not in allowed_detectors:
                    logger.warning(
                        f"Unrecognized detector: {det}\n Use one of {allowed_detectors}"
                    )

        if "pe_sets" not in event.keys():
            continue

        # Check for other unsupported keys
        other_keys = set(event.keys()) - set(mandatory_keys)
        if len(other_keys) != 0:
            logger.warning(f"Warning - Unrecognized keys: {other_keys}")

        # Parse PE sets
        pe_sets = event["pe_sets"]
        if len(pe_sets) == 0:
            logger.warning("Empty list of PE sets.")
            continue
        for peset in pe_sets:
            mandatory_keys = [
                "pe_set_name",
                "waveform_family",
                "data_url",
                "parameters",
            ]
            optional_keys = ["links"]
            for akey in mandatory_keys:
                if akey not in peset.keys():
                    logger.warning(f"PE Set missing mandatory key `{akey}`.")

            if "parameters" not in peset.keys():
                continue

            # Check for other unsupported keys
            other_keys = set(peset.keys()) - (set(mandatory_keys) | set(optional_keys))
            if len(other_keys) != 0:
                logger.warning(f"Warning - Unrecognized keys: {other_keys}")

            # Parse PE
            params = peset["parameters"]
            if len(params) == 0:
                logger.warning("Empty list of parameters.")
                continue

            for pe in params:
                mandatory_keys = [
                    "parameter_name",
                    "median",
                    "upper_95",
                    "lower_05",
                    "upper_limit",
                    "lower_limit",
                    "sigfigs",
                    "unit",
                ]
                for akey in mandatory_keys:
                    if akey not in pe.keys():
                        logger.warning(f"PE missing mandatory key `{akey}`.")
                if "name" in pe.keys():
                    allowed_names = [
                        "mass_1_source",
                        "mass_2_source",
                        "network_matched_filter_snr",
                        "luminosity_distance",
                        "chi_eff",
                        "total_mass_source",
                        "chirp_mass_source",
                        "chirp_mass",
                        "redshift",
                        "far",
                        "p_astro",
                        "final_mass_source",
                    ]
                    pe_name = pe["name"]
                    if pe_name not in allowed_names:
                        logger.warning(f"Unrecognized PE name: {pe_name}.")

                # Check for other unsupported keys
                other_keys = set(pe.keys()) - set(mandatory_keys)
                if len(other_keys) != 0:
                    logger.warning(f"Warning - Unrecognized keys: {other_keys}")

    logger.info("Verification finalized.")
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="ccverify",
        description="Check if the upload json schema for GWOSC community catalogs is correct.",
    )
    parser.add_argument("filename", help="Json file to check")
    args = parser.parse_args()
    _set_logger()
    with open(args.filename) as fp:
        newcat = json.load(fp)
    verify_upload_schema(newcat)


if __name__ == "__main__":
    main()
