# RAM Concept API imports
from ram_concept.concept import Concept
from ram_concept.model import Model
from datetime import datetime
import os


def open_concept_model(file_path) -> tuple[Concept, Model]:
    local_folder = os.path.dirname(file_path)
    concept_log = os.path.join(local_folder, f"ConceptAPI_{datetime.now().strftime('%Y%m%dT%H%M')}.log")
    concept = Concept.start_concept(headless=False, log_file_path=concept_log)
    model = concept.open_file(file_path)
    return concept, model


def set_api_units_signs(model: Model) -> tuple[str, str]:
    # store file units and set standard
    file_units = model.units.get_units()
    model.units.set_SI_API_units()
    # store file signs and set standard
    file_signs = model.signs.get_signs()
    model.signs.set_positive_signs()
    return file_units, file_signs


def restore_file_units_signs(model: Model, file_units, file_signs):
    model.units.set_units(file_units)
    model.signs.set_signs(file_signs)


def save_close_concept(concept: Concept, model: Model, file_path):
    model.save_file(file_path)
    concept.shut_down()
