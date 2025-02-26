from gh_concept import hs, hops
import rhino3dm as rhino
from gh_concept.rhino import geometry as rhino_geo
from gh_concept.concept import (
    model as concept_model,
    geometry as concept_geo,
    add_loading as concept_add_load,
)


@hops.component(
    "/add_line_load",
    name="Concept Add Line Load",
    nickname="add line load",
    description="Adds line loads to specified loading layer of a specified RAM Concept model.",
    icon="",
    inputs=[
        hs.HopsBoolean(
            "Enable push?",
            "Push?",
            "Push to RAM Concept model",
            hs.HopsParamAccess.ITEM,
            default=False,
        ),
        hs.HopsString(
            "Concept model",
            "Model",
            "File path of RAM Concept model",
            hs.HopsParamAccess.ITEM,
        ),
        hs.HopsString(
            "Loading Layer",
            "LoadingLayer",
            "Name of loading layer as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsCurve(
            "Load polyline",
            "Line",
            "Polyline of load line as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsString(
            "Loading name",
            "Name",
            "Name of line load as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Load elevation",
            "Elevation",
            "Elevation of the loading relative to surface",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Start X-axis force",
            "Start_Fx",
            "Force value in the x-axis direction at start as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Start Y-axis force",
            "Start_Fy",
            "Force value in the y-axis direction at start as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Start Z-axis force",
            "Start_Fz",
            "Force value in the z-axis direction at start as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Start X-axis moment",
            "Start_Mx",
            "Moment value about x-axis direction at start as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Start Y-axis moment",
            "Start_My",
            "Moment value about the x-axis direction at start as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "End X-axis force",
            "End_Fx",
            "Force value in the x-axis direction at end as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "End Y-axis force",
            "End_Fy",
            "Force value in the y-axis direction at end as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "End Z-axis force",
            "End_Fz",
            "Force value in the z-axis direction at end as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "End X-axis moment",
            "End_Mx",
            "Moment value about x-axis direction at end as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "End Y-axis moment",
            "End_My",
            "Moment value about the x-axis direction at end as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
    ],
    outputs=[
        hs.HopsString("Push log", "Log", "Log of Concept push"),
    ],
)
def add_line_load(
    push: bool,
    model_file: str,
    layer_name: list[str],
    line: list[rhino.PolylineCurve],
    name: list[str],
    elevation: list[float],
    Fx0: list[float],
    Fy0: list[float],
    Fz0: list[float],
    Mx0: list[float],
    My0: list[float],
    Fx1: list[float],
    Fy1: list[float],
    Fz1: list[float],
    Mx1: list[float],
    My1: list[float],
):
    if push:
        logger = []
        # check loading layer provided for each location
        if len(layer_name) != len(line):
            logger.append("Length of loading layer list and boundary list must match")
            return logger
        # verify valid line loads and translate Concept Line Segments
        valid_loads = []
        for (
            i,
            load_line,
        ) in enumerate(line):
            valid, log = rhino_geo.check_polyline_validity(load_line, i)
            logger.extend(log)
            if valid:
                valid_loads.append(
                    {
                        "layer_name": layer_name[i],
                        "line_segments": concept_geo.lines_from_polyline(load_line),
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
                    }
                )
        if valid_loads:
            # open Concept model and extract set api units and signs
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add line load segments
            for load in valid_loads:
                concept_add_load.add_line_load(model, **load)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_loads)} line loads pushed.")
        else:
            logger.append("No valid line loads provided.")
        return logger
