import rhino3dm as rhino
from gh_concept import hs, hops
from gh_concept.concept import (model as concept_model,
                                geometry as concept_geo,
                                add_structure as concept_add_struct)


@hops.component(
    "/add_point_spring",
    name="Concept Add Point Spring",
    nickname="add point spring",
    description="Adds point springs to the specified RAM Concept model.",
    icon="",
    inputs=[
        hs.HopsBoolean("Enable push?", "Push?",
                       "Push to RAM Concept model",
                       hs.HopsParamAccess.ITEM,
                       default=False),
        hs.HopsString("Concept model", "Model",
                      "File path of RAM Concept model",
                      hs.HopsParamAccess.ITEM),
        hs.HopsPoint("Spring location", "Location",
                     "Point location of point spring as list",
                     hs.HopsParamAccess.LIST),
        hs.HopsString("Support name", "Name",
                      "Name of support as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Support elevation", "Elevation",
                      "Elevation of the point spring relative to soffit",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("R-axis stiffness", "kFr",
                      "Spring stiffness in r-axis as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("S-axis stiffness", "kFs",
                      "Spring stiffness in s-axis as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Z-axis stiffness", "kFz",
                      "Spring stiffness in z-axis as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("R-axis rotational stiffness", "kMr",
                      "Rotational spring stiffness about r-axis as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("S-axis rotational stiffness", "kMs",
                      "Rotational spring stiffness about s-axis as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Support axis angle", "AxisAngle",
                      "Axis rotation of support axis as list",
                      hs.HopsParamAccess.LIST, True),
    ],
    outputs=[hs.HopsString("Push log", "Log",
                           "Log of Concept push"),
             ])
def add_point_spring(push: bool, model_file: str, location: list[rhino.Point3d], name: list[str],
                     elevation: list[float],
                     kFr: list[float], kFs: list[float], kFz: list[float], kMr: list[float], kMs: list[float],
                     angle: list[float]):
    if push:
        logger = []
        # verify valid point spring locations and translate to Concept Points
        valid_springs = []
        for i, support in enumerate(location):
            valid_springs.append({"location": concept_geo.point_from_rhino_point(support),
                                  "name": name[i] if i < len(name) else None,
                                  "elevation": elevation[i] if i < len(elevation) else None,
                                  "kFr": kFr[i] if i < len(kFr) else None,
                                  "kFs": kFs[i] if i < len(kFs) else None,
                                  "kFz": kFz[i] if i < len(kFz) else None,
                                  "kMr": kMr[i] if i < len(kMr) else None,
                                  "kMs": kMs[i] if i < len(kMs) else None,
                                  "angle": angle[i] if i < len(angle) else None,
                                  })
        if valid_springs:
            # open Concept model and extract set api units and signs
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add point springs
            for spring in valid_springs:
                concept_add_struct.add_point_spring(model, **spring)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_springs)} points springs pushed.")
        else:
            logger.append(f"No valid point springs provided.")
        return logger
