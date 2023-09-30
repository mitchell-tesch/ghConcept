from gh_concept import hs, hops
import rhino3dm as rhino
from gh_concept.rhino import geometry as rhino_geo
from gh_concept.concept import (model as concept_model,
                                geometry as concept_geo,
                                add_structure as concept_add_struct)


@hops.component(
    "/add_slab",
    name="Concept Add Slab",
    nickname="add slab",
    description="Adds slab areas to the specified RAM Concept model.",
    icon="images/add_slab_area.png",
    inputs=[
        hs.HopsBoolean("Enable push?", "Push?",
                       "Push to RAM Concept model",
                       hs.HopsParamAccess.ITEM,
                       default=False),
        hs.HopsString("Concept model", "Model",
                      "File path of RAM Concept model",
                      hs.HopsParamAccess.ITEM),
        hs.HopsCurve("Slab boundary", "Boundary",
                     "Polyline Boundary of slab as list",
                     hs.HopsParamAccess.LIST),
        hs.HopsString("Slab name", "Name",
                      "Name of slab area as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Slab thickness", "Thickness",
                      "Slab thickness as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsNumber("Top of concrete", "TopLevel",
                      "Relative top of concrete as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsInteger("Priority", "Priority",
                       "Priority of slab as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsString("Analysis behaviour", "Behaviour",
                      "Slab analysis behaviour as list\n\
                          (custom, no-torsion two-way slab, one-way slab, two-way slab)",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsString("Concrete material name", "Concrete",
                      "Concept concrete material name as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Axis angle", "AxisAngle",
                      "Axis rotation angle (deg) as list",
                      hs.HopsParamAccess.LIST, True),
        ],
    outputs=[hs.HopsString("Push log", "Log",
                           "Log of Concept push"),
             ])
def add_slab(push: bool, model_file: str, boundary: list[rhino.PolylineCurve], name: list[str], thickness: list[float],
             top_of_concrete: list[float], priority: list[int], behaviour: list[str], material: list[str],
             axis_angle: list[float]):
    if push:
        logger = []
        # verify valid areas and translate to Concept Polygons
        valid_areas = []
        for i, slab_boundary in enumerate(boundary):
            valid, log = rhino_geo.check_boundary_validity(slab_boundary, i)
            logger.extend(log)
            if valid:
                # store valid
                valid_areas.append({"polygon": concept_geo.polygon_from_polyline(slab_boundary),
                                    "name": name[i] if i < len(name) else None,
                                    "thickness": thickness[i] if i < len(thickness) else None,
                                    "top_of_concrete": top_of_concrete[i] if i < len(top_of_concrete) else None,
                                    "priority": priority[i] if i < len(priority) else None,
                                    "behaviour": behaviour[i] if i < len(behaviour) else None,
                                    "material": material[i] if i < len(material) else None,
                                    "axis_angle": axis_angle[i] if i < len(axis_angle) else None,
                                    })
        if valid_areas:
            # open Concept model and extract set api units and signs
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add polygons as slab areas
            for slab_area in valid_areas:
                concept_add_struct.add_slab_area(model, **slab_area)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_areas)} slab areas pushed.")
        else:
            logger.append(f"No valid slab areas provided.")
        return logger
