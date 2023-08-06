# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
# import collections
import json
import sys
import requests
import uuid
import logging
from ._utils._constants import api_prefix
from ._utils._utils import ApiInputs
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler(stream=sys.stdout)
# consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s  switch_api.%(module)s.%(funcName)s  %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')
consoleHandler.setFormatter(formatter)


def initialize(user_id: uuid.UUID, api_project_id: uuid.UUID):
    """"Initialize session with the API.

    Parameters
    ----------
    user_id : uuid.UUID
        Your UserID for the Switch Automation platform.
    api_project_id : uuid.UUID
        The ApiProjectID for the portfolio.

    Returns
    -------
    ApiInputs
        Returns the ApiInputs namedtuple that is required as an input to other functions.

    """

    payload = {}
    # headers = {'Content-Type': 'application/json; charset=utf-8'}

    url = api_prefix + api_project_id + "/Initialize/" + user_id
    response = requests.request("GET", url, data=payload, timeout=20)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status

    response_json = json.loads(response.text)
    datacentre = response_json['dataCentre']
    db_name = response_json['projectName']
    api_key = response_json['apiKey']
    auth = response_json['authenticated']
    email_address = response_json['emailAddress']
    data_feed_id = response_json['dataFeedId']
    data_feed_file_status_id = response_json['dataFeedFileStatusId']
    logger.info("Successfully initialized.")

    return ApiInputs(auth, email_address, user_id, api_key, api_project_id, datacentre, db_name, data_feed_id,
                     data_feed_file_status_id)
