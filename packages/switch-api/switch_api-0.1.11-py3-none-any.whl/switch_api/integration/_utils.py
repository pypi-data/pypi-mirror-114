# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
A module containing the helper functions useful when integrating asset creation, asset updates, data ingestion, etc
into the Switch Automation platform.
"""
import pandas
import requests
import datetime
import logging
import sys
from .._utils._constants import api_prefix  # , QUERY_LANGUAGE
from .._utils._utils import ApiInputs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s  switch_api.%(module)s.%(funcName)s  %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')
consoleHandler.setFormatter(formatter)


def _adx_support(api_inputs: ApiInputs, build_sites=False, build_sensors=False):
    adx_support_prefix = ''
    if api_inputs.datacentre == 'AU':
        adx_support_prefix = 'australiaeast'
    elif api_inputs.datacentre == 'EA':
        adx_support_prefix = 'australiaeast'
    elif api_inputs.datacentre == 'US':
        adx_support_prefix = 'centralus'

    if adx_support_prefix == '':
        logger.error('Invalid Data Centre: ' + api_inputs.datacentre)
        return

    if build_sites:
        adx_support_url = 'https://adxsupport-' + adx_support_prefix + \
                          '-prod.azurewebsites.net/api/sites?apiProjectId=' + api_inputs.api_project_id
        requests.get(adx_support_url)

    if build_sensors:
        adx_support_url = 'https://adxsupport-' + adx_support_prefix + \
                          '-prod.azurewebsites.net/api/sensors?apiProjectId=' + api_inputs.api_project_id
        requests.get(adx_support_url)


def _timezones(api_inputs: ApiInputs):
    """Get timezones

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    df : pandas.DataFrame


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

    # upload Blobs to folder
    url = api_prefix + "Timezones"
    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text, orient='index')
    df.rename(columns={0: 'TimezoneName'}, inplace=True)
    df['TimezoneId'] = df.index

    return df


def _timezone_offsets(api_inputs: ApiInputs, date_from: datetime.date, date_to: datetime.date,
                      installation_id_list: list):
    """Get timezones

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    date_from : datetime.date
        First (earliest) record
    date_to : datetime.date
        Last (latest) record
    installation_id_list : list
        List of InstallationIDs

    Returns
    -------
    df : pandas.DataFrame
        A dataframe containing the timezone offsets per InstallationID - if multiple timezone offsets occur for the
        submitted period, there will be a row per offset date range. E.g. for a timezone with daylight savings

    """
    payload = {
        "dateFrom": date_from.isoformat(),
        "dateTo": date_to.isoformat(),
        "installationIds": installation_id_list
    }

    headers = {
        'x-functions-key': api_inputs.api_key,
        'Content-Type': 'application/json; charset=utf-8',
        'user-key': api_inputs.user_id
    }

    if api_inputs.datacentre == '' or api_inputs.api_key == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/TimeZoneOffsets"
    response = requests.post(url, json=payload, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()

    response_data_frame = pandas.read_json(response.text)

    return response_data_frame
