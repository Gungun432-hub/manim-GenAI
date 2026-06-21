from manim import *
import numpy as np

class PythagoreanTheoremProof(Scene):
    def construct(self):
        # Set background and configuration
        self.camera.background_color = "#0f0f0f"
        
        # ========== TITLE ==========
        title = Text("Visualisation of the Pythagorean Theorem", font_size=48)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # ========== SETUP RIGHT TRIANGLE ==========
        # Using 3-4-5 triangle for exact dimensions
        a, b = 3, 4
        c = 5  # Hypotenuse

        # Triangle vertices
        p1 = ORIGIN
        p2 = np.array([b, 0, 0])      # Right point (horizontal)
        p3 = np.array([0, a, 0])      # Top point (vertical)

        # Create triangle
        triangle = Polygon(p1, p2, p3, color=WHITE, stroke_width=3)
        
        # Right angle indicator
        right_angle_size = 0.4
        right_angle_square = Polygon(
            p1,
            p1 + np.array([right_angle_size, 0, 0]),
            p1 + np.array([right_angle_size, right_angle_size, 0]),
            p1 + np.array([0, right_angle_size, 0]),
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.3,
            stroke_width=2
        )

        self.play(
            Create(triangle),
            Create(right_angle_square),
            run_time=1.5
        )
        self.wait(0.5)

        # ========== SIDE LABELS ==========
        label_a = Text("a", font_size=32, color=BLUE).next_to(
            (p1 + p3) / 2, LEFT, buff=0.3
        )
        label_b = Text("b", font_size=32, color=RED).next_to(
            (p1 + p2) / 2, DOWN, buff=0.3
        )
        label_c = Text("c", font_size=32, color=GREEN).next_to(
            (p2 + p3) / 2, UR, buff=0.4
        )

        side_labels = VGroup(label_a, label_b, label_c)
        self.play(Write(side_labels), run_time=1)
        self.wait(0.3)

        # ========== CONSTRUCT SQUARES ==========
        # Square on side 'a' (vertical, left side)
        square_a = Polygon(
            p1,
            p3,
            p3 + np.array([-a, 0, 0]),
            p1 + np.array([-a, 0, 0]),
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.6,
            stroke_width=2
        )

        # Square on side 'b' (horizontal, bottom side)
        square_b = Polygon(
            p1,
            p2,
            p2 + np.array([0, -b, 0]),
            p1 + np.array([0, -b, 0]),
            color=RED,
            fill_color=RED,
            fill_opacity=0.6,
            stroke_width=2
        )

        # Square on side 'c' (hypotenuse)
        # Calculate perpendicular vector to hypotenuse
        hyp_vector = p3 - p2
        hyp_length = np.linalg.norm(hyp_vector)
        hyp_unit = hyp_vector / hyp_length
        perp_unit = np.array([-hyp_unit[1], hyp_unit[0], 0])
        perp_vec = perp_unit * hyp_length

        square_c = Polygon(
            p2,
            p3,
            p3 + perp_vec,
            p2 + perp_vec,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=0.6,
            stroke_width=2
        )

        # Display squares
        self.play(
            Create(square_a),
            Create(square_b),
            Create(square_c),
            run_time=1.5
        )
        self.wait(0.5)

        # ========== AREA LABELS ==========
        area_a = Text("a²", font_size=28, color=BLACK, weight=BOLD).move_to(
            square_a.get_center()
        )
        area_b = Text("b²", font_size=28, color=BLACK, weight=BOLD).move_to(
            square_b.get_center()
        )
        area_c = Text("c²", font_size=28, color=BLACK, weight=BOLD).move_to(
            square_c.get_center()
        )

        area_labels = VGroup(area_a, area_b, area_c)
        self.play(Write(area_labels), run_time=1)
        self.wait(1)

        # ========== TRANSITION: HIGHLIGHT AND COMBINE ==========
        # Add explanation text
        explanation = Text(
            "The sum of the two smaller squares equals the larger square",
            font_size=24
        ).to_edge(DOWN, buff=0.5)

        self.play(Write(explanation), run_time=1.5)
        self.wait(1)

        # Highlight the small squares
        self.play(
            square_a.animate.set_stroke(BLUE, width=4),
            square_b.animate.set_stroke(RED, width=4),
            run_time=0.8
        )
        self.wait(0.5)

        # Highlight the large square
        self.play(
            square_c.animate.set_stroke(GREEN, width=4),
            run_time=0.8
        )
        self.wait(1)

        # ========== FINAL EQUATION ==========
        # Fade out the complex diagram
        self.play(
            FadeOut(explanation),
            run_time=0.5
        )

        # Scale everything down and reposition
        diagram_group = VGroup(
            triangle, right_angle_square,
            square_a, square_b, square_c,
            label_a, label_b, label_c,
            area_a, area_b, area_c
        )

        self.play(
            diagram_group.animate.scale(0.6).to_edge(LEFT, buff=0.5),
            run_time=1.5
        )
        self.wait(0.5)

        # Display theorem equation
        equation_box = VGroup(
            Text("a² + b² = c²", font_size=54, color=WHITE, weight=BOLD),
        )
        equation_box.to_edge(RIGHT, buff=1)

        self.play(Write(equation_box[0]), run_time=1.5)
        self.wait(1)

        # Add numerical example
        numerical = Text(
            "3² + 4² = 5²\n9 + 16 = 25",
            font_size=32,
            color=YELLOW
        ).next_to(equation_box[0], DOWN, buff=0.5)

        self.play(Write(numerical), run_time=1.5)
        self.wait(2)

        # Final emphasis
        self.play(
            equation_box[0].animate.set_color(TEAL).scale(1.1),
            run_time=1
        )
        self.wait(1)