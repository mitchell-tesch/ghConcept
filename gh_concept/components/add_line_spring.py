from gh_concept import hs, hops
import rhino3dm as rhino
from gh_concept.rhino import geometry as rhino_geo
from gh_concept.concept import (
    model as concept_model,
    geometry as concept_geo,
    add_structure as concept_add_struct,
)


@hops.component(
    "/add_line_spring",
    name="Concept Add Line Spring",
    nickname="add line spring",
    description="Adds line springs to the specified RAM Concept model.",
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
        hs.HopsCurve(
            "Spring polyline",
            "SupportLine",
            "Polyline of spring line as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsString(
            "Support name",
            "Name",
            "Name of support as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Support elevation",
            "Elevation",
            "Elevation of the line spring relative to soffit",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Start R-axis stiffness",
            "Start_kFr",
            "Spring stiffness in r-axis at start as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Start S-axis stiffness",
            "Start_kFs",
            "Spring stiffness in s-axis at start as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Start Z-axis stiffness",
            "Start_kFz",
            "Spring stiffness in z-axis at start as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Start R-axis rotational stiffness",
            "Start_kMr",
            "Rotational spring stiffness about r-axis at start as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Start S-axis rotational stiffness",
            "Start_kMs",
            "Rotational spring stiffness about s-axis at start as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "End R-axis stiffness",
            "End_kFr",
            "Spring stiffness in r-axis at end as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "End S-axis stiffness",
            "End_kFs",
            "Spring stiffness in s-axis at end as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "End Z-axis stiffness",
            "End_kFz",
            "Spring stiffness in z-axis at end as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "End R-axis rotational stiffness",
            "End_kMr",
            "Rotational spring stiffness about r-axis at end as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "End S-axis rotational stiffness",
            "End_kMs",
            "Rotational spring stiffness about s-axis at end as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Support axis angle",
            "AxisAngle",
            "Axis rotation of support axis as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
    ],
    outputs=[
        hs.HopsString("Push log", "Log", "Log of Concept push"),
    ],
)
def add_line_spring(
    push: bool,
    model_file: str,
    line: list[rhino.PolylineCurve],
    name: list[str],
    elevation: list[float],
    kFr0: list[float],
    kFs0: list[float],
    kFz0: list[float],
    kMr0: list[float],
    kMs0: list[float],
    kFr1: list[float],
    kFs1: list[float],
    kFz1: list[float],
    kMr1: list[float],
    kMs1: list[float],
    angle: list[float],
):
    if push:
        logger = []
        # verify valid line springs and translate Concept Line Segments
        valid_springs = []
        for (
            i,
            support_line,
        ) in enumerate(line):
            valid, log = rhino_geo.check_polyline_validity(support_line, i)
            logger.extend(log)
            if valid:
                valid_springs.append(
                    {
                        "line_segments": concept_geo.lines_from_polyline(support_line),
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
                        "angle": angle[i] if i < len(angle) else None,
                    }
                )
        if valid_springs:
            # open Concept model and extract set api units and signs
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add line spring segments
            for spring in valid_springs:
                concept_add_struct.add_line_spring(model, **spring)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_springs)} line springs pushed.")
        else:
            logger.append("No valid line springs provided.")
        return logger
