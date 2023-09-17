from ram_concept.model import Model
from ram_concept.point_2D import Point2D
from ram_concept.line_segment_2D import LineSegment2D
from ram_concept.polygon_2D import Polygon2D
from ram_concept.slab_area import SlabAreaBehavior
from ram_concept.line_segment_2D import LineSegment2D


def add_slab_area(model: Model, polygon: Polygon2D, name: str, thickness: float, top_of_concrete: float,
                  priority: int, behaviour: str, material: str, axis_rotation: float):
    # cad layer
    structure_layer = model.cad_manager.structure_layer
    # add slab area
    slab_area = structure_layer.add_slab_area(polygon)
    # set properties of slab area
    slab_area.name = name
    slab_area.thickness = thickness
    slab_area.toc = top_of_concrete
    slab_area.priority = priority
    slab_area.behavior = SlabAreaBehavior(behaviour)
    slab_area.concrete = model.concretes.concrete(material)
    slab_area.r_axis = axis_rotation


def add_column(model: Model, location: Point2D, name: str, below_slab: bool, height: float,
               compressible: bool, fixed_near: bool, fixed_far: bool, roller: bool,
               material: str, i_factor: float, depth: float, breadth: float, angle: float):
    # cad layer
    structure_layer = model.cad_manager.structure_layer
    # add column
    column = structure_layer.add_column(location)
    # set properties of column
    column.name = name
    column.below_slab = below_slab
    column.height = height
    column.compressible = compressible
    column.fixed_near = fixed_near
    column.fixed_far = fixed_far
    column.roller = roller
    column.concrete = model.concretes.concrete(material)
    column.i_factor = i_factor
    column.d = depth
    column.b = breadth
    column.angle = angle


def add_wall(model: Model, line_segments: list[LineSegment2D], name: str, below_slab: bool,
             height: float, compressible: bool, fixed_near: bool, fixed_far: bool, shear_wall: bool,
             material: str, thickness: float):
    # cad layer
    structure_layer = model.cad_manager.structure_layer
    # add  wall segments
    for segment in line_segments:
        wall = structure_layer.add_wall(segment)
        # set properties of wall
        wall.name = name
        wall.below_slab = below_slab
        wall.height = height
        wall.compressible = compressible
        wall.fixed_near = fixed_near
        wall.fixed_far = fixed_far
        wall.shear_wall = shear_wall
        wall.concrete = model.concretes.concrete(material)
        wall.thickness = thickness