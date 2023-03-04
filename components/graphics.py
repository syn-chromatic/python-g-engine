from turtle import Turtle, Screen


class GraphicsScreen:
    def __new__(cls) -> "GraphicsScreen":
        if not hasattr(cls, "instance"):
            cls.instance = super(GraphicsScreen, cls).__new__(cls)
            cls.turtle_screen = Screen()
            cls.turtle_screen.tracer(0)
        return cls.instance

    def set_screensize(self, width: int, height: int):
        self.turtle_screen.screensize(width, height)

    def set_background_color(self, r: float, g: float, b: float):
        self.turtle_screen.bgcolor(r, g, b)

    def set_title(self, title: str):
        self.turtle_screen.title(title)

    def update(self):
        self.turtle_screen.update()


class Graphics:
    def __new__(cls) -> "Graphics":
        if not hasattr(cls, "instance"):
            cls.instance = super(Graphics, cls).__new__(cls)
            cls.turtle_object = Turtle()
            cls.turtle_object.hideturtle()
        return cls.instance

    def draw_circle(
        self,
        p: tuple[float, float],
        radius: float,
        color: tuple[float, float, float],
    ):
        x, y = p
        y -= radius
        self.turtle_object.pencolor(*color)
        self.turtle_object.fillcolor(*color)
        self.turtle_object.penup()
        self.turtle_object.goto(x, y)
        self.turtle_object.begin_fill()
        self.turtle_object.circle(radius)
        self.turtle_object.end_fill()

    def draw_line(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        thickness: int,
        color: tuple[float, float, float],
    ):
        self.turtle_object.pensize(thickness)
        self.turtle_object.pencolor(*color)
        self.turtle_object.fillcolor(*color)
        self.turtle_object.penup()
        self.turtle_object.goto(*p1)
        self.turtle_object.pendown()
        self.turtle_object.goto(*p2)
        self.turtle_object.penup()

    def draw_text(
        self,
        position: tuple[float, float],
        color: tuple[float, float, float],
        text: str,
    ):
        self.turtle_object.pencolor(color)
        self.turtle_object.fillcolor(color)
        self.turtle_object.penup()
        self.turtle_object.goto(position)
        self.turtle_object.write(text, font=("Arial", 24, "normal"))

    def clear_screen(self):
        self.turtle_object.clear()
