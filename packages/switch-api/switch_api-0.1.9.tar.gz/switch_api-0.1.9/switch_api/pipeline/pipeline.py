# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""Module defining the Task abstract base class which is inherited by the following specific task types:

- IntegrationTask
- AnalyticsTask
- LogicModuleTask
- QueueTask

Also includes the Automation class which contains helper functions.

---------------
IntegrationTask
---------------
Base class used to create integrations between the Switch Automation platform and other platforms, low-level services,
or hardware.

Examples include:
    - Pulling readings or other types of data from REST APIs
    - Protocol Translators which ingest data sent to the platform via email, ftp or direct upload within platform.

-------------
AnalyticsTask
-------------
Base class used to create specific analytics functionality which may leverage existing data from the platform. Each
task may add value to, or supplement, this data and write it back.

Examples include:
    - Anomaly Detection
    - Leaky Pipes
    - Peer Tracking

---------------
LogicModuleTask
---------------
Base class that handles the running, reprocessing and scheduling of the legacy logic modules in a way which enables
integration with other platform functionality.

---------
QueueTask
---------
Base class used to create data pipelines that are fed via a queue.

----------
Automation
----------
This class contains the helper methods used to register, deploy, and test the created tasks. Additional helper functions
 for retrieving details of existing tasks on the Switch Automation platform are also included in this module.

"""
import enum
import sys
import re
import pandas
import requests
import inspect
import uuid
import logging
import datetime
# import base64
# import asyncio
from typing import List
from abc import ABC, abstractmethod
from azure.servicebus import ServiceBusClient, ServiceBusReceiveMode  # , ServiceBusMessage
from .._utils._utils import _is_valid_regex, ApiInputs, generate_password  # , ValidatedSetterProperty
from .._utils._constants import api_prefix, argus_prefix, EXPECTED_DELIVERY, DEPLOY_TYPE, MAPPING_ENTITIES, QUEUE_NAME
from .._utils._platform import _get_connection_string

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s  %(name)s.%(funcName)s  %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')
consoleHandler.setFormatter(formatter)


# Base Definitions in Switch package
class Task(ABC):
    """
    An Abstract Base Class called Task.

    Attributes
    ----------
    id : uuid.UUID
        Unique identifier of the task. This is an abstract property that needs to be overwritten when sub-classing.
        A new unique identifier can be created using uuid.uuid4()
    description : str
        Brief description of the task
    mapping_entities : MAPPING_ENTITIES
        The type of entities being mapped. An example is:

        ``['Installations', 'Devices', 'Sensors']``
    author : str
        The author of the task.
    version : str
        The version of the task.

    """
    @property
    @abstractmethod
    def id(self) -> uuid.UUID:
        """Unique identifier of the task. Create a new unique identifier using uuid.uuid4() """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Brief description of the task"""
        pass

    @property
    @abstractmethod
    def mapping_entities(self) -> MAPPING_ENTITIES:
        """The type of entities being mapped."""
        pass

    @property
    @abstractmethod
    def author(self) -> str:
        """"The author of the task."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """The version of the task"""
        pass


class IntegrationTask(Task):
    """Integration Task

    This class is used to create integrations that post data to the Switch Automation platform.


    Only one of the following methods should be implemented per class, based on the type of integration required:

    - process_file()
    - process_stream()
    - process()

    """

    @abstractmethod
    def process_file(self, api_inputs: ApiInputs, file_path_to_process: str):
        """Method to be implemented if a file will be processed by the Integration Task.

        The method should contain all code used to cleanse, reformat & post the data contained in the file.

        Parameter
        _________
        api_inputs : ApiInputs
            object returned by call to initialize()
        file_path_to_process : str
            the file path

        """
        pass

    @abstractmethod
    def process_stream(self, api_inputs: ApiInputs, stream_to_process):
        """Method to be implemented if data received via stream

        The method should contain all code used to cleanse, reformat & post the data received via the stream.

        Parameters
        __________
        api_inputs: ApiInputs
            object returned by call to initialize()
        stream to process :
            details of the stream to be processed.
        """
        pass

    @abstractmethod
    def process(self, api_inputs: ApiInputs, integration_settings: dict):
        """Method to be implemented if data

        The method should contain all code used to cleanse, reformat & post the data pulled via the integration.

        Parameters
        __________
        api_inputs: ApiInputs
            object returned by call to initialize()
        integration_settings : dict
            Any settings required to be passed to the integration to run. For example, username & password, api key,
            auth token, etc.

        """
        pass


class QueueTask(Task):
    """Integration Task

    This class is used to create integrations that post data to the Switch Automation platform using a Queue as the
    data source.

    Only one of the following methods should be implemented per class, based on the type of integration required:

    - process_file()
    - process_stream()
    - process()

    """

    @property
    @abstractmethod
    def queue_name(self) -> str:
        """The name of the queue to receive Data .. Name will actually be constructed as {ApiProjectId}_{queue_name} """
        pass

    @property
    @abstractmethod
    def maximum_message_count_per_call(self) -> int:
        """ The maximum amount of messages which should be passed to the process_queue at any one time 
            set to zero to consume all
        """
        pass

    @abstractmethod
    def start(self, api_inputs: ApiInputs):
        """Method to be implemented if a file will be processed by the QueueTask Task.    
        This will run once at the start of the processing and should contain     

        """
        pass

    @abstractmethod
    def process_queue(self, api_inputs: ApiInputs, messages: List):
        """Method to be implemented if a file will be processed by the QueueTask Task.

        The method should contain all code used to consume the messages

        Parameter
        _________
        api_inputs : ApiInputs
            object returned by call to initialize()
        messages:List)
            list of serialzed json strings which have been consumeed from the queue

        """
        pass


class AnalyticsTask(Task):

    @abstractmethod
    def start(self, api_inputs: ApiInputs, analytics_settings: dict):
        """Start.

        The method should contain all code used by the task.

        Parameters
        __________
        api_inputs : ApiInputs
            the object returned by call to initialize()
        analytics_settings : dict
            any setting required by the AnalyticsTask

        """
        pass


class LogicModuleTask(Task):

    @abstractmethod
    def start(self, start_date_time: datetime.date, end_date_time: datetime.date, installation_id: uuid.UUID,
              share_tag_group: str, share_tags: list):
        pass

    # Needs to be implemented into the deploy_on_timer


class RunAt(enum.Enum):
    """ """
    Every15Minutes = 1
    Every1Hour = 3
    EveryDay = 4
    EveryWeek = 5


class Automation:
    """Automation class defines the methods used to register and deploy tasks. """

    @staticmethod
    def run_queue_task(task: QueueTask, api_inputs: ApiInputs, consume_all_messages: bool = False):
        """Runs a Queue Task when in Development Mode
        
        The Queue Name should ideally be a testing Queue as messages will be consumed

        Parameters
        ----------
        task : QueueTask
            The custom QueueTask instance created by the user.
        api_inputs : ApiInputs
            Object returned by initialize() function.
        consume_all_messages : bool, default=False
            Consume all messages as they are read.

        Returns
        -------
        bool
            indicating whether the call was successful

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return False

        if not issubclass(type(task), QueueTask):
            logger.error(
                "Driver must be an implementation of the QueueTask (Task).")
            return False

        print()
        print("Switch.Automation: Running Queue for  " + type(task).__name__ + ' (' + str(task.id) +
              ') using Queue Name ' + task.queue_name)
        
        task.start(api_inputs)

        message_count = 0
        with ServiceBusClient.from_connection_string(_get_connection_string(
                api_inputs=api_inputs, account="Argus")) as client:
            with client.get_queue_receiver(task.queue_name,
                                           receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE) as receiver:
                while True:
                    messages = []
                    received_message_array = receiver.receive_messages(
                        max_message_count=task.maximum_message_count_per_call, max_wait_time=2)
                    for message in received_message_array:
                        messages.append(str(message))
                        message_count += 1

                    if len(received_message_array) == 0:
                        break

                    task.process_queue(api_inputs, messages)
                    
                    if consume_all_messages == False:
                        break
        print(f"Switch.Automation: Total messages consumed:  {str(message_count)} ")

    @staticmethod
    def reserve_instance(task: Task, api_inputs: ApiInputs, data_feed_id: uuid.UUID, minutes_to_reserve: int = 10):
        """Reserve a testing instance.

        Reserves a testing instance for the `driver`.

        Parameters
        ----------
        task : Task
            The custom Driver class created by the user.
        api_inputs : ApiInputs
            Object returned by initialize() function.
        data_feed_id : uuid.UUID
            The unique identifier of the data feed being tested.
        minutes_to_reserve : int, default = 10
                The duration in minutes that the testing instance will be reserved for (Default value = 10).

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the details of the reserved testing instance.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        print("Switch.Automation: Reserving Testing Instance for " + type(
            task).__name__ + ' (' + str(task.id) + ') on Data Feed Id (' + str(data_feed_id) + ')')
        print()

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        url = argus_prefix + "ReserveInstance/" + data_feed_id + "/" + str(minutes_to_reserve)

        response = requests.request("GET", url, timeout=20, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text, typ="Series")
        return df

    @staticmethod
    def register_task(task):
        """Register the task.

        Registers the task that was defined.

        Parameters
        ----------
        task : Task
            An instance of the custom class created from the Abstract Base Class `Task` or its abstract sub-classes:
            `IntegrationTask`, `AnalyticsTask`, `LogicModuleTask`.

        Returns
        -------
        pandas.DataFrame

        """

        if not issubclass(type(task), Task):
            logger.error(
                "Driver must be an implementation of the Abstract Base Class (Task).")
            return False

        base_class = ''
        if issubclass(type(task), IntegrationTask):
            base_class = 'IntegrationTask'
        elif issubclass(type(task), LogicModuleTask):
            base_class = 'LogicModuleTask'
        elif issubclass(type(task), AnalyticsTask):
            base_class = 'AnalyticsTask'

        if base_class == '':
            logger.error(
                'Task must be an implementation of the Task Subclasses of AnalyticsTask, IntegrationTask or '
                'LogicModule.')
            return {}, pandas.DataFrame()

        print("Switch.Automation: Registering " + type(
            task).__name__ + ' (' + str(task.id) + ')' + ' to the Switch Driver Library: ')
        print()

        json_payload_verify = {
            "driverId": task.id,
            "name": type(task).__name__
        }

        url = api_prefix + "Automation/VerifyRegisterDriver"
        response = requests.post(url, json=json_payload_verify)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif response.text == "Failed":
            logger.error("This Driver Guid is already associated with a Driver with a Different Name.")
            return response_status, pandas.DataFrame()

        json_payload = {
            "driverId": task.id,
            "name": type(task).__name__,
            "specification": task.description,
            "mappingEntities": task.mapping_entities,
            "scriptCode": Automation.get_task_code(task),
            "baseClass": base_class
        }

        url = api_prefix + "Automation/RegisterDriver"

        response = requests.post(url, json=json_payload)
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

    @staticmethod
    def list_tasks(api_inputs: ApiInputs, search_name_pattern: str = '*'):
        """Get a list of the deployed tasks.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize() function.
        search_name_pattern : str, optional
            A pattern that should be used as a filter when retrieving the list of deployed drivers
            (Default value = '*').

        Returns
        -------
        pandas.DataFrame

        """
        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        url = api_prefix + "Automation/ListDrivers/" + search_name_pattern

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
        df = df.drop(columns=['driverId'])
        return df

    @staticmethod
    def deploy_as_email_data_feed(task, api_inputs: ApiInputs, email_address_domain='SwitchAutomation.com',
                                  email_subject_regex='', queue_name: QUEUE_NAME = "task",
                                  expected_delivery: EXPECTED_DELIVERY = "Daily"):
        """Deploy task as an email data feed.

        Deploys the created `task` as an email data feed. This allows the driver to ingest data sent via email. The
        data must be sent to data@switchautomation.com to be processed. If it is sent to another email address, the task
        will not be run.

        Parameters
        ----------
        task : Task
            The custom driver class created from the Abstract Base Class `Driver`
        api_inputs : ApiInputs
            Object returned by initialize() function.
        email_address_domain : str, default='switchautomation.com'
            The email domain, without the @ symbol, of the sender (Default value = 'SwitchAutomation.com').
        email_subject_regex : str
            Regex expression used to parse the email subject line to determine which driver the received file will
            be processed by (Default value = '').
        queue_name : QUEUE_NAME
            The name of queue.
        expected_delivery : EXPECTED_DELIVERY
            The expected delivery frequency (Default value = "Daily").

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the details of the deployed email data feed.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        logger.info('Deploy %s (%s) as a data feed for ApiProjectID: %s', type(task).__name__, str(task.id),
                    api_inputs.api_project_id)

        if not _is_valid_regex(email_subject_regex):
            # print("Automation.deploy_as_email_data_feed: " + email_subject_regex + "is not a valid Regular "
            #                                                                        "Expression.")
            # return False
            logger.error("%s is not valid regex.", email_subject_regex)
            return pandas.DataFrame()

        if email_address_domain == "switchautomation.com":
            # print("Automation.deploy_as_email_data_feed: Emails can only be received from the " + email_address_domain
            #       + " domain.")
            logger.info("Emails can only be received from the %s domain.", email_address_domain)

        if "@" in email_address_domain:
            # print(
            #     "Automation.deploy_as_email_data_feed: Do not include the @ in the email_address_domain parameter.")
            # return False
            logger.error("Do not include the @ in the email_address_domain parameter. ")
            return pandas.DataFrame()

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        inbox_container = "data-exchange"
        payload = {
            "driverId": task.id,
            "name": 'Feed Settings for ' + type(task).__name__,
            "feedType": ",".join(task.mapping_entities),
            "expectedDelivery": expected_delivery,
            "sourceType": "email",
            "queueName": queue_name,
            "email": {
                "emailAddressDomain": email_address_domain,
                "emailSubjectRegex": email_subject_regex,
                "container": inbox_container
            }
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/DeployTask"

        response = requests.post(url, json=payload, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text, typ='Series')
        return df

        # Create Data Feed for Specified ApiProject Id
        # print the Data Centre and ApiProject Name

    @staticmethod
    def deploy_as_ftp_data_feed(task, api_inputs: ApiInputs, ftp_user_name, ftp_password,
                                queue_name: QUEUE_NAME = "task", expected_delivery: EXPECTED_DELIVERY = "15min"):
        """Deploy the custom driver as an FTP data feed

        Deploys the custom driver to receive data via an FTP data feed. Sets the `ftp_user_name` & `ftp_password` and
        the `expected_delivery` of the file.

        Parameters
        ----------
        task : Task
            The custom driver class created from the Abstract Base Class 'Driver'
        api_inputs : ApiInputs
            Object returned by the initialize() function.
        ftp_user_name : str
            The user_name to be used by the ftp service to authenticate delivery of the data feed.
        ftp_password : str
            The password to be used by the ftp service for the given `ftp_user_name` to authenticate delivery of the
            data feed.
        queue_name : QUEUE_NAME, default = 'task'
            The queue name.
        expected_delivery : EXPECTED_DELIVERY, default = '15min'
            The expected delivery frequency of the data (Default value = "15Minutes").

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the details of the deployed ftp data feed.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        logger.info('Deploy %s (%s) as a data feed for ApiProjectID: %s', type(task).__name__, str(task.id),
                    api_inputs.api_project_id)

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        inbox_container = "data-exchange"
        payload = {
            "driverId": task.id,
            "name": 'Feed Settings for ' + type(task).__name__,
            "feedType": ",".join(task.mapping_entities),
            "expectedDelivery": expected_delivery,
            "sourceType": "ftp",
            "queueName": queue_name,
            "ftp": {
                "ftpUserName": ftp_user_name,
                "ftpPassword": ftp_password,
                "container": inbox_container
            }
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/DeployTask"

        response = requests.post(url, json=payload, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text, typ='Series')
        return df

    @staticmethod
    def deploy_as_upload_data_feed(task, api_inputs: ApiInputs, queue_name: QUEUE_NAME = "task",
                                   expected_delivery: EXPECTED_DELIVERY = "15min"):
        """Deploy the custom driver as a Upload Datafeed ie Customer sends data via a Rest ENd Point

        Parameters
        ----------
        task : Task
            The custom driver class created from the Abstract Base Class 'Driver'
        api_inputs : ApiInputs
            Object returned by the initialize() function.
        queue_name : QUEUE_NAME, default = 'task'
            The queue name.
        expected_delivery : EXPECTED_DELIVERY, default = '15min'
            The expected delivery frequency of the data (Default value = "15Minutes").

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the details of the deployed ftp data feed.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        logger.info('Deploy %s (%s) as a data feed for ApiProjectID: %s', type(task).__name__, str(task.id),
                    api_inputs.api_project_id)

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        # inbox_container = "data-exchange"
        payload = {
            "driverId": task.id,
            "name": 'Feed Settings for ' + type(task).__name__,
            "feedType": ",".join(task.mapping_entities),
            "expectedDelivery": expected_delivery,
            "sourceType": "upload",
            "queueName": queue_name,
            "upload": {
                "placeholder": ""
            },
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/DeployTask"

        response = requests.post(url, json=payload, headers=headers)
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

    @staticmethod
    def deploy_on_timer(task, api_inputs: ApiInputs, cron_schedule, queue_name: QUEUE_NAME = "task",
                        expected_delivery: EXPECTED_DELIVERY = "15min", settings: dict = None):
        """Deploy driver to run on timer.

        Parameters
        ----------
        task : Task
            The custom driver class created from the Abstract Base Class `Driver`.
        api_inputs : ApiInputs
            Object returned by initialize.initialize() function
        cron_schedule :
            Cron object containing the required schedule for the driver to be run.
        queue_name : QUEUE_NAME, default = 'task'
            The queue name.
        expected_delivery : EXPECTED_DELIVERY
            The expected delivery frequency (Default value = "15min").
        settings : dict, Optional
                List of settings used to deploy the driver. For example, may contain the user_name and password
                required to authenticate calls to a third-party API (Default value = None).

        Returns
        -------
        str
            A string containing the response text.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        if len(cron_schedule.split(' ')) != 7:
            logger.error("cron_schedule parameter must be in the format * * * * * *")
            return pandas.DataFrame()

        # TODO - discuss whether this is required since we added the Literal EXPECTED_DELIVERY
        expected_deliveries = re.findall(r'[A-Za-z]+|\d+', expected_delivery)
        if len(expected_deliveries) != 2 or expected_deliveries[0].isnumeric() is not True:
            logger.error("Run At parameter must take the form of a number followed by a time type. ")
            return pandas.DataFrame()

        time_type = expected_deliveries[1].lower()[:3]
        if time_type != 'min' and time_type != 'hour' and time_type != 'day':
            # print("Automation.deploy_on_timer: Expected Delivery Time Type must start with min, hour, day")
            logger.error("The expected_delivery time type must start with one of: min, hour, day. ")
            # return False
            return pandas.DataFrame()

        logger.info('Deploy %s (%s) on timer for ApiProjectID: %s and schedule: %s.', type(task).__name__,
                    str(task.id), api_inputs.api_project_id, cron_schedule)
        logger.info('Feed Type is %s', str(task.mapping_entities))
        logger.info('Settings to be passed tothe driver on start are: %s', str(settings))

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        payload = {
            "driverId": task.id,
            "name": 'Timer Settings for ' + type(task).__name__,
            "feedType": ",".join(task.mapping_entities),
            "expectedDelivery": expected_delivery,
            "sourceType": "BlobFolder",
            "queueName": queue_name,
            "timer": {
                "cronSchedule": cron_schedule
            },
            "settings": settings
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/DeployTask"

        response = requests.post(url, json=payload, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text, typ='Series')
        return df

    @staticmethod
    def cancel_deploy(task, api_inputs: ApiInputs, deploy_type: DEPLOY_TYPE):
        """Deploy driver to run on timer.

        Parameters
        ----------
        task : Task
            The custom task class created from the Abstract Base Class `Task`.
        api_inputs : ApiInputs
            Object returned by initialize.initialize() function
        deploy_type : DEPLOY_TYPE
            One of the deploy types defined by this lteral


        Returns
        -------
        str
            A string containing the response text.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        logger.info('Cancel deploy %s (%s) on timer for ApiProjectID: %s', type(task).__name__,
                    str(task.id), api_inputs.api_project_id)
        logger.info('Feed Type is %s', str(task.mapping_entities))

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        # payload = {}

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/CancelTask/" + \
            deploy_type + "/" + task.id
        print(url)
        response = requests.get(url, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                         response.reason)
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s', response.request.__dict__)
            return response_status, pandas.DataFrame()

        df = pandas.read_json(response.text, typ='Series')
        return df

    @staticmethod
    def list_deployments(api_inputs: ApiInputs, search_name_pattern='*'):
        """Retrieve list of deployed drivers.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize.initialize() function
        search_name_pattern : str
                A pattern that should be used as a filter when retrieving the list of deployed drivers
                (Default value = '*').

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the drivers deployed for the given ApiProjectID that match the `search_name_pattern`.

        """

        if api_inputs.datacentre == '' or api_inputs.api_key == '':
            logger.error("You must call initialize() before using API.")
            return pandas.DataFrame()

        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + "/Automation/ListDeployments/" + \
            search_name_pattern

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

    @staticmethod
    def list_data_feed_history(api_inputs: ApiInputs, data_feed_id, top_count=10):
        """Retrieve data feed history

        Retrieves the `top_count` records for the given `data_feed_id`.

        Parameters
        ----------
        api_inputs : ApiInputs
            Object returned by initialize.initialize() function
        data_feed_id : uuid.UUID
                The unique identifier for the data feed that history should be retrieved for.
        top_count : int, default = 10
                The top record count to be retrieved. (Default value = 10).

        Returns
        -------
        df : pandas.DataFrame
            Dataframe containing the `top_count` history records for the given `data_feed_id`.

        """
        headers = {
            'x-functions-key': api_inputs.api_key,
            'Content-Type': 'application/json; charset=utf-8',
            'user-key': api_inputs.user_id
        }

        url = api_prefix + api_inputs.datacentre + "/" + api_inputs.api_project_id + \
            "/Automation/ListDataFeedsHistory/" + data_feed_id + "/" + str(top_count)
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

    @staticmethod
    def get_task_code(task):
        """

        Parameters
        ----------
        task : Task
            The custom driver class created from the Abstract Base Class `Task`.

        Returns
        -------
        driver_code : str
            The code used to create the `task`

        """
        task_type = type(task)
        task_code = ''
        parent_module = inspect.getmodule(task_type)
        for codeLine in inspect.getsource(parent_module).split('\n'):
            if codeLine.startswith('import ') or codeLine.startswith('from '):
                task_code += codeLine + '\n'

        task_code += '\n'
        task_code += inspect.getsource(task_type)
        task_code += ''
        task_code += 'task = ' + task_type.__name__ + '()'

        return task_code
