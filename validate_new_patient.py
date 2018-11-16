from builtins import ValueError
import logging

logging.basicConfig(filename="HR_sent_Logging.txt",
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


def check_if_new(all_id, my_id):
    """Check if patient exists

        Args:
            all_id (list): integers of current ids in db
            my_id (int): id of current patient

        Returns:
            b (int): value of 1 if new patient

        Raises:
            ValueError: if patient id already exists
    """
    b = 1
    for item in all_id:
        if item == my_id:
            logging.warning("ALREADY EXISTS")
            b = 3
            raise ValueError("Patient already exists")

    if b == 1:
        return b
