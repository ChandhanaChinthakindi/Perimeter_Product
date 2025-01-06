"""
Product of Perimeter Problem:

Algorithm Steps for Perimeter Product Calculation:
1. **Find Intersection Points**:
   - Identify intersection points between all line segments and gather unique 
     points that include intersection points.

2. **Determine Collinear Points**:
   - For each line segment, find points that are collinear with it, forming
     extended lines.

3. **Generate Line Segments**:
   - Create new line segments by pairing collinear points.

4. **Build Adjacency List**:
   - Create an adjacency list to represent connections between points.

5. **Find Cycles (Enclosed Areas)**:
   - Use Depth-First Search (DFS) to identify cycles in the adjacency list.

6. **Filter Unique Cycles**:
   - Remove duplicate cycles to retain only unique cycles.

7. **Remove Redundant Cycles**:
   - Eliminate cycles that contain other cycles within them.

8. **Check Points Inside Cycles**:
   - For each cycle, ensure no unique points lie inside it.

9. **Calculate Perimeter**:
   - Compute the perimeter of each unique cycle.

10. **Calculate Perimeter Product**:
   - Multiply the perimeters of all valid unique cycles to get the final product.

"""

# Define the line segments

line_segments = [

#Testcase 1:
    # ((1, 1), (1, 2)),
    # ((1, 2), (2, 2)),
    # ((2, 2), (2, 1)),
    # ((2, 1), (1, 1))

#Testcase 2:
    # ((1, 1), (1, 2)),
    # ((1, 2), (2, 1)),
    # ((2, 1), (2, 2)),
    # ((2, 2), (1, 1))


#Testcase 3:
    # ((1, 1), (1, 2)),
    # ((1, 2), (2, 2)),
    # ((2, 2), (2, 1)),
    # ((2, 1), (1, 1)), 
    # ((1.5, 1), (1.5, 2)),
    # ((1, 1.5), (2, 1.5))

#Testcase 4:
    ((1, 1), (1, 2)),
    ((1, 2), (1.8, 2)),
    ((1.8, 2), (1.8, 1)),
    ((1.8, 1), (1, 1)),
    ((1.2, 1), (1.2, 2)),
    ((1.6, 1), (1.6, 2)),
    ((1, 1.5), (1.6, 1.8)),
    ((1, 1.3), (1.8, 1.7)),
    ((1.2, 1.2), (1.8, 1.5))

]

import math
def find_intersection(A, B, C, D):
    """
    Find the intersection point of two line segments defined by points A-B and C-D.
    Returns the intersection point or None if they are parallel or coincident.
    """
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C
    x4, y4 = D

    # Calculate differences in coordinates
    dx1, dy1 = x2 - x1, y2 - y1
    dx2, dy2 = x4 - x3, y4 - y3

    # Calculate the determinant
    determinant = dx1 * dy2 - dy1 * dx2
    if determinant == 0:
        return None  # Lines are parallel or coincident

    # Calculate parameters t and u to determine the intersection point
    t = ((x3 - x1) * dy2 - (y3 - y1) * dx2) / determinant
    u = ((x3 - x1) * dy1 - (y3 - y1) * dx1) / determinant

    # Check if the intersection point is within the bounds of both line segments
    if 0 <= t <= 1 and 0 <= u <= 1:
        intersection_x = x1 + t * dx1
        intersection_y = y1 + t * dy1
        return (intersection_x, intersection_y)

    return None  # No intersection

def get_unique_points(line_segments):
    """
    Retrieve a set of unique points from the given line segments and their intersection points.
    """
    unique_points = set()
    for i in range(len(line_segments)-1):
        for j in range(i+1, len(line_segments)):
            p1 = line_segments[i][0]
            p2 = line_segments[i][1]
            p3 = line_segments[j][0]
            p4 = line_segments[j][1]
            intersection_point = find_intersection(p1, p2, p3, p4)
            if intersection_point is not None:
                unique_points.add(intersection_point)

            unique_points.add(p1)
            unique_points.add(p2)
            unique_points.add(p3)
            unique_points.add(p4)
    # print("Unique points:", unique_points)
    return unique_points

def are_points_collinear(A, B, C):
    """
    Check if points A, B, and C are collinear.
    Returns True if they are collinear and C lies within the bounds of A and B.
    """
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C
    
    lhs = round((y2 - y1) * (x3 - x2), 1)
    rhs = round((y3 - y2) * (x2 - x1), 1)
    within_bounds = min(x1, x2) <= x3 <= max(x1, x2) and min(y1, y2) <= y3 <= max(y1, y2)
    
    # Check for collinearity using slope comparison
    return (lhs == rhs) and within_bounds

def get_all_collinear_points(line_segments, unique_points):
    """
    For each line segment, find all collinear points including the segment's endpoints.
    Returns a list of lists containing collinear points for each segment.
    """
    collinear_points_list = []
    for line in line_segments:
        p1 = line[0]
        p2 = line[1]
        collinear_points = set()
        collinear_points.add(p1)
        collinear_points.add(p2)

        for point in unique_points:
            if are_points_collinear(p1, p2, point):
                collinear_points.add(point)

        collinear_points = sorted(collinear_points)
        collinear_points_list.append(collinear_points)

    return collinear_points_list

def generate_line_segments(collinear_points_list):
    """
    Generate new line segments from pairs of collinear points.
    Returns a list of new line segments.
    """
    new_line_segments = []
    for points in collinear_points_list:
        # Take pairs of points to form line segments
        for i in range(len(points) - 1):
            segment = (points[i], points[i + 1])
            new_line_segments.append(segment)
    return new_line_segments

def create_adjacency_list(new_line_segments):
    """
    Create an adjacency list from the new line segments.
    Each point is a key in the dictionary, and its value is a list of connected points.
    """
    adjacency_list = {}
    for start, end in new_line_segments:
        adjacency_list.setdefault(start, []).append(end)
        adjacency_list.setdefault(end, []).append(start)
    return adjacency_list

def find_enclosed_areas(adjacency_list):
    """
    Use depth-first search (DFS) to find cycles in the adjacency list.
    Returns a list of cycles found.
    """
    visited = set()
    cycles = []

    def dfs(start, current, path):
        path.append(current)
        visited.add(current)

        for neighbor in adjacency_list[current]:
            if neighbor == start and len(path) > 2:
                cycles.append(path[:])
            elif neighbor not in visited:
                dfs(start, neighbor, path)
        
        path.pop()
        visited.remove(current)

    for point in adjacency_list:
        if point not in visited:
            dfs(point, point, [])
    return cycles

def unique_cycles(cycles):
    """
    Filter out duplicate cycles by sorting them and checking for uniqueness.
    Returns a list of unique cycles.
    """
    def sort_cycle(cycle):
        return sorted(cycle, key=lambda point: (point[0], point[1]))

    unique_cycle_lists = []
    seen = set()
    for cycle in cycles:
        t = tuple(sort_cycle(cycle))
        if t not in seen:
            unique_cycle_lists.append(cycle)
            seen.add(t)
    return unique_cycle_lists

def eliminate_repeat_list(unique_cycles_list):
    """
    Remove cycles that are supersets of other cycles, retaining only the smallest cycles.
    Returns a list of smallest unique cycles.
    """
    smallest_cycles = []
    for cycle in unique_cycles_list:
        if not any(set(cycle).issuperset(set(other_cycle)) for other_cycle in unique_cycles_list if cycle != other_cycle):
            smallest_cycles.append(cycle)
    return smallest_cycles

def is_point_in_polygon(point, polygon):
    """
    Determine if a point is inside a given polygon using the ray-casting algorithm.
    Returns True if the point is inside, otherwise False.
    """
    x, y = point
    inside = False
    n = len(polygon)
    
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def filter_cycles(cycles, unique_points):
    """
    Filter cycles to retain only those that do not contain any unique points inside them.
    Returns the filtered cycles.
    """
    final_cycles = []
    for cycle in cycles:
        inside = False
        filtered_unique_points = {point for point in unique_points if point not in cycle}
        for point in filtered_unique_points:
            if is_point_in_polygon(point, cycle):
                inside = True
                break
        
        if not inside:
            final_cycles.append(cycle)

    return final_cycles

def calculate_perimeter(cycle):
    """
    Calculate the perimeter of a cycle defined by its vertices.
    Returns the perimeter value.
    """
    perimeter = 0.0
    for i in range(len(cycle)):
        x1, y1 = cycle[i]
        x2, y2 = cycle[(i + 1) % len(cycle)]
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)       
        perimeter += round(distance, 3)

    return perimeter

def main(line_segments):
    unique_points = get_unique_points(line_segments)
    collinear_points_list = get_all_collinear_points(line_segments, unique_points)
    new_line_segments = generate_line_segments(collinear_points_list)
    adjacency_list = create_adjacency_list(new_line_segments)
    cycles = find_enclosed_areas(adjacency_list)
    unique_cycles_list = unique_cycles(cycles)
    smallest_unique_cycles = eliminate_repeat_list(unique_cycles_list)

    final_filtered_cycles = filter_cycles(smallest_unique_cycles, unique_points)

    # Calculate and print the product of perimeters of unique cycles
    perimeters = [calculate_perimeter(cycle) for cycle in final_filtered_cycles]
    product_of_perimeters = math.prod(perimeters)

    # Print Cycles with each Perimeter
    # for idx, cycle in enumerate(final_filtered_cycles):
    #     print(f"***Cycle {idx + 1}****: {cycle}, Perimeter: {perimeters[idx]:.2f}")
    #     # print(f"{cycle}")

    return product_of_perimeters

# Main execution flow
if __name__=="__main__":
    result = main(line_segments)
    print(f"Product of Perimeters: {result}")
