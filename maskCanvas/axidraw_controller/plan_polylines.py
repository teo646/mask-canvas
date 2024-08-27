from maskCanvas import Point
def find_nearest_polyline(point, polylines):
    nearest_polyline = polylines[0]
    min_distance = get_squared_distance(nearest_polyline.path[0], point)

    for polyline in polylines:
        distance = get_squared_distance(polyline.path[0], point)
        if(distance < 10):
            return polyline
        if(min_distance > distance):
            nearest_polyline = polyline
            min_distance = distance

        distance = get_squared_distance(polyline.path[-1], point)
        if(distance < 10):
            polyline.path.reverse()
            return polyline
        if(min_distance > distance):
            polyline.path.reverse()
            nearest_polyline = polyline
            min_distance = distance

    return nearest_polyline


def get_squared_distance(point1, point2):
    return (point1.coordinate[0] - point2.coordinate[0])**2\
            + (point1.coordinate[1] - point2.coordinate[1])**2

def arrange_polylines(polylines):
    starting_polyline = find_nearest_polyline(Point(0,0), polylines)
    arranged_polylines = [starting_polyline]
    polylines.remove(starting_polyline)

    while len(polylines) != 0:
        current_point = arranged_polylines[-1].path[-1]
        next_polyline = find_nearest_polyline(current_point, polylines)
        arranged_polylines.append(next_polyline)
        polylines.remove(next_polyline)

    return arranged_polylines

def classify_polylines_by_pen(polylines):
    classified_polylines = {}
    for polyline in polylines:
        if(polyline.pen in classified_polylines.keys()):
            classified_polylines[polyline.pen].append(polyline)
        else:
            classified_polylines[polyline.pen] = [polyline]
    return classified_polylines

def plan_polylines(polylines):
    classified_polylines = classify_polylines_by_pen(polylines)

    for pen in classified_polylines:
        classified_polylines[pen] = arrange_polylines(classified_polylines[pen])

    return classified_polylines


