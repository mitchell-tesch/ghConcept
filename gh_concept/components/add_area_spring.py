from gh_concept import hs, hops
import rhino3dm as rhino
from gh_concept.rhino import geometry as rhino_geo
from gh_concept.concept import (model as concept_model,
                                geometry as concept_geo,
                                add_structure as concept_add_struct)


@hops.component(
    "/add_area_spring",
    name="Concept Add Area Spring",
    nickname="add area spring",
    description="Adds area springs to the specified RAM Concept model.",
    icon="",
    inputs=[
        hs.HopsBoolean("Enable push?", "Push?",
                       "Push to RAM Concept model",
                       hs.HopsParamAccess.ITEM,
                       default=False),
        hs.HopsString("Concept model", "Model",
                      "File path of RAM Concept model",
                      hs.HopsParamAccess.ITEM),
        hs.HopsCurve("Area boundary", "Boundary",
                     "Polyline boundary of area spring as list",
                     hs.HopsParamAccess.LIST),
        hs.HopsString("Area name", "Name",
                      "Name of area spring as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Spring elevation", "Elevation",
                      "Elevation of the area spring relative to soffit",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 1 R-axis stiffness", "Point1_kFr",
                      "Spring stiffness in r-axis at Point 1 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 1 S-axis stiffness", "Point1_kFs",
                      "Spring stiffness in s-axis at Point 1 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 1 Z-axis stiffness", "Point1_kFz",
                      "Spring stiffness in z-axis at Point 1 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 1 R-axis rotational stiffness", "Point1_kMr",
                      "Rotational spring stiffness about r-axis at Point 1 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 1 S-axis rotational stiffness", "Point1_kMs",
                      "Rotational spring stiffness about s-axis at Point 1 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 2 R-axis stiffness", "Point 2_kFr",
                      "Spring stiffness in r-axis at Point 2 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 2 S-axis stiffness", "Point 2_kFs",
                      "Spring stiffness in s-axis at Point 2 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 2 Z-axis stiffness", "Point 2_kFz",
                      "Spring stiffness in z-axis at Point 2 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 2 R-axis rotational stiffness", "Point 2_kMr",
                      "Rotational spring stiffness about r-axis at Point 2 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 2 S-axis rotational stiffness", "Point 2_kMs",
                      "Rotational spring stiffness about s-axis at Point 2 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 3 R-axis stiffness", "Point 3_kFr",
                      "Spring stiffness in r-axis at Point 3 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 3 S-axis stiffness", "Point 3_kFs",
                      "Spring stiffness in s-axis at Point 3 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 3 Z-axis stiffness", "Point 3_kFz",
                      "Spring stiffness in z-axis at Point 3 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 3 R-axis rotational stiffness", "Point 3_kMr",
                      "Rotational spring stiffness about r-axis at Point 3 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 3 S-axis rotational stiffness", "Point 3_kMs",
                      "Rotational spring stiffness about s-axis at Point 3 as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Spring axis angle", "AxisAngle",
                      "Axis rotation of spring axis as list",
                      hs.HopsParamAccess.LIST, True),
        ],
    outputs=[hs.HopsString("Push log", "Log",
                           "Log of Concept push"),
             ])
def add_area_spring(push: bool, model_file: str, boundary: list[rhino.PolylineCurve], name: list[str],
                    elevation: list[float],
                    kFr0: list[float], kFs0: list[float], kFz0: list[float], kMr0: list[float], kMs0: list[float],
                    kFr1: list[float], kFs1: list[float], kFz1: list[float], kMr1: list[float], kMs1: list[float],
                    kFr2: list[float], kFs2: list[float], kFz2: list[float], kMr2: list[float], kMs2: list[float],
                    angle: list[float]):
    if push:
        logger = []
        # verify valid spring areas and translate to Concept Polygons
        valid_areas = []
        for i, area_boundary in enumerate(boundary):
            valid, log = rhino_geo.check_boundary_validity(area_boundary, i)
            logger.extend(log)
            if valid:
                # store valid
                valid_areas.append({"polygon": concept_geo.polygon_from_polyline(area_boundary),
                                    "name": name[i] if i < len(name) else None,
                                    "elevation": elevation[i] if i < len(elevation) else None,
                                    "kFr0": kFr0[i] if i < len(kFr0) else None,
                                    "kFs0": kFs0[i] if i < len(kFs0) else None,
                                    "kFz0": kFz0[i] if i < len(kFz0) else None,
                                    "kMr0": kMr0[i] if i < len(kMr0) else None,
                                    "kMs0": kMs0[i] if i < len(kMs0) else None,
                                    "kFr1": kFr1[i] if i < len(kFr1) else None,
                                    "kFs1": kFs1[i] if i < len(kFs1) else None,
                                    "kFz1": kFz1[i] if i < len(kFz1) else None,
                                    "kMr1": kMr1[i] if i < len(kMr1) else None,
                                    "kMs1": kMs1[i] if i < len(kMs1) else None,
                                    "kFr2": kFr2[i] if i < len(kFr2) else None,
                                    "kFs2": kFs2[i] if i < len(kFs2) else None,
                                    "kFz2": kFz2[i] if i < len(kFz2) else None,
                                    "kMr2": kMr2[i] if i < len(kMr2) else None,
                                    "kMs2": kMs2[i] if i < len(kMs2) else None,
                                    "angle": angle[i] if i < len(angle) else None,
                                    })
        if valid_areas:
            # open Concept model and extract set api units and signs
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add polygons as area springs
            for spring_area in valid_areas:
                concept_add_struct.add_area_spring(model, **spring_area)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_areas)} spring areas pushed.")
        else:
            logger.append(f"No valid spring areas provided.")
        return logger
