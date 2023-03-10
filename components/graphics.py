from turtle import Turtle, Screen


class Graphics:
    def __new__(cls) -> "Graphics":
        if not hasattr(cls, "instance"):
            cls.instance = super(Graphics, cls).__new__(cls)
            cls.turtle_object = Turtle()
            cls.turtle_screen = Screen()
            cls.turtle_screen.tracer(0)
            cls.turtle_screen.listen()
            cls.turtle_object.hideturtle()
        return cls.instance

    def set_screensize(self, width: int, height: int):
        self.turtle_screen.screensize(width, height)

    def set_background_color(self, r: float, g: float, b: float):
        self.turtle_screen.bgcolor(r, g, b)

    def set_title(self, title: str):
        self.turtle_screen.title(title)

    def update(self):
        self.turtle_screen.update()

    def get_canvas(self):
        canvas = self.turtle_screen.getcanvas()
        return canvas

    def get_pointer_xy(self) -> tuple[int, int]:
        canvas = self.get_canvas()
        return canvas.winfo_pointerxy()

    def draw_circle(
        self,
        point: tuple[float, float],
        radius: float,
        color: tuple[float, float, float],
    ):
        x, y = point
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
        point1: tuple[float, float],
        point2: tuple[float, float],
        thickness: int,
        color: tuple[float, float, float],
    ):
        self.turtle_object.pensize(thickness)
        self.turtle_object.pencolor(*color)
        self.turtle_object.fillcolor(*color)
        self.turtle_object.penup()
        self.turtle_object.goto(*point1)
        self.turtle_object.pendown()
        self.turtle_object.goto(*point2)
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
