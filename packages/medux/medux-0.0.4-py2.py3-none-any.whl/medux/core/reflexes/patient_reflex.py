import logging

from sockpuppet.reflex import Reflex

from ..models.patient import Firstname

logger = logging.getLogger(__file__)


def validate_firstname(name: str) -> bool:
    try:
        Firstname.objects.get(name=name)
    except Firstname.DoesNotExist:
        # TODO: try to add it? Suggestion?
        logger.info(f"First name {name} not found in Firstnames list.")
    finally:
        # TODO validate first name
        if name:
            return True
        else:
            return False


class PatientAddReflex(Reflex):
    def update(self):
        pass

    def update_firstname(self):
        first_name = self.params["patient_firstname"]
        if validate_firstname(first_name):
            self.element.attributes["class"] = "is_valid"
        self.first_name = first_name
