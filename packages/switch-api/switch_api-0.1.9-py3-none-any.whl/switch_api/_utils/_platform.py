# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
A module for .....
"""
from azure.storage.blob import BlobServiceClient  # , BlobClient, ContainerClient
import uuid
import pandas
import requests
# import sys
from .._utils._constants import ACCOUNT, api_prefix
from .._utils._utils import ApiInputs


# class Platform:
class Queue:
    """ """
    @staticmethod
    def get_next_messages(account: ACCOUNT, container: str, queue_name: str, message_count: int = 1):
        """Retrieve next message(s).

        Parameters
        ----------
        account : ACCOUNT
            Azure account
        container : str
            Queue container.
        queue_name : str
            Queue name.
        message_count : int
            Message count to retrieve (Default value = 1).

        Returns
        -------

        """
        pass

    @staticmethod
    def send_message(account: ACCOUNT, container, queue_name, messages: list = None):
        """Send message

        Parameters
        ----------
        account : ACCOUNT
            Azure account.
        container : str
            Queue container.
        queue_name : str
            Queue name.
        messages : list, default = None
            Message (Default value = None).

        Returns
        -------

        """
        if messages is None:
            messages = []

        pass


class Blob:
    """ """
    @staticmethod
    def list(api_inputs: ApiInputs, account: ACCOUNT, container: str, prefix: str = None):
        """Retrieve list of blobs.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize() function.
        account : ACCOUNT
            Azure account.
        container : str
            Blob container.
        prefix : str, default=None
            Prefix (Default value = None).

        Returns
        -------

        """
        con_string = _get_connection_string(api_inputs, account)

        if prefix is None:
            prefix = ''

        blob_service_client = BlobServiceClient.from_connection_string(con_string)
        container_client = blob_service_client.get_container_client(container)
        blob_list = container_client.list_blobs(name_starts_with=prefix)
        for blob in blob_list:
            print(blob.name + ' - ' + str(blob.last_modified))
        return True

    @staticmethod
    def download(api_inputs: ApiInputs, account: ACCOUNT, container: str, blob_name: str):
        """

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize() function.
        account : ACCOUNT
            Azure account
        container : str
            Blob container.
        blob_name : str
            Blob name.

        Returns
        -------

        """
        con_string = _get_connection_string(api_inputs, account)
        blob_service_client = BlobServiceClient.from_connection_string(con_string)
        container_client = blob_service_client.get_container_client(container)
        print("Start Downloading")
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    @staticmethod
    def upload(api_inputs: ApiInputs, data_frame: pandas.DataFrame, name: str, api_project_id, is_timeseries: bool,
               account: ACCOUNT = 'SwitchStorage',  batch_id: uuid.UUID = ''):
        """Upload data to blob.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize() function.
        account: ACCOUNT
            Blob account data will be uploaded to.
        data_frame : pandas.DataFrame
            Dataframe containing the data to be uploaded to blob.
        name : str
            Name.
        api_project_id : uuid.UUID
            ApiProjectID of the portfolio data is being uploaded for.
        is_timeseries : bool
            Define whether the data being uploaded is timeseries data or not.
        batch_id : str, default = ''
            Batch ID (Default value = '').

        Returns
        -------

        """
        chunk_size = 1000000

        con_string = _get_connection_string(api_inputs, account)
        blob_service_client = BlobServiceClient.from_connection_string(con_string)
        container_client = blob_service_client.get_container_client("data-ingestion-adx")

        list_chunked_df = [data_frame[count:count + chunk_size] for count in
                           range(0, data_frame.shape[0], chunk_size)]
        upload_path = "to-ingest/" + str(uuid.uuid1()) + "/" + name + "/"

        item_counter = 0
        for current_data_frame in list_chunked_df:
            item_counter += 1
            blob_name = upload_path + str(item_counter) + ".csv"
            print("         Uploading ... " + blob_name)
            blob_client = container_client.get_blob_client(blob_name)
            data_csv = bytes(current_data_frame.to_csv(line_terminator='\r\n', index=False, header=False),
                             encoding='utf-8')
            blob_client.upload_blob(data_csv, blob_type="BlockBlob", overwrite=True)

        return upload_path, item_counter


def _get_connection_string(api_inputs: ApiInputs, account: ACCOUNT = 'SwitchStorage'):
    """Get connection string

    Parameters
    ----------
    api_inputs : ApiInputs
            Object returned by initialize() function.
    account : ACCOUNT, default = 'SwitchStorage'
         (Default value = 'SwitchStorage')

    Returns
    -------

    """

    headers = {
        'x-functions-key': api_inputs.api_key,
        'Content-Type': 'application/json; charset=utf-8',
        'user-key': api_inputs.user_id
    }

    url = api_prefix + 'Connections'
    response = requests.request("GET", url, timeout=20, headers=headers)

    blob_accounts = response.json()

    if account == 'SwitchStorage':
        return blob_accounts[account]
    elif account == 'SwitchContainer':
        return blob_accounts[account]
    elif account == 'Argus':
        return blob_accounts[account]


def _get_structure(df):
    """Get dataframe structure

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------

    """

    a = df.dtypes
    a = pandas.Series(a)
    a = a.reset_index().rename(columns={0: 'dtype'})
    a['dtype'] = a['dtype'].astype('str')
    a.set_index('index', inplace=True)
    a = a.to_dict()
    return a['dtype']
