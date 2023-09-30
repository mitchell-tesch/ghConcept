from gh_concept import hs, hops
import rhino3dm as rhino
from gh_concept.rhino import geometry as rhino_geo
from gh_concept.concept import (model as concept_model,
                                geometry as concept_geo,
                                add_loading as concept_add_load)


@hops.component(
    "/add_point_load",
    name="Concept Add Point Loading",
    nickname="add point loading",
    description="Adds point loading specified loading layer of a specified RAM Concept model.",
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
        hs.HopsPoint("Load location", "Location",
                     "Point location of load as list",
                     hs.HopsParamAccess.LIST),
        hs.HopsString("Loading name", "Name",
                      "Name of point load as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Load elevation", "Elevation",
                      "Elevation of the loading relative to surface",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("X-axis force", "Fx",
                      "Force value in the x-axis direction",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Y-axis force", "Fy",
                      "Force value in the y-axis direction",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Z-axis force", "Fz",
                      "Force value in the z-axis direction",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("X-axis moment", "Mx",
                      "Moment about the x-axis direction",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Y-axis moment", "My",
                      "Moment about the y-axis direction",
                      hs.HopsParamAccess.LIST, True),
        ],
    outputs=[hs.HopsString("Push log", "Log",
                           "Log of Concept push"),
             ])
def add_point_load(push: bool, model_file: str, layer_name: list[str], location: list[rhino.Point3d],
                   name: list[str], elevation: list[float],
                   Fx: list[float], Fy: list[float], Fz: list[float], Mx: list[float], My: list[float]):
    if push:
        logger = []
        # check loading layer provided for each location
        if len(layer_name) != len(location):
            logger.append("Length of loading layer list and location list must match")
            return logger
        # verify valid point load locations and translate to Concept Points
        valid_loads = []
        for i, point in enumerate(location):
            valid_loads.append({"layer_name": layer_name[i],
                                "location": concept_geo.point_from_rhino_point(point),
                                "name": name[i] if i < len(name) else None,
                                "elevation": elevation[i] if i < len(elevation) else None,
                                "Fx": Fx[i] if i < len(Fx) else None,
                                "Fy": Fy[i] if i < len(Fy) else None,
                                "Fz": Fz[i] if i < len(Fz) else None,
                                "Mx": Mx[i] if i < len(Mx) else None,
                                "My": My[i] if i < len(My) else None,
                                })
        if valid_loads:
            # open Concept model and extract set api units and signs
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add point loads
            for load_area in valid_loads:
                concept_add_load.add_point_load(model, **load_area)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_loads)} point loads pushed.")
        else:
            logger.append(f"No valid point loads provided.")
        return logger
