# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
from typing import Tuple
from autoreduce_db.reduction_viewer.models import ReductionRun, Status

from django.urls.base import reverse
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait

from autoreduce_utils.clients.connection_exception import ConnectionException
from autoreduce_utils.clients.queue_client import QueueClient

from autoreduce_qp.model.database import access as db
from autoreduce_qp.queue_processor.queue_listener import QueueListener, setup_connection
from autoreduce_qp.systemtests.utils.data_archive import DataArchive

# pylint:disable=no-member


def find_run_in_database(test):
    """
    Find a ReductionRun record in the database
    This includes a timeout to wait for several seconds to ensure the database has received
    the record in question
    :return: The resulting record
    """
    instrument = db.get_instrument(test.instrument_name)
    if isinstance(test.run_number, list):
        args = {"run_number__in": test.run_number}

    else:
        args = {"run_number": test.run_number}
    return instrument.reduction_runs.filter(**args)


def submit_and_wait_for_result(test, expected_runs=1):
    """
    Submit after a reset button has been clicked. Then waits until the queue listener has finished processing.

    Sticks the submission in a loop in case the first time doesn't work. The reason
    it may not work is that resetting actually swaps out the whole form using JS, which
    replaces ALL the elements and triggers a bunch of DOM re-renders/updates, and that isn't fast.
    """
    test.listener._processing = True  # pylint:disable=protected-access
    expected_url = reverse("run_confirmation", kwargs={"instrument": test.instrument_name})

    def submit_successful(driver) -> bool:
        try:
            test.page.submit_button.click()
        except ElementClickInterceptedException:
            pass
        # the submit is successful if the URL has changed
        return expected_url in driver.current_url

    WebDriverWait(test.driver, 30).until(submit_successful)
    if expected_runs == 1:
        WebDriverWait(test.driver, 30).until(lambda _: not test.listener.is_processing_message())
    else:
        num_current_runs = ReductionRun.objects.filter(status=Status.get_completed()).count()
        WebDriverWait(test.driver, 30).until(lambda _: ReductionRun.objects.filter(status=Status.get_completed()).count(
        ) == num_current_runs + expected_runs)

    return find_run_in_database(test)


def setup_external_services(instrument_name: str, start_year: int,
                            end_year: int) -> Tuple[DataArchive, QueueClient, QueueListener]:
    """
    Sets up a DataArchive complete with scripts, database client and queue client and listeners and returns their
    objects in a tuple
    :param instrument_name: Name of the instrument
    :param start_year: Start year for the archive
    :param end_year: End year for the archive
    :return: Tuple of external objects needed.
    """
    data_archive = DataArchive([instrument_name], start_year, end_year)
    data_archive.create()
    try:
        queue_client, listener = setup_connection()
    except ConnectionException as err:
        raise RuntimeError("Could not connect to ActiveMQ - check your credentials. If running locally check that "
                           "ActiveMQ is running and started by `python setup.py start`") from err

    return data_archive, queue_client, listener
