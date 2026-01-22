import logging

from psu_mgmt.app import psu_mgmt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"
)

psu_mgmt.main()
