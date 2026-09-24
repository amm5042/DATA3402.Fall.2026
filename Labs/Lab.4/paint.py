class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]

    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]

    def v_line(self, x, y, w, **kargs):
        for i in range(x, x + w):
            self.set_pixel(i, y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y, y + h):
            self.set_pixel(x, i, **kargs)

    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2 - y1) / (x2 - x1)
        for y in range(y1, y2):
            x = int(slope * y)
            self.set_pixel(x, y, **kargs)

    def display(self):
        print("\n".join(["".join(row) for row in self.data]))



import math

class shape:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def x(self):
        return self.__x
    def y(self):
        return self.__y

    def area(self):
        raise NotImplementedError
    def perimeter(self):
        raise NotImplementedError
    def points_perimeter(self):
        raise NotImplementedError
    def points_container(self, px, py):
        raise NotImplementedError

    def overlaps(self, other):
        for (px, py) in self.points_perimeter():
            if other.points_container(px, py):
                return True
        for (px, py) in other.points_perimeter():
            if self.points_container(px, py):
                return True
        return False

    def paint(self, canvas):
        for (px, py) in self.points_perimeter():
            row = int(py)
            col = int(px)
            if 0 <= row < canvas.height and 0 <= col < canvas.width:
                canvas.set_pixel(row, col)


class CompoundShape:
    def __init__(self, shapes = None):
        self.shapes = shapes if shapes is not None else []

    def add_shape(self, shape_obj):
        self.shapes.append(shape_obj)

    def paint(self, canvas):
        for s in self.shapes:
            s.paint(canvas)

class rectangle(shape):
    def __init__(self, length, width, x, y):
        shape.__init__(self, x, y)
        self.__length = length
        self.__width = width

    def length(self):
        return self.__length
    def width(self):
        return self.__width

    def area(self):
        return self.length() * self.width()

    def perimeter(self):
        return 2 * (self.length() + self.width())

    def points_perimeter(self):
        points = []
        corners = [
            (self.x(), self.y()),
            (self.x() + self.length(), self.y()),
            (self.x() + self.length(), self.y() + self.width()),
            (self.x(), self.y() + self.width())
        ]
        for i in range(4):
            start = corners[i]
            finish = corners[(i + 1) % 4]
            for j in range(4):
                t = j / 4
                px = start[0] + t * (finish[0] - start[0])
                py = start[1] + t * (finish[1] - start[1])
                points.append((px, py))
        return points

    def points_container(self, px, py):
        inside_x = self.x() <= px <= self.x() + self.length()
        inside_y = self.y() <= py <= self.y() + self.width()
        return inside_x and inside_y

class circle(shape):
    def __init__(self, radius, x, y):
        shape.__init__(self, x, y)
        self.__radius = radius

    def radius(self):
        return self.__radius

    def area(self):
        return math.pi * self.radius() ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius()

    def points_perimeter(self):
        points = []
        for i in range(16):
            angle = i * 2 * math.pi / 16
            px = self.x() + self.radius() * math.cos(angle)
            py = self.y() + self.radius() * math.sin(angle)
            points.append((px, py))
        return points

    def points_container(self, px, py):
        distance = math.sqrt((px - self.x())**2 + (py - self.y())**2)
        return distance <= self.radius()

class triangle(shape):
    def __init__(self, a, b, c, x, y):
        shape.__init__(self, x, y)
        self.__a = a
        self.__b = b
        self.__c = c

    def a(self):
        return self.__a
    def b(self):
        return self.__b
    def c(self):
        return self.__c

    def perimeter(self):
        return self.a() + self.b() + self.c()
    def area(self):
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a()) * (s - self.b()) * (s - self.c()))

    def points_perimeter(self):
        v0 = (self.x(), self.y())
        v1 = (self.x() + self.a(), self.y())
        angle = math.acos((self.a() ** 2 + self.c() ** 2 - self.b() ** 2) / (2 * self.a() * self.c()))
        v2 = (self.x() + self.c() * math.cos(angle), self.y() + self.c() * math.sin(angle))

        corners = [v0, v1, v2]
        points = []
        counts = [6, 5, 5]
        for i in range(3):
            start = corners[i]
            finish = corners[(i + 1) % 3]
            n = counts[i]
            for j in range(n):
                t = j / n
                px = start[0] + t * (finish[0] - start[0])
                py = start[1] + t * (finish[1] - start[1])
                points.append((px, py))
        return points

    def points_container(self, px, py):
        v0 = (self.x(), self.y())
        v1 = (self.x() + self.a(), self.y())
        angle = math.acos((self.a() ** 2 + self.c() ** 2 - self.b() ** 2) / (2 * self.a() * self.c()))
        v2 = (self.x() + self.c() * math.cos(angle), self.y() + self.c() * math.sin(angle))

        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        d1 = sign((px, py), v0, v1)
        d2 = sign((px, py), v1, v2)
        d3 = sign((px, py), v2, v0)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)        