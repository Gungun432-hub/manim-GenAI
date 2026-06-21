from manim import *
import numpy as np

class PythagoreanTheorem(Scene):
    def construct(self):
        # Define vertices for a right-angled triangle (a=3, b=4, c=5)
        p1 = ORIGIN
        p2 = RIGHT * 4
        p3 = UP * 3

        triangle = Polygon(p1, p2, p3, color=WHITE)

        # Side lengths
        len_a = np.linalg.norm(p3 - p1)  # vertical side
        len_b = np.linalg.norm(p2 - p1)  # horizontal side
        len_c = np.linalg.norm(p3 - p2)  # hypotenuse

        # Create squares on each side
        # Square on side 'a' (vertical)
        square_a = Polygon(
            p1,
            p3,
            p3 + LEFT * len_a,
            p1 + LEFT * len_a,
            color=BLUE,
            fill_opacity=0.7
        )

        # Square on side 'b' (horizontal)
        square_b = Polygon(
            p1,
            p2,
            p2 + DOWN * len_b,
            p1 + DOWN * len_b,
            color=RED,
            fill_opacity=0.7
        )

        # Square on side 'c' (hypotenuse) - initially as an outline
        # Calculate vector perpendicular to (p3 - p2) and pointing outwards
        perp_vec_c = rotate_vector(
            normalize(p3 - p2),
            -PI / 2
        ) * len_c

        square_c_outline = Polygon(
            p2,
            p3,
            p3 + perp_vec_c,
            p2 + perp_vec_c,
            color=GREEN,
            fill_opacity=0
        )

        square_c_filled = square_c_outline.copy().set_fill(
            GREEN,
            opacity=0.7
        )

        # Labels for sides
        label_a = Text("a").next_to(
            (p1 + p3) / 2,
            LEFT,
            buff=0.1
        )

        label_b = Text("b").next_to(
            (p1 + p2) / 2,
            DOWN,
            buff=0.1
        )

        label_c = Text("c").next_to(
            (p2 + p3) / 2,
            UR,
            buff=0.1
        )  # UR because hypotenuse goes from DR to UL

        # Labels for areas
        area_a_label = Text("a^2").move_to(square_a.get_center()).set_color(BLACK)
        area_b_label = Text("b^2").move_to(square_b.get_center()).set_color(BLACK)
        area_c_label = Text("c^2").move_to(square_c_outline.get_center()).set_color(BLACK)

        # Group side labels and area labels for easier animation
        side_labels = VGroup(label_a, label_b, label_c)
        area_labels = VGroup(area_a_label, area_b_label, area_c_label)

        # Display triangle and labels
        self.play(Create(triangle))
        self.play(Write(side_labels))
        self.wait(0.5)

        # Display squares and area labels
        self.play(
            Create(square_a),
            Create(square_b),
            Create(square_c_outline)
        )
        self.play(Write(area_labels))
        self.wait(1)

        # Demonstrate combination: Fade out context, move small squares to center,
        # then fade them out as the larger square fades in at the center.

        # Create copies of small squares and their labels
        s_a_copy = square_a.copy()
        s_b_copy = square_b.copy()
        l_a_copy = area_a_label.copy()
        l_b_copy = area_b_label.copy()

        group_a = VGroup(s_a_copy, l_a_copy)
        group_b = VGroup(s_b_copy, l_b_copy)

        # Fade out original triangle context and hypotenuse square
        self.play(
            FadeOut(triangle, side_labels, square_c_outline, area_c_label),
            ReplacementTransform(square_a, s_a_copy),
            ReplacementTransform(square_b, s_b_copy),
            ReplacementTransform(area_a_label, l_a_copy),
            ReplacementTransform(area_b_label, l_b_copy)
        )
        self.wait(0.5)

        # Move small squares to a central position, side-by-side
        self.play(
            group_a.animate.move_to(LEFT * 2.5),
            group_b.animate.move_to(RIGHT * 2.5)
        )
        self.wait(1)

        # Create the final combined square (c^2)
        final_square_c_combined = Square(
            side_length=len_c
        ).move_to(ORIGIN).set_color(GREEN).set_fill(
            GREEN,
            opacity=0.7
        )

        final_area_c_label_combined = Text("c^2").move_to(
            final_square_c_combined.get_center()
        ).set_color(BLACK)

        # Animate the small squares fading out as the large square fades in
        self.play(
            FadeOut(group_a),
            FadeOut(group_b),
            FadeIn(final_square_c_combined),
            Write(final_area_c_label_combined),
            run_time=2
        )
        self.wait(1)

        # Display the Pythagorean theorem equation
        equation = Text("a^2 + b^2 = c^2")
        equation.next_to(final_square_c_combined, DOWN, buff=0.8)

        self.play(Write(equation))
        self.wait(2)