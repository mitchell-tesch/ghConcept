from typing import Union
from ram_concept.model import Model
from ram_concept.cad_manager import CadManager
from ram_concept.force_loading_layer import ForceLoadingLayer
from ram_concept.point_2D import Point2D
from ram_concept.line_segment_2D import LineSegment2D
from ram_concept.polygon_2D import Polygon2D


def add_loading_layer(model: Model, layer_name: str, layer_type: str):
    # cad layer
    cad_manager: CadManager = model.cad_manager
    if layer_type.lower == "force":
        cad_manager.add_force_loading_layer(layer_name)
    elif layer_type.lower == "shrink":
        cad_manager.add_shrinkage_loading_layer(layer_name)
    elif layer_type.lower == "temp":
        cad_manager.add_temperature_loading_layer(layer_name)
    else:
        cad_manager.add_load_combo_layer(layer_name)


def add_area_load(model: Model, layer_name: str, polygon: Polygon2D, name: Union[str, None],
                  elevation: Union[float, None],
                  Fx0: Union[float, None], Fy0: Union[float, None], Fz0: Union[float, None], Mx0: Union[float, None],
                  My0: Union[float, None],
                  Fx1: Union[float, None], Fy1: Union[float, None], Fz1: Union[float, None], Mx1: Union[float, None],
                  My1: Union[float, None],
                  Fx2: Union[float, None], Fy2: Union[float, None], Fz2: Union[float, None], Mx2: Union[float, None],
                  My2: Union[float, None]):
    # cad layer
    loading_layer: ForceLoadingLayer = model.cad_manager.force_loading_layer(layer_name)
    load_area = loading_layer.add_area_load(polygon)
    # set properties of area load
    if name is not None:
        load_area.name = name
    if elevation is not None:
        load_area.elevation = elevation
    # point 1 loading values
    if Fx0 is not None:
        load_area.Fx0 = Fx0
    if Fy0 is not None:
        load_area.Fy0 = Fy0
    if Fz0 is not None:
        load_area.Fz0 = Fz0
    if Mx0 is not None:
        load_area.Mx0 = Mx0
    if My0 is not None:
        load_area.My0  = My0
    # point 2 loading values
    if Fx1 is not None:
        load_area.Fx1 = Fx1
    if Fy1 is not None:
        load_area.Fy1 = Fy1
    if Fz1 is not None:
        load_area.Fz1 = Fz1
    if Mx1 is not None:
        load_area.Mx1 = Mx1
    if My1 is not None:
        load_area.My1  = My1
    # point 3 loading values
    if Fx2 is not None:
        load_area.Fx2 = Fx2
    if Fy2 is not None:
        load_area.Fy2 = Fy2
    if Fz2 is not None:
        load_area.Fz2 = Fz2
    if Mx2 is not None:
        load_area.Mx2 = Mx2
    if My2 is not None:
        load_area.My2  = My2


def add_line_load(model: Model, layer_name: str, line_segments: list[LineSegment2D], name: Union[str, None],
                  elevation: Union[float, None],
                  Fx0: Union[float, None], Fy0: Union[float, None], Fz0: Union[float, None], Mx0: Union[float, None],
                  My0: Union[float, None],
                  Fx1: Union[float, None], Fy1: Union[float, None], Fz1: Union[float, None], Mx1: Union[float, None],
                  My1: Union[float, None]):
    # cad layer
    loading_layer: ForceLoadingLayer = model.cad_manager.force_loading_layer(layer_name)
    # add line load segments
    for segment in line_segments:
        load_line = loading_layer.add_line_load(segment)
        # set properties of line load
        if name is not None:
            load_line.name = name
        if elevation is not None:
            load_line.elevation = elevation
        # start point loading values
        if Fx0 is not None:
            load_line.Fx0 = Fx0
        if Fy0 is not None:
            load_line.Fy0 = Fy0
        if Fz0 is not None:
            load_line.Fz0 = Fz0
        if Mx0 is not None:
            load_line.Mx0 = Mx0
        if My0 is not None:
            load_line.My0 = My0
        # end point loading values
        if Fx1 is not None:
            load_line.Fx1 = Fx1
        if Fy1 is not None:
            load_line.Fy1 = Fy1
        if Fz1 is not None:
            load_line.Fz1 = Fz1
        if Mx1 is not None:
            load_line.Mx1 = Mx1
        if My1 is not None:
            load_line.My1 = My1


def add_point_load(model: Model, layer_name: str, location: Point2D, name: Union[str, None],
                   elevation: Union[float, None],
                   Fx: Union[float, None], Fy: Union[float, None], Fz: Union[float, None], Mx: Union[float, None],
                   My: Union[float, None]):
    # cad layer
    loading_layer: ForceLoadingLayer = model.cad_manager.force_loading_layer(layer_name)
    # add point load
    point_load = loading_layer.add_point_load(location)
    if name is not None:
        point_load.name = name
    if elevation is not None:
        point_load.elevation = elevation
    if Fx is not None:
        point_load.Fx = Fx
    if Fy is not None:
        point_load.Fy = Fy
    if Fz is not None:
        point_load.Fz = Fz
    if Mx is not None:
        point_load.Mx = Mx
    if My is not None:
        point_load.My = My
