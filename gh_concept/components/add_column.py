import rhino3dm as rhino
from gh_concept import hs, hops
from gh_concept.concept import (model as concept_model,
                                geometry as concept_geo,
                                add_structure as concept_add_struct)


@hops.component(
    "/add_column",
    name="Concept Add Columns",
    nickname="add columns",
    description="Adds columns to the specified RAM Concept model.",
    icon="images/add_column.png",
    inputs=[
        hs.HopsBoolean("Enable push?", "Push?",
                       "Push to RAM Concept model",
                       hs.HopsParamAccess.ITEM,
                       default=False),
        hs.HopsString("Concept model", "Model",
                      "File path of RAM Concept model",
                      hs.HopsParamAccess.ITEM),
        hs.HopsPoint("Column location", "Location",
                     "Point location of centroid column as list",
                     hs.HopsParamAccess.LIST),
        hs.HopsString("Column Name", "Name",
                      "Name of column as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsBoolean("Below slab?", "Below?",
                       "Is column below slab as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsNumber("Section depth/dia", "Depth/Dia",
                      "Column section depth as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsNumber("Section breadth", "Breadth",
                      "Column section breadth as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsNumber("Section angle", "AxisAngle",
                      "Axis rotation of section as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsString("Concrete material name", "Concrete",
                      "Concept concrete material name as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsNumber("Column height", "Height",
                      "Height of column as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsBoolean("Compressible?", "Compress?",
                       "Is column compressible as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsBoolean("Fixed near?", "FixNear?",
                       "Is column fixed near as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsBoolean("Fixed far?", "FixFar?",
                       "Is column fixed far as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsBoolean("Roller?", "Roller?",
                       "Is column roller restrained as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsNumber("Bending Factor", "CrackFactor",
                      "Factor to applied to bending stiffness as list",
                      hs.HopsParamAccess.LIST),
        ],
    outputs=[])
def add_column(push: bool, model_file: str, location: list[rhino.Point3d], name: list[str], below_slab: list[bool],
               depth_dia: list[float], breadth: list[float], angle: list[float], material: list[str],
               height: list[float], compressible: list[bool], fixed_near: list[bool], fixed_far: list[bool],
               roller: list[bool], bending_factor: list[float]):
    if push:
        # open Concept model and extract set api units and sings
        concept, model = concept_model.open_concept_model(model_file)
        file_units, file_signs = concept_model.set_api_units_signs(model)
        # establish Concept location from Rhino point
        for i, location in enumerate(location):
            location = concept_geo.point_from_rhino_point(location)
            concept_add_struct.add_column(model, location, name[i], below_slab[i], height[i], compressible[i],
                                          fixed_near[i], fixed_far[i], roller[i], material[i], bending_factor[i],
                                          depth_dia[i], breadth[i], angle[i])
        # restore user units and save and close Concept
        concept_model.restore_file_units_signs(model, file_units, file_signs)
        concept_model.save_close_concept(concept, model, model_file)
