from gh_concept import hs, hops
import rhino3dm as rhino
from gh_concept.rhino import geometry as rhino_geo
from gh_concept.concept import (model as concept_model,
                                geometry as concept_geo,
                                add_structure as concept_add_struct)


@hops.component(
    "/add_beam",
    name="Concept Add Beam",
    nickname="add beam",
    description="Adds beams to the specified RAM Concept model.",
    icon="images/add_slab_area.png",
    inputs=[
        hs.HopsBoolean("Enable push?", "Push?",
                       "Push to RAM Concept model",
                       hs.HopsParamAccess.ITEM,
                       default=False),
        hs.HopsString("Concept model", "Model",
                      "File path of RAM Concept model",
                      hs.HopsParamAccess.ITEM),
        hs.HopsCurve("Beam polyline", "BeamLine",
                     "Polyline of beam as list",
                     hs.HopsParamAccess.LIST),
        hs.HopsString("Beam name", "Name",
                      "Name of beam as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsNumber("Beam thickness", "Thickness",
                      "Beam thickness as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsNumber("Beam width", "Width",
                      "Beam thickness as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsNumber("Top of concrete", "TopLevel",
                      "Relative top of concrete as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsInteger("Priority", "Priority",
                       "Priority of beam as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsString("Analysis behaviour", "Behaviour",
                      "Beam analysis behaviour as list\n\
                          (custom, no-torsion two-way slab, two-way slab)",
                      hs.HopsParamAccess.LIST),
        hs.HopsString("Concrete material name", "Concrete",
                      "Concept concrete material name as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsBoolean("Mesh as slab?", "Mesh?",
                       "Mesh beam as slab as list",
                       hs.HopsParamAccess.LIST),
        ],
    outputs=[hs.HopsString("Push log", "Log",
                           "Log of Concept push"),
             ])
def add_beam(push: bool, model_file: str, line: list[rhino.PolylineCurve], name: list[str], thickness: list[float],
             width: list[float], top_of_concrete: list[float], priority: list[int], behaviour: list[str],
             material: list[str], mesh_as_slab: list[float]):
    if push:
        logger = []
        # verify valid beam lines and translate to Concept Line Segments
        valid_beams = []
        for i, beam_line in enumerate(line):
            valid, log = rhino_geo.check_polyline_validity(beam_line, i)
            logger.extend(log)
            if valid:
                # store valid
                valid_beams.append({"line_segments": concept_geo.lines_from_polyline(beam_line),
                                    "name": name[i] if i < len(name) else None,
                                    "thickness": thickness[i] if i < len(thickness) else None,
                                    "width": width[i] if i < len(width) else None,
                                    "top_of_concrete": top_of_concrete[i] if i < len(top_of_concrete) else None,
                                    "priority": priority[i] if i < len(priority) else None,
                                    "behaviour": behaviour[i] if i < len(behaviour) else None,
                                    "material": material[i] if i < len(material) else None,
                                    "mesh_as_slab": mesh_as_slab[i] if i < len(mesh_as_slab) else None,
                                    })
        if valid_beams:
            # open Concept model and extract set api units and sings
            concept, model = concept_model.open_concept_model(model_file)
            file_units, file_signs = concept_model.set_api_units_signs(model)
            # add line segments as beams
            for beam in valid_beams:
                concept_add_struct.add_beam(model, **beam)
            # restore user units and save and close Concept
            concept_model.restore_file_units_signs(model, file_units, file_signs)
            concept_model.save_close_concept(concept, model, model_file)
            logger.append(f"{len(valid_beams)} beams pushed.")
        else:
            logger.append(f"No valid beams provided.")
        return logger
