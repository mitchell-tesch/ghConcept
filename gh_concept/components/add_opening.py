from gh_concept import hs, hops
import rhino3dm as rhino
from gh_concept.rhino import geometry as rhino_geo
from gh_concept.concept import (model as concept_model,
                                geometry as concept_geo,
                                add_structure as concept_add_struct)


@hops.component(
    "/add_opening",
    name="Concept Add Opening",
    nickname="add opening",
    description="Adds slab openings to the specified RAM Concept model.",
    icon="images/add_slab_area.png",
    inputs=[
        hs.HopsBoolean("Enable push?", "Push?",
                       "Push to RAM Concept model",
                       hs.HopsParamAccess.ITEM,
                       default=False),
        hs.HopsString("Concept model", "Model",
                      "File path of RAM Concept model",
                      hs.HopsParamAccess.ITEM),
        hs.HopsCurve("Opening boundary", "Boundary",
                     "Polyline boundary of opening as list",
                     hs.HopsParamAccess.LIST),
        hs.HopsString("Opening name", "Name",
                      "Name of slab opening as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsInteger("Priority", "Priority",
                       "Priority of slab as list",
                       hs.HopsParamAccess.LIST),
        ],
    outputs=[hs.HopsString("Push log", "Log",
                           "Log of Concept push"),
             ])
def add_slab_opening(push: bool, model_file: str, boundary: list[rhino.PolylineCurve], name: list[str],
                     priority: list[int]):
    if push:
        logger = []
        # verify valid areas and translate to Concept Polygons
        valid_openings = []
        for i, open_boundary in enumerate(boundary):
            valid, log = rhino_geo.check_boundary_validity(open_boundary, i)
            logger.extend(log)
            if valid:
                # store valid
                valid_openings.append({"polygon": concept_geo.polygon_from_polyline(open_boundary),
                                       "name": name[i] if i < len(name) else None,
                                       "priority": priority[i] if i < len(priority) else None,
                                       })
        if valid_openings:
            # open Concept model and extract set api units and sings
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add polygons as slab openings
            for open_area in valid_openings:
                concept_add_struct.add_slab_opening(model, **open_area)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_openings)} slab openings pushed.")
        else:
            logger.append(f"No valid slab openings provided.")
        return logger
