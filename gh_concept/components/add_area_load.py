from gh_concept import hs, hops
import rhino3dm as rhino
from gh_concept.rhino import geometry as rhino_geo
from gh_concept.concept import (model as concept_model,
                                geometry as concept_geo,
                                add_loading as concept_add_load)


@hops.component(
    "/add_area_load",
    name="Concept Add Area Loading",
    nickname="add area loading",
    description="Adds area loading specified loading layer of a specified RAM Concept model.",
    icon="",
    inputs=[
        hs.HopsBoolean("Enable push?", "Push?",
                       "Push to RAM Concept model",
                       hs.HopsParamAccess.ITEM,
                       default=False),
        hs.HopsString("Concept model", "Model",
                      "File path of RAM Concept model",
                      hs.HopsParamAccess.ITEM),
        hs.HopsString("Loading Layer", "LoadingLayer",
                      "Name of loading layer as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsCurve("Loading boundary", "Boundary",
                     "Polyline boundary of loading area as list",
                     hs.HopsParamAccess.LIST),
        hs.HopsString("Loading name", "Name",
                      "Name of area load as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Load elevation", "Elevation",
                      "Elevation of the loading relative to surface",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 1 X-axis force", "Fx0",
                      "Force value in the x-axis at first point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 1 Y-axis force", "Fy0",
                      "Force value in the y-axis at first point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 1 Z-axis force", "Fz0",
                      "Force value in the z-axis at first point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 1 X-axis moment", "Mx0",
                      "Moment about the x-axis at first point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 1 Y-axis moment", "My0",
                      "Moment about the y-axis at first point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 2 X-axis force", "Fx1",
                      "Force value in the x-axis at second point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 2 Y-axis force", "Fy1",
                      "Force value in the y-axis at second point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 2 Z-axis force", "Fz1",
                      "Force value in the z-axis at second point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 2 X-axis moment", "Mx1",
                      "Moment about the x-axis at second point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 2 Y-axis moment", "My1",
                      "Moment about the y-axis at second point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 3 X-axis force", "Fx2",
                      "Force value in the x-axis at third point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 3 Y-axis force", "Fy2",
                      "Force value in the y-axis at third point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 3 Z-axis force", "Fz2",
                      "Force value in the z-axis at third point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 3 X-axis moment", "Mx2",
                      "Moment about the x-axis at third point as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Point 3 Y-axis moment", "My2",
                      "Moment about the y-axis at third point as list",
                      hs.HopsParamAccess.LIST, True),
        ],
    outputs=[hs.HopsString("Push log", "Log",
                           "Log of Concept push"),
             ])
def add_area_load(push: bool, model_file: str, layer_name: list[str], boundary: list[rhino.PolylineCurve],
                  name: list[str], elevation: list[float],
                  Fx0: list[float], Fy0: list[float], Fz0: list[float], Mx0: list[float], My0: list[float],
                  Fx1: list[float], Fy1: list[float], Fz1: list[float], Mx1: list[float], My1: list[float],
                  Fx2: list[float], Fy2: list[float], Fz2: list[float], Mx2: list[float], My2: list[float]):
    if push:
        logger = []
        # check loading layer provided for each location
        if len(layer_name) != len(boundary):
            logger.append("Length of loading layer list and boundary list must match")
            return logger
        # verify valid areas and translate to Concept Polygons
        valid_areas = []
        for i, load_boundary in enumerate(boundary):
            valid_area, log = rhino_geo.check_boundary_validity(load_boundary, i)
            logger.extend(log)
            if valid_area:
                # store valid
                valid_areas.append({"layer_name": layer_name[i],
                                    "polygon": concept_geo.polygon_from_polyline(load_boundary),
                                    "name": name[i] if i < len(name) else None,
                                    "elevation": elevation[i] if i < len(elevation) else None,
                                    "Fx0": Fx0[i] if i < len(Fx0) else None,
                                    "Fy0": Fy0[i] if i < len(Fy0) else None,
                                    "Fz0": Fz0[i] if i < len(Fz0) else None,
                                    "Mx0": Mx0[i] if i < len(Mx0) else None,
                                    "My0": My0[i] if i < len(My0) else None,
                                    "Fx1": Fx1[i] if i < len(Fx1) else None,
                                    "Fy1": Fy1[i] if i < len(Fy1) else None,
                                    "Fz1": Fz1[i] if i < len(Fz1) else None,
                                    "Mx1": Mx1[i] if i < len(Mx1) else None,
                                    "My1": My1[i] if i < len(My1) else None,
                                    "Fx2": Fx2[i] if i < len(Fx2) else None,
                                    "Fy2": Fy2[i] if i < len(Fy2) else None,
                                    "Fz2": Fz2[i] if i < len(Fz2) else None,
                                    "Mx2": Mx2[i] if i < len(Mx2) else None,
                                    "My2": My2[i] if i < len(My2) else None,
                                    })
        if valid_areas:
            # open Concept model and extract set api units and signs
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add polygons as loading areas
            for load_area in valid_areas:
                concept_add_load.add_area_load(model, **load_area)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_areas)} area loads pushed.")
        else:
            logger.append(f"No valid area loads provided.")
        return logger
