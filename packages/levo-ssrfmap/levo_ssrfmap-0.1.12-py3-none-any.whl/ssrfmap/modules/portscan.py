import concurrent.futures
import logging
from datetime import datetime
from typing import List

from ssrfmap.core.utils import gen_ip_list, wrapper_http

name = "portscan"
description = "Scan ports of the target"
author = "Swissky"
documentation: List[str] = []


class exploit:
    def __init__(self, requester, args):
        logging.info("Module '{}' launched !".format(name))
        r = requester.do_request(args.param, "")

        load_ports = ""
        with open("data/ports", "r") as f:
            load_ports = f.readlines()

        # Using a generator to create the host list
        gen_host = gen_ip_list("127.0.0.1", args.level)
        for ip in gen_host:
            # We can use a with statement to ensure threads are cleaned up promptly
            with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
                future_to_url = {
                    executor.submit(
                        self.concurrent_request, requester, args.param, ip, port, r
                    ): port
                    for port in load_ports
                }

    def concurrent_request(self, requester, param, host, port, compare):
        try:
            payload = wrapper_http("", host, port.strip())
            r = requester.do_request(param, payload)

            # Display Open port
            if r != None and not "Connection refused" in r.text:
                timer = datetime.today().time().replace(microsecond=0)
                port = port.strip() + " " * 20

                # Check if the request is the same
                if r.text != "" and r.text != compare.text:
                    logging.info(
                        "\t[{}] IP:{:12s}, Found \033[32mopen     \033[0m port n°{}".format(
                            timer, host, port
                        )
                    )
                else:
                    logging.info(
                        "\t[{}] IP:{:12s}, Found \033[31mfiltered\033[0m  port n°{}".format(
                            timer, host, port
                        )
                    )

            timer = datetime.today().time().replace(microsecond=0)
            port = port.strip() + " " * 20
            logging.info("\t[{}] Checking port n°{}".format(timer, port), end="\r"),

        # Timeout is a potential port
        except Exception as e:
            logging.debug(e)
            timer = datetime.today().time().replace(microsecond=0)
            port = port.strip() + " " * 20
            logging.info(
                "\t[{}] IP:{:212}, \033[33mTimed out\033[0m  port n°{}".format(
                    timer, host, port
                )
            )
            pass
