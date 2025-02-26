import rhino3dm as rhino
from gh_concept import hs, hops
from gh_concept.concept import (
    model as concept_model,
    geometry as concept_geo,
    add_structure as concept_add_struct,
)


@hops.component(
    "/add_column",
    name="Concept Add Column",
    nickname="add column",
    description="Adds columns to the specified RAM Concept model.",
    icon="images/add_column.png",
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
        hs.HopsPoint(
            "Column location",
            "Location",
            "Point location of centroid column as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsString(
            "Column Name",
            "Name",
            "Name of column as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsBoolean(
            "Below slab?",
            "Below?",
            "Is column below slab as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsNumber(
            "Section depth/dia",
            "Depth/Dia",
            "Column section depth as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsNumber(
            "Section breadth",
            "Breadth",
            "Column section breadth as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsNumber(
            "Section angle",
            "AxisAngle",
            "Axis rotation of section as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsString(
            "Concrete material name",
            "Concrete",
            "Concept concrete material name as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Column height",
            "Height",
            "Height of column as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsBoolean(
            "Compressible?",
            "Compress?",
            "Is column compressible as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsBoolean(
            "Fixed near?",
            "FixNear?",
            "Is column fixed near as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsBoolean(
            "Fixed far?",
            "FixFar?",
            "Is column fixed far as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsBoolean(
            "Roller?",
            "Roller?",
            "Is column roller restrained as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Bending Factor",
            "CrackFactor",
            "Factor to applied to bending stiffness as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
    ],
    outputs=[
        hs.HopsString("Push log", "Log", "Log of Concept push"),
    ],
)
def add_column(
    push: bool,
    model_file: str,
    location: list[rhino.Point3d],
    name: list[str],
    below_slab: list[bool],
    depth_dia: list[float],
    breadth: list[float],
    angle: list[float],
    material: list[str],
    height: list[float],
    compressible: list[bool],
    fixed_near: list[bool],
    fixed_far: list[bool],
    roller: list[bool],
    bending_factor: list[float],
):
    if push:
        logger = []
        # verify valid column locations and translate to Concept Points
        valid_columns = []
        for i, column in enumerate(location):
            valid_columns.append(
                {
                    "location": concept_geo.point_from_rhino_point(column),
                    "name": name[i] if i < len(name) else None,
                    "below_slab": below_slab[i] if i < len(below_slab) else None,
                    "height": height[i] if i < len(height) else None,
                    "compressible": compressible[i] if i < len(compressible) else None,
                    "fixed_near": fixed_near[i] if i < len(fixed_near) else None,
                    "fixed_far": fixed_far[i] if i < len(fixed_far) else None,
                    "roller": roller[i] if i < len(roller) else None,
                    "material": material[i] if i < len(material) else None,
                    "i_factor": bending_factor[i] if i < len(bending_factor) else None,
                    "depth": depth_dia[i] if i < len(depth_dia) else None,
                    "breadth": breadth[i] if i < len(breadth) else None,
                    "angle": angle[i] if i < len(angle) else None,
                }
            )
        if valid_columns:
            # open Concept model and extract set api units and signs
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add columns at point locations
            for column in valid_columns:
                concept_add_struct.add_column(model, **column)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_columns)} columns pushed.")
        else:
            logger.append("No valid columns provided.")
        return logger
