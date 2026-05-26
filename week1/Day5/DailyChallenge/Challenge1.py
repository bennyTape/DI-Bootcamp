import math
import turtle


class Circle:
    """A class representing a geometric circle."""

    def __init__(self, radius):
        self.radius = radius

    
    @classmethod
    def from_diameter(cls, diameter):
        """Create a Circle by specifying its diameter instead of radius."""
        return cls(diameter / 2)

    
    @property
    def diameter(self):
        return self.radius * 2

    @property
    def area(self):
        return math.pi * self.radius ** 2

    
    def __str__(self):
        return (
            f"Circle(radius={self.radius:.2f}, "
            f"diameter={self.diameter:.2f}, "
            f"area={self.area:.2f})"
        )

    def __repr__(self):
        return f"Circle(radius={self.radius!r})"

    def __add__(self, other):
        """Add two circles → new Circle whose radius is the sum of both radii."""
        if not isinstance(other, Circle):
            return NotImplemented
        return Circle(self.radius + other.radius)

    def __eq__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius

    def __gt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius > other.radius

    def __lt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius

    def __ge__(self, other):
        return self.radius >= other.radius

    def __le__(self, other):
        return self.radius <= other.radius


# ---------------------------------------------------------------------------
# Turtle drawing
# ---------------------------------------------------------------------------
COLORS = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6"]

def draw_circles(sorted_circles):
    """Draw sorted circles side-by-side using the turtle module."""
    screen = turtle.Screen()
    screen.title("Sorted Circles")
    screen.bgcolor("#1a1a2e")
    screen.setup(width=900, height=500)

    t = turtle.Turtle()
    t.speed(0)          # fastest
    t.hideturtle()
    t.pensize(2)

    # Space circles evenly across the screen
    n = len(sorted_circles)
    total_width = 800
    spacing = total_width / (n + 1)
    start_x = -total_width / 2 + spacing

    for i, circle in enumerate(sorted_circles):
        x = start_x + i * spacing
        color = COLORS[i % len(COLORS)]

        # --- filled circle ---
        t.penup()
        t.goto(x, -circle.radius)   # turtle.circle() starts at bottom
        t.pendown()
        t.fillcolor(color)
        t.pencolor("white")
        t.begin_fill()
        t.circle(circle.radius)
        t.end_fill()

        # --- label below ---
        t.penup()
        t.goto(x, -circle.radius - 25)
        t.pencolor("white")
        t.write(
            f"r={circle.radius}",
            align="center",
            font=("Arial", 11, "bold"),
        )

    screen.mainloop()


# ---------------------------------------------------------------------------
# Demo / Test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    c1 = Circle(5)
    c2 = Circle(3)
    c3 = Circle.from_diameter(16)   # radius = 8
    c4 = Circle(3)

    print("=== Individual circles ===")
    print(c1)
    print(c2)
    print(c3)
    print(f"c4 (from diameter=6) → {c4}")

    print("\n=== Area ===")
    print(f"Area of {c1!r}: {c1.area:.4f}")
    print(f"Area of {c3!r}: {c3.area:.4f}")

    print("\n=== Addition ===")
    c_sum = c1 + c2
    print(f"{c1!r} + {c2!r} = {c_sum}")

    print("\n=== Comparisons ===")
    print(f"c1 > c2  → {c1 > c2}")
    print(f"c2 > c3  → {c2 > c3}")
    print(f"c2 == c4 → {c2 == c4}")
    print(f"c1 == c3 → {c1 == c3}")

    print("\n=== Sorting ===")
    circles = [c3, c1, c2, Circle(1), Circle(10), c4]
    print("Unsorted:", circles)
    circles.sort()
    print("Sorted:  ", circles)

    print("\n=== Drawing with Turtle (close the window to exit) ===")
    draw_circles(circles)