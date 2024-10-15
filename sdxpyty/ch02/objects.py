import math

# normal way using classes
class Shape:
    def __init__(self, name):
        self.name = name

    def perimeter(self):
        raise NotImplementedError("perimeter")

    def area(self):
        raise NotImplementedError("area")


class Square(Shape):
    def __init__(self, name, side):
        super().__init__(name)  # this will use the parent's class contructor
        self.side = side

    def perimeter(self):
        return self.side * 4

    def area(self):
        return self.side**2


class Circle(Shape):
    def __init__(self, name, radius):
        super().__init__(name)
        self.radius = radius

    def perimeter(self):
        return 2 * math.pi * self.radius

    def area(self):
        return math.pi * self.radius**2


# examples: list[Shape] = [Square("sq", 3), Circle("ci", 2)]
# for shape in examples:
#     n = shape.name
#     p = shape.perimeter()
#     a = shape.area()
#     print(f"{n} has a perimeter of {p:.2f} and area {a:.2f}")


# creating our own classes with dicts 
def shape_density(thing: dict, weight: int | float) -> int | float:
    return weight / call(thing, "area")


# our own __init__
def shape_new(name: str) -> dict:
    return {"name": name, "_class": Shape}

def shape_static_example():
    return "I am static method"

static_method = {
    "func": shape_static_example,
    "_method_type": "static"
}

def shape_class_method(cls):
    return f"I am a class method of {cls['_classname']}"

class_method = {
    "func": shape_class_method,
    "_method_type": "class"
}

Shape = {
    "density": shape_density,
    "static_method": static_method,
    "class_method": class_method,
    "_classname": "Shape",
    "_parent": [],
    "_new": shape_new,
}


def make(cls: dict, *args) -> dict:
    return cls["_new"](*args)


def square_perimeter(thing: dict) -> int:
    return thing["side"] * 4


def square_area(thing: dict) -> int:
    return thing["side"] ** 2


def square_larger(thing: dict, size: int) -> bool:
    return call(thing, "area") > size


def square_new(name: str, side: int | float) -> dict:
    return make(Shape, name) | {"side": side, "_class": Square}


Square = {
    "perimeter": square_perimeter,
    "area": square_area,
    "larger": square_larger,
    "_classname": "Square",
    "_parent": [Shape],
    "_new": square_new,
}


def circle_perimeter(thing: dict) -> int | float:
    return math.pi * 2 * thing["radius"]


def circle_area(thing: dict) -> int | float:
    return math.pi * thing["radius"] ** 2


def circle_larger(thing: dict, size) -> bool:
    return call(thing, "area") > size


def circle_new(name: str, radius: int | float) -> dict:
    return make(Shape, name) | {"radius": radius, "_class": Circle}


Circle = {
    "perimeter": circle_perimeter,
    "area": circle_area,
    "larger": circle_larger,
    "_classname": "Circle",
    "_parent": [Shape],
    "_new": circle_new,
}


# TODO: implement multiple inheritance
#   my solution:
#   I turned _parent into list of dicts this means we need to change the find
#   function to loop through all the parents and recurisvely called find on each
#   parent. We put the find in try/except block because if the first parent doesn't 
#   find the method we still want to check the next parents.
def find(cls: dict, method_name):
    while cls is not None:
        if method_name in cls:
            return cls[method_name]
        parents = cls["_parent"]
        for parent in parents:
            try:
                return find(parent, method_name)
            except NotImplementedError:
                continue
    raise NotImplementedError(method_name)


def call(thing, method_name, *args, **kwargs):
    # _class is only available when thing is an object not a class itself
    # this is why we call .get if if not there we return thing itself as the class   
    cls = thing.get("_class", thing)
    method_entry = find(cls, method_name)
    if isinstance(method_entry, dict):
        method = method_entry["func"] 
        method_type = method_entry["_method_type"]

        if method_type == "static":
            return method(*args, **kwargs)
        elif method_type == "class":
            return method(cls, *args, **kwargs)
    else:
        method = method_entry
    return method(thing, *args, **kwargs)


examples = [make(Square, "sq", 3), make(Circle, "ci", 2)]
for shape in examples:
    n = shape["name"]
    p = call(shape, "perimeter")
    a = call(shape, "area")
    d = call(shape, "density", 10)
    print(f"{n} has a perimeter of {p:.2f}, area {a:.2f} and density {d:.2f}")

    size = 10
    result = call(shape, "larger", size)
    print(f"is {n} larger than {size}? {result}")

static_result = call(Shape, "static_method")
print(static_result)

class_method_result = call(Shape, "class_method")
print(class_method_result)