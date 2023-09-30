from typing import Union
from ram_concept.model import Model
from ram_concept.structure_layer import StructureLayer
from ram_concept.point_2D import Point2D
from ram_concept.line_segment_2D import LineSegment2D
from ram_concept.polygon_2D import Polygon2D
from ram_concept.slab_area import SlabAreaBehavior
from ram_concept.beam import BeamBehavior


def add_slab_area(model: Model, polygon: Polygon2D, name: Union[str, None], thickness: Union[float, None],
                  top_of_concrete: Union[float, None], priority: Union[int, None], behaviour: Union[str, None],
                  material: Union[str, None], axis_angle: Union[float, None]):
    # cad layer
    structure_layer: StructureLayer = model.cad_manager.structure_layer
    # add slab area
    slab_area = structure_layer.add_slab_area(polygon)
    # set properties of slab area
    if name is not None:
        slab_area.name = name
    if thickness is not None:
        slab_area.thickness = thickness
    if top_of_concrete is not None:
        slab_area.toc = top_of_concrete
    if priority is not None:
        slab_area.priority = priority
    if behaviour is not None:
        slab_area.behavior = SlabAreaBehavior(behaviour)
    if material is not None:
        slab_area.concrete = model.concretes.concrete(material)
    if axis_angle is not None:
        slab_area.r_axis = axis_angle
    # TODO add stiffness modifiers for custom slab areas


def add_slab_opening(model: Model, polygon: Polygon2D, name: Union[str, None], priority: Union[int, None]):
    # cad layer
    structure_layer: StructureLayer = model.cad_manager.structure_layer
    # add slab opening
    slab_opening = structure_layer.add_slab_opening(polygon)
    # set properties of slab opening
    if name is not None:
        slab_opening.name = name
    if priority is not None:
        slab_opening.priority = priority


def add_column(model: Model, location: Point2D, name: Union[str, None], below_slab: Union[bool, None],
               height: Union[float, None], compressible: Union[bool, None], fixed_near: Union[bool, None],
               fixed_far: Union[bool, None], roller: Union[bool, None], material: Union[str, None],
               i_factor: Union[float, None], depth: Union[float, None], breadth: Union[float, None],
               angle: Union[float, None]):
    # cad layer
    structure_layer: StructureLayer = model.cad_manager.structure_layer
    # add column
    column = structure_layer.add_column(location)
    # set properties of column
    if name is not None:
        column.name = name
    if below_slab is not None:
        column.below_slab = below_slab
    if height is not None:
        column.height = height
    if compressible is not None:
        column.compressible = compressible
    if fixed_near is not None:
        column.fixed_near = fixed_near
    if fixed_far is not None:
        column.fixed_far = fixed_far
    if roller is not None:
        column.roller = roller
    if material is not None:
        column.concrete = model.concretes.concrete(material)
    if i_factor is not None:
        column.i_factor = i_factor
    if depth is not None:
        column.d = depth
    if breadth is not None:
        column.b = breadth
    if angle is not None:
        column.angle = angle


def add_wall(model: Model, line_segments: list[LineSegment2D], name: Union[str, None], below_slab: Union[bool, None],
             height: Union[float, None], compressible: Union[bool, None], fixed_near: Union[bool, None],
             fixed_far: Union[bool, None], shear_wall: Union[bool, None], material: Union[str, None],
             thickness: Union[float, None]):
    # cad layer
    structure_layer: StructureLayer = model.cad_manager.structure_layer
    # add wall segments
    for segment in line_segments:
        wall = structure_layer.add_wall(segment)
        # set properties of wall
        if name is not None:
            wall.name = name
        if below_slab is not None:
            wall.below_slab = below_slab
        if height is not None:
            wall.height = height
        if compressible is not None:
            wall.compressible = compressible
        if fixed_near is not None:
            wall.fixed_near = fixed_near
        if fixed_far is not None:
            wall.fixed_far = fixed_far
        if shear_wall is not None:
            wall.shear_wall = shear_wall
        if material is not None:
            wall.concrete = model.concretes.concrete(material)
        if thickness is not None:
            wall.thickness = thickness


def add_beam(model: Model, line_segments: list[LineSegment2D], name: Union[str, None], thickness: Union[float, None],
             width: Union[float, None], top_of_concrete: Union[float, None], priority: Union[int, None],
             behaviour: Union[str, None], material: Union[str, None], mesh_as_slab: Union[bool, None]):
    # cad layer
    structure_layer: StructureLayer = model.cad_manager.structure_layer
    # add beam segments
    for segment in line_segments:
        beam = structure_layer.add_beam(segment)
        # set properties of beam
        if name is not None:
            beam.name = name
        if thickness is not None:
            beam.thickness = thickness
        if width is not None:
            beam.width = width
        if top_of_concrete is not None:
            beam.toc = top_of_concrete
        if priority is not None:
            beam.priority = priority
        if behaviour is not None:
            beam.behavior = BeamBehavior(behaviour)
        if material is not None:
            beam.concrete = model.concretes.concrete(material)
        if mesh_as_slab is not None:
            beam.mesh_as_slab = mesh_as_slab
    # TODO add stiffness modifiers for custom beams


def add_point_support(model: Model, location: Point2D, name: Union[str, None], elevation: Union[float, None],
                      Fr: Union[bool, None], Fs: Union[bool, None], Fz: Union[bool, None],
                      Mr: Union[bool, None], Ms: Union[bool, None], angle: Union[float, None]):
    # cad layer
    structure_layer: StructureLayer = model.cad_manager.structure_layer
    # add point support
    support = structure_layer.add_point_support(location)
    # set properties of point support
    if name is not None:
        support.name = name
    if elevation is not None:
        support.elevation = elevation
    if Fr is not None:
        support.Fr = Fr
    if Fs is not None:
        support.Fs = Fs
    if Fz is not None:
        support.Fz = Fz
    if Mr is not None:
        support.Mr = Mr
    if Ms is not None:
        support.Ms = Ms
    if angle is not None:
        support.angle = angle


def add_point_spring(model: Model, location: Point2D, name: Union[str, None], elevation: Union[float, None],
                     kFr: Union[float, None], kFs: Union[float, None], kFz: Union[float, None],
                     kMr: Union[float, None], kMs: Union[float, None], angle: Union[float, None]):
    # cad layer
    structure_layer: StructureLayer = model.cad_manager.structure_layer
    # add point spring
    spring = structure_layer.add_point_spring(location)
    # set properties of point spring
    if name is not None:
        spring.name = name
    if elevation is not None:
        spring.elevation = elevation
    if kFr is not None:
        spring.kFr = kFr
    if kFs is not None:
        spring.kFs = kFs
    if kFz is not None:
        spring.kFz = kFz
    if kMr is not None:
        spring.kMr = kMr
    if kMs is not None:
        spring.kMs = kMs
    if angle is not None:
        spring.angle = angle


def add_line_support(model: Model, line_segments: list[LineSegment2D], name: Union[str, None],
                     elevation: Union[float, None],
                     Fr: Union[bool, None], Fs: Union[bool, None], Fz: Union[bool, None],
                     Mr: Union[bool, None], Ms: Union[bool, None]):
    # cad layer
    structure_layer: StructureLayer = model.cad_manager.structure_layer
    # add line segments support
    for segment in line_segments:
        line_support = structure_layer.add_line_support(segment)
        # set properties of point support
        if name is not None:
            line_support.name = name
        if elevation is not None:
            line_support.elevation = elevation
        if Fr is not None:
            line_support.Fr = Fr
        if Fs is not None:
            line_support.Fs = Fs
        if Fz is not None:
            line_support.Fz = Fz
        if Mr is not None:
            line_support.Mr = Mr
        if Ms is not None:
            line_support.Ms = Ms


def add_line_spring(model: Model, line_segments: list[LineSegment2D], name: Union[str, None],
                    elevation: Union[float, None],
                    kFr0: Union[float, None], kFs0: Union[float, None], kFz0: Union[float, None],
                    kMr0: Union[float, None], kMs0: Union[float, None],
                    kFr1: Union[float, None], kFs1: Union[float, None], kFz1: Union[float, None],
                    kMr1: Union[float, None], kMs1: Union[float, None],
                    angle: Union[float, None]):
    # cad layer
    structure_layer: StructureLayer = model.cad_manager.structure_layer
    # add line segments spring
    for segment in line_segments:
        line_spring = structure_layer.add_line_spring(segment)
        # set properties of point support
        if name is not None:
            line_spring.name = name
        if elevation is not None:
            line_spring.elevation = elevation
        if angle is not None:
            line_spring.angle = angle
        # start point stiffness values
        if kFr0 is not None:
            line_spring.kFr0 = kFr0
        if kFs0 is not None:
            line_spring.kFs0 = kFs0
        if kFz0 is not None:
            line_spring.kFz0 = kFz0
        if kMr0 is not None:
            line_spring.kMr0 = kMr0
        if kMs0 is not None:
            line_spring.kMs0 = kMs0
        # end point stiffness values
        if kFr1 is not None:
            line_spring.kFr1 = kFr1
        if kFs1 is not None:
            line_spring.kFs1 = kFs1
        if kFz1 is not None:
            line_spring.kFz1 = kFz1
        if kMr1 is not None:
            line_spring.kMr1 = kMr1
        if kMs1 is not None:
            line_spring.kMs1 = kMs1


def add_area_spring(model: Model, polygon: Polygon2D, name: Union[str, None], elevation: Union[float, None],
                    kFr0: Union[float, None], kFs0: Union[float, None], kFz0: Union[float, None],
                    kMr0: Union[float, None], kMs0: Union[float, None],
                    kFr1: Union[float, None], kFs1: Union[float, None], kFz1: Union[float, None],
                    kMr1: Union[float, None], kMs1: Union[float, None],
                    kFr2: Union[float, None], kFs2: Union[float, None], kFz2: Union[float, None],
                    kMr2: Union[float, None], kMs2: Union[float, None],
                    angle: Union[float, None]):
    # cad layer
    structure_layer: StructureLayer = model.cad_manager.structure_layer
    # add area spring
    area_spring = structure_layer.add_area_spring(polygon)
    # set properties of area spring
    if name is not None:
        area_spring.name = name
    if elevation is not None:
        area_spring.elevation = elevation
    if angle is not None:
        area_spring.angle = angle
    # point 1 stiffness values
    if kFr0 is not None:
        area_spring.kFr0 = kFr0
    if kFs0 is not None:
        area_spring.kFs0 = kFs0
    if kFz0 is not None:
        area_spring.kFz0 = kFz0
    if kMr0 is not None:
        area_spring.kMr0 = kMr0
    if kMs0 is not None:
        area_spring.kMs0 = kMs0
    # point 2 stiffness values
    if kFr1 is not None:
        area_spring.kFr1 = kFr1
    if kFs1 is not None:
        area_spring.kFs1 = kFs1
    if kFz1 is not None:
        area_spring.kFz1 = kFz1
    if kMr1 is not None:
        area_spring.kMr1 = kMr1
    if kMs1 is not None:
        area_spring.kMs1 = kMs1
    # point 3 stiffness values
    if kFr2 is not None:
        area_spring.kFr2 = kFr2
    if kFs2 is not None:
        area_spring.kFs2 = kFs2
    if kFz2 is not None:
        area_spring.kFz2 = kFz2
    if kMr2 is not None:
        area_spring.kMr2 = kMr2
    if kMs2 is not None:
        area_spring.kMs2 = kMs2
