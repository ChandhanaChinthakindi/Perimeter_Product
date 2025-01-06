# Perimeter_Product
Given a list of line segments represented as a set of two x,y points.
( ((x1, y1), (x2, y2)),
  ((x3, y3), (x4, y4)), …. )
The final result we wish to calculate is to find the multiplicative product of all perimeters of all the individual enclosed areas.
Note: 
-> If there are two areas, but we do not explicitly write the intersection point at the neck of the hourglass. 
-> We do NOT double count the larger original square, nor the 4 possible rectangles. 
-> We expect the floating point solution, not the exact values.
