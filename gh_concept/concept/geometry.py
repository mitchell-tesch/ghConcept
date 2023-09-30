import rhino3dm as rhino

from ram_concept.point_2D import Point2D
from ram_concept.line_segment_2D import LineSegment2D
from ram_concept.polygon_2D import Polygon2D


def point_from_rhino_point(rhino_point: rhino.Point3d) -> Point2D:
    """Converts a Rhino Point3d to RAM Concept Point2D

    :param rhino_point: Rhino Point3d
    :return: RAM Concept Point2D
    """
    return Point2D(rhino_point.X, rhino_point.Y)


def lines_from_polyline(rhino_polyline: rhino.PolylineCurve) -> list[LineSegment2D]:
    """Converts a Rhino PolyLineCurve to a RAM Concept LineSegments

    :param rhino_polyline: Rhino polyline
    :return: List of RAM Concept LineSegment2D
    """
    lines: list[LineSegment2D] = []
    if type(rhino_polyline) is rhino.LineCurve:
        start_point = point_from_rhino_point(rhino_polyline.PointAtStart)
        end_point = point_from_rhino_point(rhino_polyline.PointAtEnd)
        lines = [LineSegment2D(start_point, end_point)]
    else:
        for point in range(0, rhino_polyline.PointCount - 1):
            start_point = point_from_rhino_point(rhino_polyline.Point(point))
            end_point = point_from_rhino_point(rhino_polyline.Point(point + 1))
            lines.append(LineSegment2D(start_point, end_point))
    return lines


def polygon_from_polyline(rhino_polyline: rhino.PolylineCurve) -> Polygon2D:
    """Convert a Rhino PolylineCurve to a RAM Concept Polygon2D

    :param rhino_polyline: Rhino polyline
    :return: RAM Concept Polygon2D
    """
    points = []
    for p in range(0, rhino_polyline.PointCount - 1):
        points.append(point_from_rhino_point(rhino_polyline.Point(p)))
    return Polygon2D(points)
    