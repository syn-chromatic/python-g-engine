from turtle import Turtle, Screen


class GraphicsScreen:
    def __init__(self):
        self.turtle_screen = Screen()
        self.turtle_screen.tracer(0)

    def set_screensize(self, width: int, height: int):
        self.turtle_screen.screensize(width, height)

    def set_background_color(self, r: float, g: float, b: float):
        self.turtle_screen.bgcolor(r, g, b)

    def set_title(self, title: str):
        self.turtle_screen.title(title)

    def update(self):
        self.turtle_screen.update()


class Graphics:
    def __init__(self):
        self.turtle_object = Turtle()
        self.turtle_object.hideturtle()

    def draw_circle(
        self,
        p: tuple[float, float],
        radius: float,
        color: tuple[float, float, float],
    ):
        x, y = p
        # print(x, y, radius)
        # input()
        y -= radius

        # y -= radius - y / 2



        self.turtle_object.pencolor(*color)
        self.turtle_object.fillcolor(*color)
        self.turtle_object.penup()
        self.turtle_object.goto(x, y)
        self.turtle_object.begin_fill()
        self.turtle_object.circle(radius)
        self.turtle_object.end_fill()

        # self.turtle_object.goto(*p)

        # self.turtle_object.pencolor((0.0, 1.0, 0.0))
        # self.turtle_object.fillcolor((0.0, 1.0, 0.0))
        # self.turtle_object.begin_fill()
        # self.turtle_object.circle(1)
        # self.turtle_object.end_fill()



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
