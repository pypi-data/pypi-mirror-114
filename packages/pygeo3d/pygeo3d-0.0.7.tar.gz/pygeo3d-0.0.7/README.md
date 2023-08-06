
# pygeo3d

This is a vast Mathematical Module which is extremely user-friendly. The module deals with 3-dimensional objects, namely **Point, Line and Plane**. Using this module, the 3D algebra of **Points, Lines and Planes** can be easily performed in python. \
A lot of help text is included in each class, and in the error messages, hence making the module easy to use. \
This module is dependent upon another of my own modules, namely 'pyvectors' without which, this module cannot be used upto its full capacity. For example, Vectors are needed in 3-dimensions to determine the difference between two Points, to determine the direction of a Line, to determine the normal to a Plane and so on. Users are advised to familiarize themselves with pyvectors in order to use pygeo3d effectively.

## Attributes of Point, Line and Plane objects

- Point:
    - self.x, self.y, self.z -> the x, y and z co-ordinates of the Point
    - self.posn_vector -> the unique position Vector associated with that Point, i.e. Vector(x, y, z)
- Line:
    - self.a -> a Point on the Line
    - self.b -> a Vector parallel to the Line
- Plane:
    - self.n -> a Vector normal to the Plane
    - self.d -> the constant in the equation of the Plane (r.n = d)

## Creating Point, Line and Plane objects

- Point:
    > **Point(x, y, z) -> xi + yj + zk** \
    > represents the Position Vector of a Point in 3D space \
    > x, y and z are the Cartesian co-ordinates of the Point
- Line:
    > **Line(Point(x1, y1, z2), Vector(x2, y2, z2)) -> r = (x1i + y1j + z1k) + u(x2i + y2j + z2k)** \
    > represents the Vector Equation of a Line in 3D space \
    > (a := Point(x1, y1, z1)) is a Point on the Line and (b := Vector(x2, y2, z2)) is a Vector parallel to the Line
- Plane:
    > **Plane(Vector(x, y, z), d) -> r.(xi + yj + zk) = d** \
    > represents the Vector Equation of a Plane in 3D space \
    > (n := Vector(x, y, z)) is a Vector normal to the Plane and d is the constant in the equation of the Plane

## Methods of classes Point, Line and Plane

- Point:
    - indexing a Point:
        > Point can be indexed by the strings ("x", "y", "z") which return the x, y and z co-ordinate of the Point respectively \
        > ex: Point(2, -3, 5)["y"] -> -3
    - absolute value of a Point:
        > defined as the distance of the Point from Origin (0, 0, 0) \
        > can be achieved through abs(Point(x, y, z))
    - addition of a Point with a Vector:
        > returns the Point obtained when given Point is moved along a Vector \
        > can be achieved through (p + v)
    - subtraction of two Points:
        > returns the Vector joining the given Points p1 and p2 \
        > can be achieved through p2 - p1 (with tip at p2 and tail at p1)
    - Point.components(point):
        > returns a tuple (x, y, z) containing the co-ordinates of the Point
    - Point.octant(point):
        > returns the octant in which the given Point lies (1 - 8)
    - Point.axis(point):
        > returns the axis on which the given Point lies (1 - 3)
- Line:
    - indexing a Line:
        > Line can be indexed by Real Numbers (int / float) which return the Point located on the Line at the parameter value equal to the given index \
        > ex: Line(Point(1, 2, -4), Vector(2, -1, -1))[2] -> Point(5, 0, -6) \
        > ex: Line(Point(1, 2, -4), Vector(2, -1, -1))[-2.5] -> Point(4, 4.5, -1.5)
    - membership for a Line ("in" operator):
        > left operand - Point \
        > returns True if the Point lies on the Line and False in all other cases
    - Line.directioncos(line):
        > returns a tuple (cosA, cosB, cosC) containing the direction cosines of the Line
    - Line.directionratios(line, k=n):
        > returns a tuple wherein the direction ratios of the Line are scaled by a factor 'n'
    - Line.get_points(line, k1, k2, step=n):
        > returns a tuple of Points on the Line from index k1 to index k2 (including k1 and excluding k2) separated by value step
- Plane:
    - membership for a Plane ("in" operator):
        > left operand - Point / Line \
        > returns True if the Point lies on / the Line is contained in the Plane and False in all other cases
    - Plane.cartesian_repr(plane):
        > returns a str of representation of the Plane in Cartesian form
    - Plane.unit_normal_repr(plane):
        > returns a str of representation of the Plane in terms of its unit normal Vector and its distance from the Origin (0, 0, 0)

Each of these objects can be constructed alternatively by the following classmethods:
- Alternate constructors for Point:
    - Point.FromSequence(seq):
        > creates a Point whose co-ordinates are taken from the given list, tuple or dict \
        > to pass a dict as an argument, appropriate keys ("x", "y", "z") must be used
    - Point.FromVector(vector):
        > creates the unique Point associated with the given Position Vector \
        > using Vector(x, y, z) as an argument results in the Point(x, y, z)
- Alternate constructors for Line:
    - Line.FromAngles(alpha, beta, gamma, point=p):
        > creates a Line inclined to the co-ordinate axes at the given angles passing through the given Point
    - Line.From2Points(p1, p2):
        > creates a Line passing through two unique Points
- Alternate constructors for Plane:
    - Plane.FromPointNormal(n, point=p):
        > creates a Plane with normal Vector n, passing through the given Point
    - Plane.From3Points(p1, p2, p3):
        > creates a Plane passing through three unique non-collinear Points
    - Plane.From2Lines(l1, l2):
        > creates a Plane containing the two unique non-skew Lines
    - Plane.From2Planes(pi1, pi2, point=p):
        > creates a Plane through the Line of intersection of the given Planes passing through the given Point
    - Plane.FromLinePoint(line=l, point=p):
        > creates a Plane containing the given Line passing through the given Point

And many more... Each function contains help text that can be accessed through help() in python to know more about it. Users are advised to read help() on methods they want to use to ensure required results.

## Plotting a 3D - object
Many methods are provided for the user to plot and visualize 3-dimensional Points, Lines, Planes, Line Segments and Vectors. In order, these are:

- Methods attached to classes:
    - Point.plot(p1):
        > plots single Point
    - Point.plot_vectors(p1, p2, p3, ..., pn, show_legend=True):
        > plots multiple Points on the same grid
    - Line.plot(l1):
        > plots single Line
    - Line.plot_vectors(l1, l2, l3, ..., ln, show_legend=True):
        > plots multiple Lines on the same grid
    - Plane.plot(pi1):
        > plots single Plane
    - Plane.plot_vectors(pi1, pi2, pi3, ..., pin, show_legend=True):
        > plots multiple Planes on the same grid
- Functions (not attached to any class):
    - plot_linesegment(p1, p2):
        > plots the Line Segment joining two unique Points
    - plot_objects(o1, o2, o3, ..., on, show_legend=True, plot_intersections=False):
        > plots any number of 3D objects on the same grid \
        > to refer to a Line Segment, pass a tuple of two unique Points \
        > plot_intersections is a boolean which if True, plots the objects along with their Points / Lines of intersection (if any)
    - plot_random_objects(points=x1, lines=x2, planes=x3, vectors=x4, linesegs=x5, show_legend=True):
        > plots given number of each 3D object (chosen randomly) on the same grid
- From the module pyvectors:
    - Vector.plot(v1):
        > plots single Vector
    - Vector.plot_vectors(v1, v2, v3, ..., vn, show_legend=True):
        > plots multiple Vectors on the same grid

Notes:
- in each method / function that plots multiple objects, show_legend is a boolean which displays legend on the plot if True
- to plot a single object only, it is best practice to use object.plot() method
- to plot multiple objects of the same type, it is best practice to use the method associated with that class

## Other functions

- distance(...):
    > returns the shortest Euclidean distance between two Points, Lines, Planes or any combination thereof
- angle(...):
    > returns the acute angle between two Lines, Planes or any combination thereof
- parallel(...):
    > returns True if all given Lines and Planes are parallel to each other and False in all other cases
- perpendicular(...):
    > returns True if two Lines, Planes and or combination thereof are perpendicular and False in all other cases
- section(p1, p2, m, n, external=False):
    > returns the Point which divides the Line Segment joining p1 and p2 in the ratio m : n internally by default
- midpoint(p1, p2):
    > returns the midpoint of the Line Segment joining p1 and p2
- area(p1, p2, p3):
    > returns the area of the triangle formed by p1, p2 and p3
- centroid(p1, p2, p3):
    > returns the centroid of the triangle formed by p1, p2 and p3
- collinear(...):
    > returns True if all given Points are collinear and False in all other cases
- coplanar(...):
    > returns True if all given Points are coplanar and False in all other cases
- intersection(...):
    - returns the:
        - Point of intersection of two Lines
        - Point of intersection of Line and Plane (and vice - versa)
        - Point of intersection of three Planes
        - Line of intersection of two Planes
- image(...):
    - returns the image of:
        - Point in a Line
        - Point in a Plane
        - Line in a Line
        - Line in a Plane
        - Plane in a Plane
- projection(...):
    - returns the projection of:
        - Point on a Line
        - Point on a Plane
        - Line on a Plane

And many more... Each function contains help text that can be accessed through help() in python to know more about it. Users are advised to read help() on methods they want to use to ensure required results.

## CONSTANTS
- ORIGIN = origin = Point(0, 0, 0)
- X_AXIS = x_axis = Line(origin, Vector(1, 0, 0))
- Y_AXIS = y_axis = Line(origin, Vector(0, 1, 0))
- Z_AXIS = z_axis = Line(origin, Vector(0, 0, 1))
- XY_PLANE = xy_plane = Plane(Vector(0, 0, 1), 0)
- YZ_PLANE = yz_plane = Plane(Vector(1, 0, 0), 0)
- ZX_PLANE = zx_plane = Plane(Vector(1, 0, 1), 0)

## Updates (0.0.5)
- Minor bug fixes
- Alternate constructor for Point - Point.FromSequence(seq) can now accept generators / generator expressions as argument
- More colors available for plotting objects - Points, Lines, Planes and Line Segments (and Vectors)

## Updates (0.0.6)
Line objects now support slicing - which returns a tuple of Points on the Line at the indices given in the slice
> for example: \
> Line(Point(1, -2, 3), Vector(-2, 4, -1))[-1.5:1:0.5] -> (Point(-2, 4, 1.5), Point(-1, 2, 2), Point(0, 0, 2.5), Point(1, -2, 3), Point(2, -4, 3.5))

## Updates (0.0.7)
- Minor bug fixes
- Better type hinting for functions

## Reach out to me
Feel free to reach out to me if you notice any bugs or if you need any kind of help from me in understanding the usage of the module or the source code. My email: knightt1821@gmail.com