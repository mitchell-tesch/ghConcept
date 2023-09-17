import rhino3dm as rhino

from ram_concept.point_2D import Point2D
from ram_concept.line_segment_2D import LineSegment2D
from ram_concept.polygon_2D import Polygon2D



def point_from_rhino_point(rhino_point: rhino.Point3d) -> Point2D:
    return Point2D(rhino_point.X, rhino_point.Y)


def polygon_from_points(points: list[Point2D]) -> Polygon2D:
    return Polygon2D(points)


def lines_from_polyline(rhino_polyline: rhino.PolylineCurve) -> list[LineSegment2D]:
    lines: list[LineSegment2D] = []
    for point in range(0, rhino_polyline.PointCount - 1):
        start_point = point_from_rhino_point(rhino_polyline.Point(point))
        end_point = point_from_rhino_point(rhino_polyline.Point(point + 1))
        lines.append(LineSegment2D(start_point, end_point))
    return lines
    