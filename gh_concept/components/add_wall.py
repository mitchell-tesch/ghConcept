import rhino3dm as rhino
from gh_concept import hs, hops
from gh_concept.concept import (model as concept_model,
                                geometry as concept_geo,
                                add_structure as concept_add_struct)


@hops.component(
    "/add_wall",
    name="Concept Add Walls",
    nickname="add walls",
    description="Adds walls to the specified RAM Concept model.",
    icon="images/add_wall.png",
    inputs=[
        hs.HopsBoolean("Enable push?", "Push?",
                       "Push to RAM Concept model",
                       hs.HopsParamAccess.ITEM,
                       default=False),
        hs.HopsString("Concept model", "Model",
                      "File path of RAM Concept model",
                      hs.HopsParamAccess.ITEM),
        hs.HopsCurve("Wall polyline", "Wall",
                     "Polyline of wall as list",
                     hs.HopsParamAccess.LIST),
        hs.HopsString("Wall Name", "Name",
                      "Name of wall as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsBoolean("Below slab?", "Below?",
                       "Is wall below slab as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsNumber("Wall thickness", "Thickness",
                      "Column section depth as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsString("Concrete material name", "Concrete",
                      "Concept concrete material name as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsNumber("Wall height", "Height",
                      "Height of wall as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsBoolean("Compressible?", "Compress?",
                       "Is wall compressible as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsBoolean("Fixed near?", "FixNear?",
                       "Is wall fixed near as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsBoolean("Fixed far?", "FixFar?",
                       "Is wall fixed far as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsBoolean("Shear wall?", "Shear?",
                       "Is wall a shear wall as list",
                       hs.HopsParamAccess.LIST),
        ],
    outputs=[])
def add_wall(push: bool, model_file: str, wall_lines: list[rhino.PolylineCurve], name: list[str],
             below_slab: list[bool], thickness: list[float], material: list[str], height: list[float],
             compressible: list[bool], fixed_near: list[bool], fixed_far: list[bool], shear: list[bool]):
    if push:
        # open Concept model and extract set api units and sings
        concept, model = concept_model.open_concept_model(model_file)
        file_units, file_signs = concept_model.set_api_units_signs(model)
        # establish Concept location from Rhino point
        for i, wall_polyline in enumerate(wall_lines):
            wall_polyline: rhino.PolylineCurve
            wall_segments = concept_geo.lines_from_polyline(wall_polyline)
            concept_add_struct.add_wall(model, wall_segments, name[i], below_slab[i], height[i], compressible[i],
                                        fixed_near[i], fixed_far[i], shear[i], material[i], thickness[i])
        # restore user units and save and close Concept
        concept_model.restore_file_units_signs(model, file_units, file_signs)
        concept_model.save_close_concept(concept, model, model_file)
