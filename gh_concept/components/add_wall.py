from gh_concept import hs, hops
import rhino3dm as rhino
from gh_concept.rhino import geometry as rhino_geo
from gh_concept.concept import (
    model as concept_model,
    geometry as concept_geo,
    add_structure as concept_add_struct,
)


@hops.component(
    "/add_wall",
    name="Concept Add Walls",
    nickname="add walls",
    description="Adds walls to the specified RAM Concept model.",
    icon="images/add_wall.png",
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
            "Wall polyline",
            "WallLine",
            "Polyline of wall as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsString(
            "Wall Name", "Name", "Name of wall as list", hs.HopsParamAccess.LIST, True
        ),
        hs.HopsBoolean(
            "Below slab?",
            "Below?",
            "Is wall below slab as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsNumber(
            "Wall thickness",
            "Thickness",
            "Column section depth as list",
            hs.HopsParamAccess.LIST,
        ),
        hs.HopsString(
            "Concrete material name",
            "Concrete",
            "Concept concrete material name as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsNumber(
            "Wall height",
            "Height",
            "Height of wall as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsBoolean(
            "Compressible?",
            "Compress?",
            "Is wall compressible as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsBoolean(
            "Fixed near?",
            "FixNear?",
            "Is wall fixed near as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsBoolean(
            "Fixed far?",
            "FixFar?",
            "Is wall fixed far as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
        hs.HopsBoolean(
            "Shear wall?",
            "Shear?",
            "Is wall a shear wall as list",
            hs.HopsParamAccess.LIST,
            True,
        ),
    ],
    outputs=[],
)
def add_wall(
    push: bool,
    model_file: str,
    line: list[rhino.PolylineCurve],
    name: list[str],
    below_slab: list[bool],
    thickness: list[float],
    material: list[str],
    height: list[float],
    compressible: list[bool],
    fixed_near: list[bool],
    fixed_far: list[bool],
    shear_wall: list[bool],
):
    if push:
        logger = []
        # verify valid wall locations and translate to Concept Line Segments
        valid_walls = []
        for i, wall_line in enumerate(line):
            valid, log = rhino_geo.check_polyline_validity(wall_line, i)
            logger.extend(log)
            if valid:
                # store valid
                valid_walls.append(
                    {
                        "line_segments": concept_geo.lines_from_polyline(wall_line),
                        "name": name[i] if i < len(name) else None,
                        "below_slab": below_slab[i] if i < len(below_slab) else None,
                        "height": height[i] if i < len(height) else None,
                        "compressible": compressible[i]
                        if i < len(compressible)
                        else None,
                        "fixed_near": fixed_near[i] if i < len(fixed_near) else None,
                        "fixed_far": fixed_far[i] if i < len(fixed_far) else None,
                        "shear_wall": shear_wall[i] if i < len(shear_wall) else None,
                        "material": material[i] if i < len(material) else None,
                        "thickness": thickness[i] if i < len(thickness) else None,
                    }
                )
        if valid_walls:
            # open Concept model and extract set api units and signs
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add line segments as walls
            for wall in valid_walls:
                concept_add_struct.add_wall(model, **wall)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_walls)} walls pushed.")
        else:
            logger.append("No valid walls provided.")
        return logger
