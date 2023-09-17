from gh_concept import hs, hops
import rhino3dm as rhino
from gh_concept.concept import (model as concept_model,
                                geometry as concept_geo,
                                add_structure as concept_add_struct)


@hops.component(
    "/add_slab_area",
    name="Concept Add Slab Areas",
    nickname="add slabs",
    description="Adds a slab areas to the specified RAM Concept model.",
    icon="images/add_slab_area.png",
    inputs=[
        hs.HopsBoolean("Enable push?", "Push?",
                       "Push to RAM Concept model",
                       hs.HopsParamAccess.ITEM,
                       default=False),
        hs.HopsString("Concept model", "Model",
                      "File path of RAM Concept model",
                      hs.HopsParamAccess.ITEM),
        hs.HopsCurve("Slab boundary", "Boundary",
                     "Polyline Boundary of slab as list",
                     hs.HopsParamAccess.LIST),
        hs.HopsString("Slab name", "Name",
                      "Name of slab area as list",
                      hs.HopsParamAccess.ITEM),
        hs.HopsNumber("Slab thickness", "Thickness",
                      "Slab thickness as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsNumber("Top of concrete", "TopLevel",
                      "Relative top of concrete as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsInteger("Priority", "Priority",
                       "Priority of slab as list",
                       hs.HopsParamAccess.LIST),
        hs.HopsString("Analysis behaviour", "Behaviour",
                      "Slab analysis behaviour as list\n\
                          (custom, no-torsion two-way slab, one-way slab, two-way slab)",
                      hs.HopsParamAccess.LIST),
        hs.HopsString("Concrete material name", "Concrete",
                      "Concept concrete material name as list",
                      hs.HopsParamAccess.LIST),
        hs.HopsNumber("Axis Angle", "AxisAngle",
                      "Axis rotation angle as list",
                      hs.HopsParamAccess.LIST),
        ],
    outputs=[])
def add_slab_area(push: bool, model_file: str, boundary: list[rhino.PolylineCurve], name: list[str],
                  thickness: list[float], top_of_concrete: list[float], priority: list[int], behaviour: list[str],
                  material: list[str], axis_angle: list[float]):
    if push:
        # open Concept model and extract set api units and sings
        concept, model = concept_model.open_concept_model(model_file)
        file_units, file_signs = concept_model.set_api_units_signs(model)
        # add slab boundaries
        for i, boundary in enumerate(boundary):
            # establish concept polygon from Rhino closed polyline
            boundary_points = []
            for p in range(0, boundary.PointCount - 1):
                boundary_points.append(concept_geo.point_from_rhino_point(boundary.Point(p)))
            polygon = concept_geo.Polygon2D(boundary_points)
            # push slab area
            concept_add_struct.add_slab_area(model, polygon, name[i], thickness[i], top_of_concrete[i],
                                             priority[i], behaviour[i], material[i], axis_angle[i])
        # restore user units and save and close Concept
        concept_model.restore_file_units_signs(model, file_units, file_signs)
        concept_model.save_close_concept(concept, model, model_file)
