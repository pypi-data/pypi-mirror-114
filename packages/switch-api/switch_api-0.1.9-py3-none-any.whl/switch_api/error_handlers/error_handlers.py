# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
This module contains the helper functions for error handling.

The module contains three functions:
    - invalid_file_format() which should be used to validate the source file received against the expected schema and
      post any issues identified to the data feed dashboard.

    - post_errors() which is used to post errors (apart from those identified by the invalid_file_format() function) to
      the data feed dashboard.

    - validate_datetime() which checks whether the values of the datetime column(s) of the source file are valid. Any
      datetime errors identified by this function should be passed to the post_errors() function.

The validate_datetime() function can be used to validate the datetime column(s) of the source file. The output
`df_invalid_datetime` from this function should be passed to the post_errors() function. For example,

>>> import pandas as pd
>>> import switch_api as sw
>>> api_inputs = sw.initialize(user_id, api_project_id) # set api_project_id to the relevant portfolio and user_id to
                                                       # your own user identifier
>>> test_df = pd.DataFrame({'DateTime':['2021-06-01 00:00:00', '2021-06-01 00:15:00', '', '2021-06-01 00:45:00'],
... 'Value':[10, 20, 30, 40], 'device_id':['xyz', 'xyz', 'xyz', 'xyz']})
>>> df_invalid_datetime, df = validate_datetime(df=test_df, datetime_col=['DateTime'], dt_fmt='%Y-%m-%d %H:%M:%S')
>>> if df_invalid_datetime.shape[0] != 0:
...     sw.error_handlers.post_errors(api_inputs, df_invalid_datetime, error_type='DateTime')

"""
import pandas
import pandera
import logging
import requests
import sys
from typing import Optional, List, Union
from .._utils._constants import api_prefix, ERROR_TYPE
from .._utils._utils import ApiInputs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s  switch_api.%(module)s.%(funcName)s  %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')
consoleHandler.setFormatter(formatter)


def invalid_file_format(api_inputs: ApiInputs, schema: pandera.DataFrameSchema, raw_df: pandas.DataFrame):
    """Validates the raw file format and posts any errors to data feed dashboard

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by call to initialize()
    schema : pandera.DataFrameSchema
        The defined data frame schema object to be used for validation.
    raw_df : pandas.DataFrame
        The raw dataframe created by reading the file.

    Returns
    -------
    response_data_frame : pandas.DataFrame
        Data frame containing the response from API after posting any errors to data feed dashboard.

    """
    if api_inputs.datacentre == '' or api_inputs.api_key == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = {
        'x-functions-key': api_inputs.api_key,
        'Content-Type': 'application/json; charset=utf-8',
        'user-key': api_inputs.user_id
    }

    try:
        schema.validate(raw_df, lazy=True)
    except pandera.errors.SchemaErrors as err:
        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/DataFeedErrors/FileFormat"
        print(err.failure_cases)
        schema_error = err.failure_cases
        response = requests.post(url, data=schema_error.to_json(orient='records'), headers=headers)
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


def post_errors(api_inputs: ApiInputs, errors_df: pandas.DataFrame, error_type: ERROR_TYPE):
    """Post errors to the Data Feed Dashboard

    Post dataframe containing the errors of type ``error_type`` to the Data Feed Dashboard in the Switch Platform.

    Parameters
    ----------
    api_inputs : ApiInputs
        The object returned by call to initialize() function.
    errors_df : pandas.DataFrame
        The dataframe containing the rows with errors.
    error_type : ERROR_TYPE
        The type of error being posted to Data Feed Dashboard.

    Returns
    -------
    response_boolean: boolean
        True or False indicating the success of the call

    """
    if api_inputs.datacentre == '' or api_inputs.api_key == '':
        logger.error("You must call initialize() before using API.")
        return False

    headers = {
        'x-functions-key': api_inputs.api_key,
        'Content-Type': 'application/json; charset=utf-8',
        'user-key': api_inputs.user_id
    }
    url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/DataFeedErrors/" + error_type + \
        "/" + str(api_inputs.data_feed_id) + "/" + str(api_inputs.data_feed_file_status_id)

    response = requests.post(url, data=errors_df.to_json(orient='records'), headers=headers)

    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, False
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s', response.request.__dict__)
        return response_status, False

    return response.text


def validate_datetime(df: pandas.DataFrame, datetime_col: Union[str, List[str]],
                      dt_fmt: Optional[str] = None):  # -> tuple[pandas.DataFrame, pandas.DataFrame]:
    """Check for datetime errors.

    Returns a tuple ``(df_invalid_datetime, df)``, where:
        - ``df_invalid_datetime`` is a dataframe containing the extracted rows of the input df with invalid datetime
        values.

        - ``df`` is the original dataframe input after dropping any rows with datetime errors.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe that contains the columns to be validated.
    datetime_col: List[str]
        List of column names that contain the datetime values to be validated. If passing a single column name in as a
        string, it will be coerced to a list.
    dt_fmt : Optional[str]
        The expected format of the datetime columns to be coerced. The strftime to parse time, eg "%d/%m/%Y", note
        that "%f" will parse all the way up to nanoseconds. See strftime documentation for more information on
        choices: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

    Returns
    -------
    df_invalid_datetime, df : tuple[pandas.DataFrame, pandas.DataFrame]
        (df_invalid_datetime, df) - where: `df_invalid_date

    Notes
    -----
    If the ``df_invalid_datetime`` dataframe is not empty, then the dataframe should be passed to the ``post_errors()``
    function using ``error_type = 'DateTime'``. See example code below:

    >>> import pandas as pd
    >>> import switch_api as sw
    >>> api_inputs = sw.initialize(user_id, api_project_id) # set api_project_id to the relevant portfolio and user_id
    ...                                                     # to your own user identifier
    >>> test_df = pd.DataFrame({'DateTime':['2021-06-01 00:00:00', '2021-06-01 00:15:00', '', '2021-06-01 00:45:00'],
    ... 'Value':[10, 20, 30, 40], 'device_id':['xyz', 'xyz', 'xyz', 'xyz']})
    >>> df_invalid_datetime, df = validate_datetime(df=test_df, datetime_col=['DateTime'], dt_fmt='%Y-%m-%d %H:%M:%S')
    >>> if df_invalid_datetime.shape[0] != 0:
    ...     sw.error_handlers.post_errors(api_inputs, df_invalid_datetime, error_type='DateTime')

    """

    if type(datetime_col) == str:
        datetime_col = [datetime_col]
    elif type(datetime_col) == list:
        datetime_col = datetime_col
    else:
        logger.error('datetime_col: Invalid format - datetime_col must be a string or list of strings.')

    val_dt_cols = []
    for i in datetime_col:
        val_dt_cols.append(i + '_dt')
    lst = [None] * len(datetime_col)

    if dt_fmt is None:
        for i in range(len(datetime_col)):
            df[val_dt_cols[i]] = pandas.to_datetime((df[datetime_col[i]]), errors='coerce')
            lst[i] = df[df[val_dt_cols[i]].isnull()]
            df = df[df[val_dt_cols[i]].notnull()]
            lst[i] = lst[i].drop(val_dt_cols[i], axis=1)
            df = df.drop(val_dt_cols[i], axis=1)
        df_invalid_datetime = pandas.concat(lst, axis=0)
        df[datetime_col] = df[datetime_col].apply(lambda x: pandas.to_datetime(x))
        logger.info('Row count with invalid datetime values: %s', df_invalid_datetime.shape[0])
        logger.info('Row count with valid datetime values: %s', df.shape[0])
        return df_invalid_datetime, df
    else:
        for i in range(len(datetime_col)):
            df[val_dt_cols[i]] = pandas.to_datetime((df[datetime_col[i]]), errors='coerce', format=dt_fmt)
            lst[i] = df[df[val_dt_cols[i]].isnull()]
            df = df[df[val_dt_cols[i]].notnull()]
            lst[i] = lst[i].drop(val_dt_cols[i], axis=1)
            df = df.drop(val_dt_cols[i], axis=1)
        df_invalid_datetime = pandas.concat(lst, axis=0)
        df[datetime_col] = df[datetime_col].apply(lambda x: pandas.to_datetime(x, format=dt_fmt))
        logger.info('Row count with invalid datetime values: %s', df_invalid_datetime.shape[0])
        logger.info('Row count with valid datetime values: %s', df.shape[0])
        return df_invalid_datetime, df

# def missing_devices(api_inputs: ApiInputs, missing_devices_df: pandas.DataFrame):
#     """Send devices unable to be identified in platform to data feed dashboard.
#
#     Any records in the data file that cannot be aligned to a device within the Switch Automation platform.
#
#     Parameters
#     ----------
#     api_inputs : ApiInputs
#         Object returned by call to initialize()
#     missing_devices_df : pandas.DataFrame
#         The dataframe containing the unique instances of devices that do not match any existing in the Switch
#         platform.
#
#     Returns
#     -------
#     response_data_frame : pandas.DataFrame
#         Data frame containing the response from API after posting any errors to data feed dashboard.
#
#     """
#     if api_inputs.datacentre == '' or api_inputs.api_key == '':
#         logger.error("You must call initialize() before using API.")
#         return pandas.DataFrame()
#
#     headers = {
#         'x-functions-key': api_inputs.api_key,
#         'Content-Type': 'application/json; charset=utf-8',
#         'user-key': api_inputs.user_id
#     }
#
#     url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/DataFeedErrors/MissingDevices"
#     response = requests.post(url, data=missing_devices_df.to_json(orient='records'), headers=headers)
#     response_status = '{} {}'.format(response.status_code, response.reason)
#     if response.status_code != 200:
#         logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
#                      response.reason)
#         return response_status, pandas.DataFrame()
#     elif len(response.text) == 0:
#         logger.error('No data returned for this API call. %s', response.request.__dict__)
#         return response_status, pandas.DataFrame()
#
#     response_data_frame = pandas.read_json(response.text)
#
#     return response_data_frame


# def invalid_datetime(api_inputs: ApiInputs, df: pandas.DataFrame, datetime_col: List[str],
#                      dt_fmt: Optional[str] = None): # -> tuple[pandas.DataFrame, pandas.DataFrame]:
#     """Check for datetime errors.
#
#     Returns tuple in the form ``(df_invalid_datetime, df)`` where:
#         - ``df_invalid_datetime`` is a dataframe containing the extracted rows of the input `df` with invalid
#         datetime values.
#
#         - ``df`` is the original dataframe input after dropping any rows with datetime errors
#
#     Parameters
#     ----------
#     api_inputs: ApiInputs
#         The object returned by call to initialize()
#     df : pandas.DataFrame
#         The dataframe that contains the columns to be validated.
#     datetime_col: List[str]
#         List of column names
#     dt_fmt : Optional[str]
#         The expected format of the datetime columns to be coerced. The strftime to parse time, eg "%d/%m/%Y", note
#         that "%f" will parse all the way up to nanoseconds. See strftime documentation for more information on
#         choices: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
#
#     Returns
#     -------
#     df_invalid_datetime, df : tuple[pandas.DataFrame, pandas.DataFrame]
#
#         *df_invalid_datetime* : Dataframe containing the extracted rows of the input df with invalid datetime values.
#
#         df: The original dataframe input after dropping any rows with datetime errors.
#     df : pandas.DataFrame
#         The original dataframe input after dropping any rows with datetime errors
#
#     """
#
#     if api_inputs.datacentre == '' or api_inputs.api_key == '':
#         logger.error("You must call initialize() before using API.")
#         return pandas.DataFrame()
#
#     headers = {
#         'x-functions-key': api_inputs.api_key,
#         'Content-Type': 'application/json; charset=utf-8',
#         'user-key': api_inputs.user_id
#     }
#     url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/DataFeedErrors/DateTime"
#
#     if type(datetime_col) == str:
#         datetime_col = [datetime_col]
#     elif type(datetime_col) == list:
#         datetime_col = datetime_col
#     else:
#         return 'datetime_col: Invalid format. datetime_col must be a string or list of strings.'
#
#     val_dt_cols = []
#     for i in datetime_col:
#         val_dt_cols.append(i + '_dt')
#     lst = [None] * len(datetime_col)
#
#     if dt_fmt is None:
#         for i in range(len(datetime_col)):
#             df[val_dt_cols[i]] = pandas.to_datetime((df[datetime_col[i]]), errors='coerce')
#             lst[i] = df[df[val_dt_cols[i]].isnull()]
#             df = df[df[val_dt_cols[i]].notnull()]
#             lst[i] = lst[i].drop(val_dt_cols[i], axis=1)
#             df = df.drop(val_dt_cols[i], axis=1)
#         df_invalid_datetime = pandas.concat(lst, axis=0)
#         df[datetime_col] = df[datetime_col].apply(lambda x: pandas.to_datetime(x))
#
#         response = requests.post(url, data=df_invalid_datetime.to_json(orient='records'), headers=headers)
#         response_status = '{} {}'.format(response.status_code, response.reason)
#         if response.status_code != 200:
#             logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
#                          response.reason)
#             return response_status, pandas.DataFrame()
#         elif len(response.text) == 0:
#             logger.error('No data returned for this API call. %s', response.request.__dict__)
#             return response_status, pandas.DataFrame()
#
#         response_data_frame = pandas.read_json(response.text)
#
#         return df_invalid_datetime, df
#     else:
#         for i in range(len(datetime_col)):
#             df[val_dt_cols[i]] = pandas.to_datetime((df[datetime_col[i]]), errors='coerce', format=dt_fmt)
#             lst[i] = df[df[val_dt_cols[i]].isnull()]
#             df = df[df[val_dt_cols[i]].notnull()]
#             lst[i] = lst[i].drop(val_dt_cols[i], axis=1)
#             df = df.drop(val_dt_cols[i], axis=1)
#         df_invalid_datetime = pandas.concat(lst, axis=0)
#         df[datetime_col] = df[datetime_col].apply(lambda x: pandas.to_datetime(x, format=dt_fmt))
#
#         response = requests.post(url, data=df_invalid_datetime.to_json(orient='records'), headers=headers)
#         response_status = '{} {}'.format(response.status_code, response.reason)
#         if response.status_code != 200:
#             logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
#                          response.reason)
#             return response_status, pandas.DataFrame()
#         elif len(response.text) == 0:
#             logger.error('No data returned for this API call. %s', response.request.__dict__)
#             return response_status, pandas.DataFrame()
#
#         response_data_frame = pandas.read_json(response.text)
#
#         return df_invalid_datetime, df
