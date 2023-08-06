# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
A module containing the helper functions useful when integrating asset creation, asset updates, data ingestion, etc
into the Switch Automation platform.
"""
import sys
import pandas
# import pandera
import requests
# import datetime
import logging
import uuid
from typing import Union
# from .._utils._platform import _get_structure, Blob
from .._utils._constants import api_prefix, QUERY_LANGUAGE
from .._utils._utils import ApiInputs, _column_name_cap  # , _with_func_attrs, _work_order_schema

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s  %(name)s.%(funcName)s  %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')
consoleHandler.setFormatter(formatter)


def get_operation_state(upload_id: uuid.UUID, api_inputs: ApiInputs):
    """Get operation state

    Parameters
    ----------
    upload_id: uuid.UUID
        uploadId returned from the Data Operation
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
    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.db_name + "/" + api_inputs.api_project_id + \
        "/AdxDataOperation/" + upload_id
    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df = df.drop(columns=['NodeId', 'RootActivityId', 'Principal', 'User', 'Database'])
    return df


def load_data(dev_mode_path, api_inputs: ApiInputs):
    """Load data

    Parameters
    ----------
    dev_mode_path :

    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    pandas.DataFrame

    """
    if api_inputs.datacentre == '' or api_inputs.api_key == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    df = pandas.read_csv(dev_mode_path)

    return df


def data_table_exists(table_name: str, api_inputs: ApiInputs):
    """Validate if data table exists.

    Parameters
    ----------
    table_name: str :
        Table name to validate.
    api_inputs: ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    bool
        True if the datatable exists. False if the table does not exist.

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

    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.db_name + "/" + api_inputs.api_project_id + \
        "/DataTableExists/" + table_name

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status

    if response.text == 'true':
        logger.info("Response status: %s", response_status)
        logger.info("Data table '%s' exists.", table_name)
        return True
    else:
        logger.info("Response status: %s", response_status)
        logger.info("Data table '%s' does not exist.", table_name)
        return False


def get_sites(api_inputs: ApiInputs, include_tag_groups: Union[list, bool] = False,
              sql_where_clause: str = None, top_count: int = None):
    """Retrieve site information.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    include_tag_groups : Union[list, bool], default = False
        If False, no tag groups are included. If True, all tag groups will be returned. Else, if list, the Tag Groups
        in the list are retrieved as columns.
    sql_where_clause : str, default = None
        Optional `WHERE` clause in SQL syntax.
    top_count: int, default = None
        For use during testing to limit the number of records returned.


    Returns
    -------
    df : pandas.DataFrame

    """

    if top_count is None:
        top_count = 0

    tags_mode = False
    tag_groups = []
    if type(include_tag_groups) is list:
        tags_mode = True
        tag_groups = include_tag_groups
    elif type(include_tag_groups) is bool:
        tag_groups = []
        tags_mode = include_tag_groups

    payload = {
        "sendAllTags": tags_mode,
        "includeTagColumns": tag_groups,
        "sqlWhereClause": sql_where_clause,
        "topCount": top_count,
    }

    headers = {
        'x-functions-key': api_inputs.api_key,
        'Content-Type': 'application/json; charset=utf-8',
        'user-key': api_inputs.user_id
    }

    if api_inputs.datacentre == '' or api_inputs.api_key == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + \
        "/Integration/GetSites"

    response = requests.post(url, json=payload, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status

    df = pandas.read_json(response.text)

    return df


def get_device_sensors(api_inputs: ApiInputs, include_tag_groups: Union[list, bool] = False,
                       include_metadata_keys: Union[list, bool] = False, sql_where_clause: str = None,
                       top_count: int = None):
    """Retrieve device and sensor information.

    Optionally include all or a subset of tag groups and/or metadata keys depending on the configuration of the
    `include_tag_groups` and `include_metadata_keys` parameters. Whilst testing, there is the option to limit the number
    of records returned via the `top_count` parameter. If this parameter is not set, then the function will return all
    records.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    include_tag_groups : Union[list, bool], default = False
        If False, no tag groups are included. If True, all tag groups will be returned. Else, if list, the Tag Groups
        in the list are retrieved as columns.
    include_metadata_keys : Union[list, bool], default = False
        If False, no metadata keys are included. If True, all metadata keys will be returned. Else, if list,
        the metadata keys in the list are retrieved as columns.
    sql_where_clause : str, optional
        optional `WHERE` clause in SQL syntax.
    top_count: int, default = None
        For use during testing to limit the number of records returned.

    Returns
    -------
    df : pandas.DataFrame

    """
    if top_count is None:
        top_count = 0

    tags_mode = False
    tag_groups = []
    if type(include_tag_groups) is list:
        tags_mode = True
        tag_groups = include_tag_groups
    elif type(include_tag_groups) is bool:
        tag_groups = []
        tags_mode = include_tag_groups

    metadata_mode = False
    metadata_keys = []
    if type(include_metadata_keys) is list:
        metadata_mode = True
        metadata_keys = include_metadata_keys
    elif type(include_metadata_keys) is bool:
        metadata_keys = []
        metadata_mode = include_metadata_keys

    payload = {
        "tagsMode": tags_mode,
        "metadataMode": metadata_mode,
        "includeTagColumns": tag_groups,
        "includeMetadataColumns": metadata_keys,
        "sqlWhereClause": sql_where_clause,
        "topCount": top_count,
    }

    headers = {
        'x-functions-key': api_inputs.api_key,
        'Content-Type': 'application/json; charset=utf-8',
        'user-key': api_inputs.user_id
    }

    if api_inputs.datacentre == '' or api_inputs.api_key == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + \
        "/Integration/GetDeviceSensors"

    response = requests.post(url, json=payload, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status

    df = pandas.read_json(response.text)

    return df


def get_data(query_text, api_inputs: ApiInputs, query_language: QUERY_LANGUAGE = "sql"):
    """Retrieve data.

    Parameters
    ----------
    query_text : str
        SQL statement used to retrieve data.
    api_inputs : ApiInputs
        Object returned by initialize() function.
    query_language : QUERY_LANGUAGE
        The query language the query_text is written in.

    Returns
    -------
    df : pandas.DataFrame

    """
    payload = {
        "queryText": query_text,
        "queryLanguage": str(query_language)
    }
    headers = {
        'x-functions-key': api_inputs.api_key,
        'Content-Type': 'application/json; charset=utf-8',
        'user-key': api_inputs.user_id
    }

    if api_inputs.datacentre == '' or api_inputs.api_key == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.db_name + "/" + api_inputs.api_project_id + \
        "/Integration/GetData"
    response = requests.post(url, json=payload, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status

    df = pandas.read_json(response.text)

    return df


def get_states_by_country(api_inputs: ApiInputs, country: str):
    """Get list of States for selected country.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize() function.
        country: str
            Country to lookup states for.

        Returns
        -------
        df : pandas.DataFrame
            Data frame containing the states for the given country.

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

    url = api_prefix + "Country/States/" + country
    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df.columns = _column_name_cap(df.columns)

    return df


def get_templates(api_inputs: ApiInputs, object_property_type: str = None):
    """Get list of Templates by Type.

    Also retrieves the default unit of measure for the given template.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    object_property_type : str, Optional
        The object property type to filter to.

    Returns
    -------
    df : pandas.DataFrame
        Data frame containing the templates by type including the default unit of measure.

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

    url = ''
    if object_property_type is None:
        url = api_prefix + "Templates"
    elif object_property_type is not None:
        url = api_prefix + 'TemplatesByType/' + object_property_type
    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df.columns = _column_name_cap(df.columns)

    return df


def get_tag_groups(api_inputs: ApiInputs):
    """Get the sensor-level tag groups present for a portfolio.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    df : pandas.DataFrame
        Data frame containing the tag groups present in the given portfolio.

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

    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Tags"

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)

    return df


def get_metadata_keys(api_inputs: ApiInputs):
    """Get the device-level metadata keys for a portfolio.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    df : pandas.DataFrame
        Data frame containing the metadata keys present in the portfolio.

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

    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Metadata"

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df.columns = ['MetadataKey']

    return df


def get_units_of_measure(api_inputs: ApiInputs, object_property_type: str = None):
    """Get list of units of measure by type.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    object_property_type : str, Optional
        The ObjectPropertyType to filter on.

    Returns
    -------
    df : pandas.DataFrame
        Data frame containing the units of measure by type.

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

    url = ''
    if object_property_type is None:
        url = api_prefix + "Units"
    elif object_property_type is not None:
        url = api_prefix + 'UnitsByType/' + object_property_type

    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df.columns = _column_name_cap(df.columns)

    return df


def get_equipment_classes(api_inputs: ApiInputs):
    """Get list of Equipment Classes.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.

    Returns
    -------
    df : pandas.DataFrame
        Data frame containing the equipment classes.

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

    url = api_prefix + "EquipmentClasses"
    response = requests.request("GET", url, timeout=20, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text)
    df.columns = ['EquipmentClass']

    return df


# def get_portfolios(api_inputs: ApiInputs, search_term: str = None):
#     """Get list of units of measure by type.
#
#     Parameters
#     ----------
#     api_inputs : ApiInputs
#         Object returned by initialize() function.
#     search_term : str
#         The search_term used to filter list of portfolios to be retrieved.
#
#     Returns
#     -------
#     df : pandas.DataFrame
#         A list of portfolios.
#
#     """
#     payload = {}
#     headers = {
#         'x-functions-key': api_inputs.api_key,
#         'Content-Type': 'application/json; charset=utf-8',
#         'user-key': api_inputs.user_id
#     }
#
#     if api_inputs.datacentre == '' or api_inputs.api_key == '':
#         logger.error("You must call initialize() before using API.")
#         return pandas.DataFrame()
#
#     if search_term is None:
#         search_term = '*'
#
#     url = api_prefix + "Portfolios/" + search_term
#     response = requests.request("GET", url, timeout=20, headers=headers)
#     response_status = '{} {}'.format(response.status_code, response.reason)
#     if response.status_code != 200:
#         logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
#                      response.reason)
#         return response_status, pandas.DataFrame()
#     elif len(response.text) == 0:
#         logger.error('No data returned for this API call. %s', response.request.__dict__)
#         return response_status, pandas.DataFrame()
#
#     df = pandas.read_json(response.text)
#
#     return df
