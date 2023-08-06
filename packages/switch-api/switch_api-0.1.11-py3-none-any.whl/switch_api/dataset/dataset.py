# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
A module for interacting with Data Sets from the Switch Automation platform.

"""
import pandas
import requests
from .._utils._constants import api_prefix
from .._utils._utils import ApiInputs
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s  switch_api.%(module)s.%(funcName)s  %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')
consoleHandler.setFormatter(formatter)


def get_folders(api_inputs: ApiInputs, folder_type="dataset"):
    """Get dataset folders

    Retrieves the list of DataSets folders for the given portfolio from the Switch Automation
    platform.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    folder_type : str
        Type of folder records to retrieve. (Default value = "dataset")

    Returns
    -------
    tuple[str, pandas.DataFrame]
        (response, df) - Returns the response status of the call & a dataframe containing the data returned by the call.

    """
    payload = {}
    headers = {
        'x-functions-key': api_inputs.api_key,
        'Content-Type': 'application/json; charset=utf-8',
        'user-key': api_inputs.user_id
    }

    if api_inputs.datacentre == '' or api_inputs.api_key == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Folders/FolderType/" + folder_type
    logger.info("Sending request: GET %s", url)
    response = requests.request("GET", url, data=payload, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()
    df = pandas.read_json(response.text)
    logger.info("API Call successful.")
    return response_status, df


def get_datasets_list(api_inputs: ApiInputs, include_path: bool = False, path_prefix="*"):
    """Get list of data sets.

    Retrieves the list of data set queries either for the entire project across all folders
    (if `include_path`=False) or specific to the folder designated in the `path_prefix`
    when `include_path` = True.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    include_path : bool, default = False
        Include the folder path (Default value = False).
    path_prefix : str
        The folder path where queries should be returned from (Default value = "*").

    Returns
    -------
    tuple[str, pandas.DataFrame]
        (response, df) - Returns the response status of the call & a dataframe containing the data returned by the call.

    """
    payload = {}
    headers = {
        'x-functions-key': api_inputs.api_key,
        'Content-Type': 'application/json; charset=utf-8',
        'user-key': api_inputs.user_id
    }

    if api_inputs.datacentre == '' or api_inputs.api_key == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Datasets/PathPrefix/" + \
        path_prefix.replace('/', '|') + "/IncludePath/" + str(include_path)
    response = requests.request("GET", url, data=payload, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    logger.info("API Call successful.")

    return response_status, df


# def get_dataset_details(api_inputs: ApiInputs, dataset_id, path_prefix="*"):
#     """Retrieve details of the given Data Set.
#
#      Retrieves the details of the given data set from the Switch Automation platform. This includes any parameters
#      required to be passed when using the get_data() function.
#
#     Parameters
#     ----------
#     api_inputs : ApiInputs
#         Object returned by initialize() function.
#     dataset_id : uuid.UUID
#         The identifier for the data set.
#     path_prefix : str, default = '*'
#         The folder path for the given data set (Default value = "*").
#
#     Returns
#     -------
#     tuple[str,pandas.DataFrame]
#         (resp_sts, df) - Returns the response status of the call and a dataframe containing the data returned by the call.
#
#     """
#     payload = {}
#     headers = {
#         'x-functions-key': api_inputs.api_key,
#         'Content-Type': 'application/json; charset=utf-8',
#         'user-key': api_inputs.user_id
#     }
#
#     # search_path = "*"
#
#     if api_inputs.datacentre == '' or api_inputs.api_key == '':
#         logger.error("You must call initialize() before using API.")
#         return pandas.DataFrame()
#
#     url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/DatasetDetails/" + str(dataset_id) \
#         + "/PathPrefix/" + path_prefix.replace('/', '|')
#     logger.info('DataSets: Sending request for DatasetID: %s', dataset_id)
#     response = requests.request("GET", url, data=payload, timeout=20, headers=headers)
#     response_status = '{} {}'.format(response.status_code, response.reason)
#     if response.status_code != 200:
#         logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
#                      response.reason)
#         return response_status, pandas.DataFrame()
#     elif len(response.text) == 0:
#         logger.error('No data returned for this API call. %s', response.request.__dict__)
#         return response_status, pandas.DataFrame()
#     df = pandas.read_json(response.text)
#     logger.info("API Call successful.")
#     df = df.set_index(['id', 'name', 'parameters'])
#
#     return response_status, df


def get_data(api_inputs: ApiInputs, dataset_id, parameters: dict = None):
    """Retrieve data for the given Data Set.

    Retrieves data from the Switch Automation platform for the given data set.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    dataset_id : uuid.UUID
        The identifier for the data set.
    parameters : dict, Optional
        Any parameters required to be passed to the data set.

    Returns
    -------
    tuple[str, pandas.DataFrame]
        (response, df) - Returns the response status of the call & a dataframe containing the data returned by the call.
    """
    # payload = {}
    headers = {
        'x-functions-key': api_inputs.api_key,
        'Content-Type': 'application/json; charset=utf-8',
        'user-key': api_inputs.user_id
    }

    if api_inputs.datacentre == '' or api_inputs.api_key == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/DatasetData/" + str(dataset_id)
    logger.info('DataSets: Sending request for DatasetID: %s', dataset_id)

    if parameters is None:
        parameters = {}
    response = requests.post(url, json=parameters, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('DataSets: no data returned for this call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text, dtype=False)
    logger.info("API Call successful.")

    return response_status, df
