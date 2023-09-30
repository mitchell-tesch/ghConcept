from gh_concept import hs, hops
import rhino3dm as rhino
from gh_concept.rhino import geometry as rhino_geo
from gh_concept.concept import (model as concept_model,
                                geometry as concept_geo,
                                add_structure as concept_add_struct)


@hops.component(
    "/add_line_support",
    name="Concept Add Line Support",
    nickname="add line support",
    description="Adds line supports to the specified RAM Concept model.",
    icon="",
    inputs=[
        hs.HopsBoolean("Enable push?", "Push?",
                       "Push to RAM Concept model",
                       hs.HopsParamAccess.ITEM,
                       default=False),
        hs.HopsString("Concept model", "Model",
                      "File path of RAM Concept model",
                      hs.HopsParamAccess.ITEM),
        hs.HopsCurve("Support polyline", "SupportLine",
                     "Polyline of support as list",
                     hs.HopsParamAccess.LIST),
        hs.HopsString("Support name", "Name",
                      "Name of support as list",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsNumber("Support elevation", "Elevation",
                      "Elevation of the support relative to soffit",
                      hs.HopsParamAccess.LIST, True),
        hs.HopsBoolean("R-axis fixed?", "Fr?",
                       "Fixed in r-axis as list?",
                       hs.HopsParamAccess.LIST, True),
        hs.HopsBoolean("S-axis fixed?", "Fs?",
                       "Fixed in s-axis as list?",
                       hs.HopsParamAccess.LIST, True),
        hs.HopsBoolean("Z-axis fixed?", "Fz?",
                       "Fixed in z-axis as list?",
                       hs.HopsParamAccess.LIST, True),
        hs.HopsBoolean("R-axis moment fixed?", "Mr?",
                       "Rotationally fixed about r-axis as list?",
                       hs.HopsParamAccess.LIST, True),
        hs.HopsBoolean("S-axis moment fixed?", "Ms?",
                       "Rotationally fixed about s-axis as list?",
                       hs.HopsParamAccess.LIST,True),
        ],
    outputs=[hs.HopsString("Push log", "Log",
                           "Log of Concept push"),
             ])
def add_line_support(push: bool, model_file: str, line: list[rhino.PolylineCurve], name: list[str],
                     elevation: list[float],
                     Fr: list[bool], Fs: list[bool], Fz: list[bool], Mr: list[bool], Ms: list[bool]):
    if push:
        logger = []
        # verify valid line supports and translate Concept Line Segments
        valid_supports = []
        for i, support_line in enumerate(line):
            valid, log = rhino_geo.check_polyline_validity(support_line, i)
            logger.extend(log)
            if valid:
                valid_supports.append({"line_segments": concept_geo.lines_from_polyline(support_line),
                                       "name": name[i] if i < len(name) else None,
                                       "elevation": elevation[i] if i < len(elevation) else None,
                                       "Fr": Fr[i] if i < len(Fr) else None,
                                       "Fs": Fs[i] if i < len(Fs) else None,
                                       "Fz": Fz[i] if i < len(Fz) else None,
                                       "Mr": Mr[i] if i < len(Mr) else None,
                                       "Ms": Ms[i] if i < len(Ms) else None,
                                       })
        if valid_supports:
            # open Concept model and extract set api units and signs
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add line support segments
            for support in valid_supports:
                concept_add_struct.add_line_support(model, **support)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_supports)} line supports pushed.")
        else:
            logger.append(f"No valid line supports provided.")
        return logger
