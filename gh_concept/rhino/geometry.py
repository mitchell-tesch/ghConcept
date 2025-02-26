import rhino3dm as rhino


def check_boundary_validity(
    boundary: rhino.PolylineCurve, index: int = 0
) -> tuple[bool, list[str]]:
    problems = []
    valid = True
    if not boundary.IsValid:
        problems.append(f"Boundary at index {index} is invalid.")
        valid = False
    if not boundary.IsClosed:
        problems.append(f"Boundary at index {index} is not closed.")
        valid = False
    if not boundary.IsPlanar():
        problems.append(f"Boundary at index {index} is not planar.")
        valid = False
    if not boundary.IsPolyline():
        problems.append(f"Boundary at index {index} contains curve segments.")
        valid = False
    return valid, problems


def check_polyline_validity(
    polyline: rhino.PolylineCurve, index: int = 0
) -> tuple[bool, list[str]]:
    problems = []
    valid = True
    if not polyline.IsValid:
        problems.append(f"Polyline/Line at index {index} is invalid.")
        valid = False
    if not polyline.IsPlanar():
        problems.append(f"Polyline/Line at index {index} is not planar.")
        valid = False
    if not polyline.IsPolyline():
        problems.append(f"Polyline/Line at index {index} contains curve segments.")
        valid = False
    return valid, problems
