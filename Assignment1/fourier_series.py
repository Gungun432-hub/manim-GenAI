from manim import *

class FourierSquareWave(Scene):
    def construct(self):
        # 1. Title
        title = Text("Fourier Series of a Square Wave", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 2. Coordinate Axes
        self.axes = Axes(
            x_range=[-PI * 2, PI * 2, PI/2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
            tips=False
        ).scale(0.8).to_edge(DOWN)
        labels = self.axes.get_axis_labels(x_label="x", y_label="f(x)")

        self.play(Create(self.axes), Write(labels))
        self.wait(1)

        # Define harmonic functions
        funcs = [
            lambda x: np.sin(x),
            lambda x: (1/3) * np.sin(3*x),
            lambda x: (1/5) * np.sin(5*x),
            lambda x: (1/7) * np.sin(7*x),
            lambda x: (1/9) * np.sin(9*x),
        ]

        # Define cumulative sum functions
        sum_funcs = [
            funcs[0],
            lambda x: funcs[0](x) + funcs[1](x),
            lambda x: funcs[0](x) + funcs[1](x) + funcs[2](x),
            lambda x: funcs[0](x) + funcs[1](x) + funcs[2](x) + funcs[3](x),
            lambda x: funcs[0](x) + funcs[1](x) + funcs[2](x) + funcs[3](x) + funcs[4](x),
        ]

        # Colors for each harmonic
        harmonic_colors = [RED, GREEN, BLUE, PURPLE, ORANGE]

        # Text labels for harmonics
        harmonic_labels_text = [
            "sin(x)",
            "(1/3)sin(3x)",
            "(1/5)sin(5x)",
            "(1/7)sin(7x)",
            "(1/9)sin(9x)",
        ]

        # Text labels for cumulative sums
        sum_labels_text = [
            "Sum: sin(x)",
            "Sum: sin(x) + (1/3)sin(3x)",
            "Sum: sin(x) + (1/3)sin(3x) + (1/5)sin(5x)",
            "Sum: sin(x) + (1/3)sin(3x) + (1/5)sin(5x) + (1/7)sin(7x)",
            "Sum: sin(x) + (1/3)sin(3x) + (1/5)sin(5x) + (1/7)sin(7x) + (1/9)sin(9x)",
        ]

        # Legend setup
        legend_items_group = VGroup()
        legend_position = RIGHT * 4 + UP * 2.5
        legend_spacing = 0.5

        # Initialize current sum graph and label (starts at zero)
        current_sum_graph = self.axes.plot(lambda x: 0, color=YELLOW, stroke_width=4)
        current_sum_label = Text("Current Sum: 0", font_size=28, color=YELLOW).to_corner(DR)
        self.add(current_sum_graph, current_sum_label)
        self.wait(1)

        # Loop through each harmonic
        for i in range(5):
            harmonic_func = funcs[i]
            sum_func = sum_funcs[i]
            color = harmonic_colors[i]
            harmonic_text_content = harmonic_labels_text[i]
            sum_text_content = sum_labels_text[i]

            # Create individual harmonic graph
            harmonic_graph = self.axes.plot(harmonic_func, color=color)

            # Create temporary label for the current harmonic
            temp_harmonic_label = Text(harmonic_text_content, font_size=24, color=color).to_corner(UL).shift(DOWN * 0.5)

            # Animate showing the harmonic and its temporary label
            self.play(
                Create(harmonic_graph),
                Write(temp_harmonic_label)
            )
            self.wait(1)

            # Update the legend
            line_for_legend = Line(ORIGIN, RIGHT * 0.5, color=color, stroke_width=3)
            item_text = Text(harmonic_text_content, font_size=20, color=WHITE)
            legend_item = VGroup(line_for_legend, item_text).arrange(RIGHT, buff=0.2)
            if i == 0:
                legend_item.move_to(legend_position)
            else:
                legend_item.next_to(legend_items_group[-1], DOWN, buff=legend_spacing, aligned_edge=LEFT)
            self.play(FadeIn(legend_item))
            legend_items_group.add(legend_item)

            # Animate transforming the cumulative sum
            new_sum_graph = self.axes.plot(sum_func, color=YELLOW, stroke_width=4)
            new_sum_label = Text(sum_text_content, font_size=28, color=YELLOW).to_corner(DR)

            self.play(
                ReplacementTransform(current_sum_graph, new_sum_graph),
                ReplacementTransform(current_sum_label, new_sum_label),
                FadeOut(temp_harmonic_label) # Remove temporary harmonic label
            )
            current_sum_graph = new_sum_graph
            current_sum_label = new_sum_label
            self.wait(1.5)

        # Final annotation
        final_annotation = Text(
            "Sum of first 5 odd harmonics approximating a square wave",
            font_size=30,
            color=WHITE
        ).next_to(self.axes, UP, buff=0.5).shift(DOWN*0.5)
        self.play(Write(final_annotation))
        self.wait(2)
        self.play(FadeOut(final_annotation))
        self.wait(0.5)

        # Add "Cumulative Sum" to legend
        line_for_sum_legend = Line(ORIGIN, RIGHT * 0.5, color=YELLOW, stroke_width=4)
        item_text_sum = Text("Cumulative Sum", font_size=20, color=WHITE)
        legend_item_sum = VGroup(line_for_sum_legend, item_text_sum).arrange(RIGHT, buff=0.2)
        legend_item_sum.next_to(legend_items_group[-1], DOWN, buff=legend_spacing, aligned_edge=LEFT)
        self.play(FadeIn(legend_item_sum))
        legend_items_group.add(legend_item_sum)

        self.wait(3)