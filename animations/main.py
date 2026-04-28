from manim import *

HIGHLIGHT = BLUE
DEFAULT = BLACK
DISTANCE = 1.8

class Pipeline:
    def __init__(self, passes):
        self.passes = passes
        self.boxes = VGroup()
        self.arrows = VGroup()
        self.arrow_labels = VGroup()
        self.sequence = []

        # -----------------------
        # 1. Create boxes
        # -----------------------
        previous = None
        for i in range(passes):
            box = Rectangle(color=DEFAULT, width=2, height=4)
            label = Text(str(i), color=DEFAULT).move_to(box.get_center())
            group = VGroup(box, label)

            if previous is not None:
                group.next_to(previous, RIGHT, buff=DISTANCE)

            self.boxes.add(group)
            self.sequence.append(group)
            previous = group

        # -----------------------
        # 2. Create arrows (between boxes)
        # -----------------------
        for i in range(1, passes):
            left_box = self.sequence[i - 1]
            right_box = self.sequence[i]

            arrow = Arrow(
                left_box[0].get_right(),
                right_box[0].get_left(),
                color=DEFAULT,
                buff=0
            )
            self.arrows.add(arrow)

        # -----------------------
        # 3. Create arrow labels (outgoing from each box)
        # -----------------------
        for i, arrow in enumerate(self.arrows):
            arrow_label = MathTex(
                f"(G_{{{i}}}", f"p_{{{i}}}", ")",
                color=DEFAULT
            ).scale(1)

            arrow_label.next_to(arrow, UP, buff=0.1)
            self.arrow_labels.add(arrow_label)

        # -----------------------
        # Input / Output arrows
        # -----------------------
        first = self.sequence[0]
        last = self.sequence[-1]

        self.input_arrow = Arrow(
            first[0].get_left() + LEFT * DISTANCE,
            first[0].get_left(),
            color=DEFAULT,
            buff=0
        )

        self.input_label = MathTex("(G,p)", color=DEFAULT)
        self.input_label.next_to(self.input_arrow, LEFT, buff=0.2)

        self.output_arrow = Arrow(
            last[0].get_right(),
            last[0].get_right() + RIGHT * DISTANCE,
            color=DEFAULT,
            buff=0
        )

        self.output_label = MathTex("(", "G'", ",", "p'", ")", color=DEFAULT)
        self.output_label.next_to(self.output_arrow, RIGHT, buff=0.2)

        self.mobjects = VGroup(
            self.input_arrow,
            self.input_label,
            self.boxes,
            self.arrows,
            self.arrow_labels,
            self.output_arrow,
            self.output_label
        )

    # -----------------------
    # Draw structure
    # -----------------------
    def draw(self, scene):
        animations = []

        animations.append(Create(self.input_arrow))
        animations += [Create(box) for box in self.boxes]
        animations += [Create(arrow) for arrow in self.arrows]
        animations.append(Create(self.output_arrow))

        scene.play(
            AnimationGroup(*animations, lag_ratio=0.2),
            run_time=2
        )

    # -----------------------
    # Linear animation
    # -----------------------
    def animate(self, scene, run_time=0.5):
        scene.play(Write(self.input_label), run_time=run_time)

        # propagate through pipeline
        for i in range(0, len(self.sequence)):            
            box = self.sequence[i]
            color = RED if i >= 3 else BLUE

            if i < 9:
                arrow_label = self.arrow_labels[i]
                scene.play(Write(arrow_label), run_time=run_time)

            scene.play(
                box[0].animate.set_color(color),
                box[1].animate.set_color(color),
                arrow_label[1].animate.set_color(color),
                run_time=run_time
            )

            scene.play(
                box[0].animate.set_color(DEFAULT),
                box[1].animate.set_color(DEFAULT),
                run_time=run_time
            )

        scene.play(Write(self.output_label), run_time=run_time)
        return (self.output_arrow, self.output_label)

    def animate_binary(self, scene, run_time=0.4):
        order = []
        l, r = 0, self.passes - 1

        # Initial pointers
        l_label = MathTex(f"l={l}", color=BLUE)
        r_label = MathTex(f"r={r}", color=RED)

        l_label.next_to(self.sequence[l], UP, buff=0.3)
        r_label.next_to(self.sequence[r], UP, buff=0.3)

        scene.play(Write(l_label), Write(r_label))

        while l != r - 1:
            m = (l + r) // 2
            order.append(m)

            box = self.sequence[m]

            # Highlight midpoint
            scene.play(
                box[0].animate.set_color(ORANGE),
                box[1].animate.set_color(ORANGE),
                run_time=run_time
            )

            if m > 2:
                new_r = m

                new_r_label = MathTex(f"r={new_r}", color=RED)
                new_r_label.next_to(self.sequence[new_r], UP, buff=0.3)

                scene.play(
                    FadeOut(r_label),
                    FadeIn(new_r_label),
                    run_time=run_time
                )

                r = new_r
                r_label = new_r_label

            else:
                new_l = m

                new_l_label = MathTex(f"l={new_l}", color=BLUE)
                new_l_label.next_to(self.sequence[new_l], UP, buff=0.3)

                scene.play(
                    FadeOut(l_label),
                    FadeIn(new_l_label),
                    run_time=run_time
                )

                l = new_l
                l_label = new_l_label

            # Reset midpoint
            scene.play(
                box[0].animate.set_color(DEFAULT),
                box[1].animate.set_color(DEFAULT),
                run_time=run_time
            )

class Animation(MovingCameraScene):
    def construct(self):
        # Setup
        pipeline = Pipeline(10)
        pipeline.mobjects.move_to(ORIGIN)
        frame = self.camera.frame
        frame.scale(3.3)
        initial_frame = frame.copy()

        # First phase
        pipeline.draw(self)
        self.wait(1)
        
        # Zoom on faulty pass
        pass_3 = pipeline.sequence[3]
        self.play(
            frame.animate.move_to(pass_3).set(width=pass_3.width * 10)
        )
        self.wait(1)
        # Blink
        for _ in range(0,2):
            self.play(
                pass_3.animate.set_color(RED),
                run_time=0.3
            )
            self.play(
                pass_3.animate.set_color(DEFAULT),
                run_time=0.3
            )

        self.wait(1)

        # Reset camera
        self.play(Transform(self.camera.frame, initial_frame))

        self.wait(1)

        # Simulate pipeline execution
        output_arrow, output_label = pipeline.animate(self, run_time=0.4)
        # zoom into output
        self.play(
            frame.animate.move_to(output_label).set(width=output_label.width * 5)
        )

        comparison = MathTex("p'", r"\neq q \to", "m", color=DEFAULT)
        comparison[0].set_color(RED)
        comparison.next_to(output_arrow, RIGHT, buff=0.2)

        self.play(
            Transform(output_label, comparison),
            run_time=1
        )

        self.wait(1)

        # Reset camera
        self.play(Transform(self.camera.frame, initial_frame))

        self.wait(1)

        pipeline.animate_binary(self)