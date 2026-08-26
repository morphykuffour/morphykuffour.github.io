"""The mesh-analysis animation behind /math-tricks/.

Renders a three-mesh circuit and builds its resistance matrix a term at a
time: each diagonal is the sum of the resistors around one loop, each
off-diagonal the negative of the resistor two loops share. The point of
animating it rather than writing it out is that the matrix is a picture of
the circuit -- every number in it is a branch you can point at -- and a still
page cannot point.

The circuit is reproduced from a reel by MAE Academy, credited on the page.
Nothing of theirs is copied into this file: the topology and the numbers are
read off their frames, the drawing and the timing are written here, and their
watermark is deliberately absent -- it is their mark, not mine to reproduce.

Portrait, because the composition is a column: title, circuit, working line,
matrix. Laid side by side those four want a screen twice as wide as the
site's text column, and the arithmetic has to sit under the loop it came from
for the animation to read at all.

Rendering:

    manim scripts/mesh_analysis.py MeshMatrix --media_dir /tmp/manim-out

Frame size, resolution and frame rate are set below rather than passed as
flags, so the render is the same wherever it is run from -- module-level
config assignments are applied after the command line is parsed, so a stray
-q would otherwise silently change the shape of the output.

Manim itself is not vendored here. Mine is the fork at github.com/morph-k/manim
(Manim Community v0.21), but any install of that version renders this file;
it needs a LaTeX with dvisvgm alongside it for the matrix.

The video on the page is not this render as it stands: scripts/boomerang.sh
plays it forward and then backward, so it loops without a cut back to black.
"""

from manim import *

# 720x1280 at 30fps, the shape the source reel was cut to. frame_width is the
# width in scene units, so every coordinate below is a fraction of 8 -- and
# frame_height has to be set with it, or the scene is drawn to a 16:9 frame
# and squeezed into a portrait one.
config.pixel_width = 720
config.pixel_height = 1280
config.frame_width = 8.0
config.frame_height = 8.0 * 1280 / 720
config.frame_rate = 30
config.background_color = "#08080C"

# A preamble of our own rather than manim's default one. The stock template
# pulls in a dozen packages -- calligra, physics, tipa, wasysym -- for symbols
# nothing here uses, and each one is a package a TeX install has to have
# before this file renders at all. Three packages and a document class is the
# whole of what a matrix of numbers needs, and it renders on a small texlive.
config.tex_template = TexTemplate(
    documentclass=r"\documentclass[preview]{standalone}",
    preamble="\n".join([
        r"\usepackage{amsmath}",
        r"\usepackage{amssymb}",
        r"\usepackage{xcolor}",
    ]),
)

WIRE = "#D8D8DC"
OHM = "#F2C94C"          # the resistor labels
SRC = "#31C5D2"          # the source, and the voltage vector it fills
I1C = "#2F80ED"          # mesh 1, and everything that comes from it
I2C = "#A85CF9"          # mesh 2
I3C = "#EB2F72"          # mesh 3
TITLE = "#E8541F"
OFFD = "#4CD5B0"         # the off-diagonals: shared, so neither mesh's colour

# The rectangle the circuit is drawn on. Three verticals and three horizontals
# out of these six numbers, which is what keeps the meshes square: the middle
# horizontal only spans the right half, and that is the whole topology.
XL, XM, XR = -2.85, 0.10, 2.85
YT, YM, YB = 4.15, 2.30, 0.45


def resistor(start, end, zigs=7, amp=0.13, lead=0.30):
    """A resistor drawn as a zigzag in the middle of the segment start..end.

    Written rather than taken from a symbol library because manim has no
    circuit primitives, and a zigzag between two points is nine lines of
    vector arithmetic. The leads at either end are what let the same helper
    sit on a vertical, a horizontal, or neither: the body is centred on the
    segment and the wire runs into it from both sides.
    """
    a, b = np.array(start, dtype=float), np.array(end, dtype=float)
    span = b - a
    length = np.linalg.norm(span)
    unit = span / length
    perp = np.array([-unit[1], unit[0], 0.0])
    body = length - 2 * lead

    points = [a, a + unit * lead]
    for i in range(zigs):
        along = lead + body * (i + 0.5) / zigs
        points.append(a + unit * along + perp * (amp if i % 2 == 0 else -amp))
    points += [b - unit * lead, b]

    line = VMobject(stroke_color=WIRE, stroke_width=3.2)
    line.set_points_as_corners(points)
    return line


def battery(start, end, gap=0.13, long=0.30, short=0.17):
    """A single cell on the segment start..end, long plate towards `end`.

    Which plate is which is not decoration: the long plate is the positive
    terminal, and putting it at the top of the left branch is what makes the
    source drive the left mesh clockwise -- the same direction the three loop
    arrows are drawn, which is in turn why every off-diagonal below comes out
    negative and the voltage vector comes out +16 rather than -16.
    """
    a, b = np.array(start, dtype=float), np.array(end, dtype=float)
    unit = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-unit[1], unit[0], 0.0])
    mid = (a + b) / 2

    lo, hi = mid - unit * gap, mid + unit * gap
    return VGroup(
        Line(a, lo, stroke_color=WIRE, stroke_width=3.2),
        Line(lo - perp * short, lo + perp * short, stroke_color=WIRE, stroke_width=3.2),
        Line(hi - perp * long, hi + perp * long, stroke_color=WIRE, stroke_width=3.2),
        Line(hi, b, stroke_color=WIRE, stroke_width=3.2),
    )


def loop_arrow(centre, colour, radius=0.48):
    """A mesh current: a nearly-closed circle with a head on it.

    Swept negative, which is clockwise, so the head lands on the left of the
    circle pointing up. All three are drawn the same way round on purpose --
    mesh analysis only gives a symmetric matrix if every loop is traversed in
    the same direction, and a reader who cannot see that in the picture has
    to take the minus signs on trust.
    """
    arc = Arc(
        radius=radius,
        start_angle=PI * 0.62,
        angle=-TAU * 0.80,
        arc_center=np.array([*centre, 0.0]) if len(centre) == 2 else np.array(centre),
        stroke_color=colour,
        stroke_width=4,
    )
    arc.add_tip(tip_length=0.20, tip_width=0.18)
    return arc


class MeshMatrix(Scene):
    def construct(self):
        title = (
            VGroup(
                Tex("Mesh Analysis", color=TITLE),
                Tex("Matrix Setup", color=TITLE),
            )
            .arrange(DOWN, buff=0.18)
            .scale(1.05)
            .to_edge(UP, buff=0.75)
        )

        circuit, parts = self.build_circuit()
        arrows = VGroup(
            loop_arrow(((XL + XM) / 2, (YB + YT) / 2), I1C),
            loop_arrow(((XM + XR) / 2, (YM + YT) / 2 + 0.05), I2C, radius=0.40),
            loop_arrow(((XM + XR) / 2, (YB + YM) / 2 - 0.05), I3C, radius=0.40),
        )
        # Clear of the circle rather than on it: at 0.62 the label sat on the
        # stroke and the two read as one smudge at this height.
        arrow_labels = VGroup(
            MathTex("I_1", color=I1C).scale(0.70).move_to(arrows[0]).shift(RIGHT * 0.86),
            MathTex("I_2", color=I2C).scale(0.70).move_to(arrows[1]).shift(RIGHT * 0.78),
            MathTex("I_3", color=I3C).scale(0.70).move_to(arrows[2]).shift(RIGHT * 0.78),
        )

        self.play(Write(title), run_time=1.0)
        self.play(Create(circuit), run_time=1.6)
        self.play(*[Create(a) for a in arrows], *[FadeIn(l) for l in arrow_labels],
                  run_time=0.9)

        equation, R, I, V = self.build_equation()
        caption = Tex("Step 1: Calculating Resistance Matrix [R]", color=OHM)
        caption.scale(0.58).move_to([0, -0.55, 0])

        self.play(FadeIn(caption, shift=UP * 0.15), FadeIn(equation), run_time=0.9)

        # The diagonals. Each one is a loop lit up and the resistors around it
        # added, so the sum on screen is read off the picture above it rather
        # than asserted underneath it.
        for entry, mesh, colour, sum_tex, value in [
            (0, "m1", I1C, "10 + 6 + 8 = 24", "24"),
            (4, "m2", I2C, "6 + 5 + 9 = 20", "20"),
            (8, "m3", I3C, "8 + 5 + 12 = 25", "25"),
        ]:
            patch = self.lit(parts[mesh], colour, 0.28)
            working = MathTex(sum_tex, color=colour).scale(0.72).move_to([0, -1.55, 0])
            self.play(FadeIn(patch), Write(working), run_time=0.7)
            self.replace_entry(R, entry, value, OHM)
            self.wait(0.25)
            self.play(FadeOut(patch), FadeOut(working), run_time=0.35)

        # The off-diagonals. Two meshes lit at once and the branch they share
        # flashed between them -- which is the whole content of the minus sign,
        # since the two currents run through that branch in opposite directions.
        for entries, meshes, shared, value in [
            ((1, 3), (("m1", I1C), ("m2", I2C)), "r6", "-6"),
            ((2, 6), (("m1", I1C), ("m3", I3C)), "r8", "-8"),
            ((5, 7), (("m2", I2C), ("m3", I3C)), "r5", "-5"),
        ]:
            patches = VGroup(*[self.lit(parts[m], c, 0.24) for m, c in meshes])
            working = MathTex(value, color=OFFD).scale(0.78).move_to([0, -1.55, 0])
            self.play(FadeIn(patches), Write(working), run_time=0.6)
            self.play(parts[shared].animate.set_stroke(OFFD, width=5.5), run_time=0.3)
            for entry in entries:
                self.replace_entry(R, entry, value, OFFD, run_time=0.35)
            self.play(parts[shared].animate.set_stroke(WIRE, width=3.2),
                      FadeOut(patches), FadeOut(working), run_time=0.35)

        # The voltage vector. Only the mesh the source sits in gets a term,
        # which is why two of the three entries are a zero worth showing.
        step2 = Tex("Step 2: Calculating Voltage Vector [V]", color=SRC)
        step2.scale(0.58).move_to(caption)
        self.play(FadeOut(caption), FadeIn(step2), run_time=0.5)
        self.play(parts["src"].animate.set_stroke(SRC, width=5), run_time=0.4)
        self.replace_entry(V, 0, "16", SRC)
        self.play(parts["src"].animate.set_stroke(WIRE, width=3.2), run_time=0.3)
        for entry in (1, 2):
            self.replace_entry(V, entry, "0", SRC, run_time=0.3)

        solved = Tex("After Solving \\ldots", color=TITLE).scale(0.62).move_to(caption)
        self.play(FadeOut(step2), FadeIn(solved), run_time=0.6)
        self.wait(0.5)

        answers = (
            VGroup(
                MathTex(r"I_1 \approx 0.870~\text{A}", color=I1C),
                MathTex(r"I_2 \approx 0.348~\text{A}", color=I2C),
                MathTex(r"I_3 \approx 0.348~\text{A}", color=I3C),
            )
            .arrange(DOWN, buff=0.45)
            .scale(0.95)
            # Up from where the matrix sat: with the caption gone too, three
            # short lines at the matrix's height leave the frame bottom-heavy.
            .move_to([0, -3.0, 0])
        )
        self.play(FadeOut(equation, shift=DOWN * 0.3), FadeOut(solved), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(a, shift=UP * 0.2) for a in answers],
                              lag_ratio=0.35), run_time=1.5)
        self.wait(1.2)

    @staticmethod
    def lit(mesh, colour, opacity):
        """A mesh area filled in, and pushed behind the drawing.

        Behind rather than over: at the default z-index the patch is painted
        after the circuit and swallows anything of it inside the loop -- the
        5 ohm label sits just inside mesh 2 and disappeared under it.
        """
        patch = mesh.copy().set_fill(colour, opacity=opacity).set_stroke(width=0)
        patch.set_z_index(-10)
        return patch

    def replace_entry(self, matrix, index, value, colour, run_time=0.45):
        """Swap one entry of a matrix for its solved value, in place.

        Transform rather than a second matrix drawn over the first: the
        brackets and the eleven entries that are not changing stay the same
        mobjects, so nothing shifts under the one that is. Transform rather
        than ReplacementTransform for the same reason -- the entry is a
        descendant of the matrix, and replacing it would take it out of the
        group and leave the new one floating at the top of the scene.

        The replacement is built at the matrix's own scale rather than fitted
        to the box it lands in: `24` has no subscript and `R_{11}` does, so
        matching heights would set the number a third larger than its
        neighbours.
        """
        old = matrix.get_entries()[index]
        new = MathTex(value, color=colour).scale(self.entry_scale).move_to(old)
        self.play(Transform(old, new), run_time=run_time)

    def build_circuit(self):
        """The drawing, plus the handful of pieces the animation lights up.

        The dict is what the two loops in construct() reach for -- the three
        mesh rectangles, the three shared resistors and the source. They are
        returned rather than found again by position because a resistor is a
        zigzag among a dozen zigzags, and looking one up by where it happens
        to sit is a bug waiting for the first time the layout moves.
        """
        wires = VGroup(
            Line([XL, YT, 0], [XR, YT, 0]),
            Line([XL, YB, 0], [XR, YB, 0]),
            Line([XM, YM, 0], [XR, YM, 0]),
        ).set_stroke(WIRE, 3.2)

        r10 = resistor([XL, YT, 0], [XL, YM, 0])
        src = battery([XL, YB, 0], [XL, YM, 0])
        r6 = resistor([XM, YT, 0], [XM, YM, 0])
        r8 = resistor([XM, YM, 0], [XM, YB, 0])
        r9 = resistor([XR, YT, 0], [XR, YM, 0])
        r12 = resistor([XR, YM, 0], [XR, YB, 0])
        r5 = resistor([XM, YM, 0], [XR, YM, 0], zigs=5, amp=0.11, lead=0.62)

        labels = VGroup(
            MathTex(r"10\Omega", color=OHM).scale(0.55).next_to(r10, LEFT, buff=0.12),
            MathTex(r"16\text{V}", color=SRC).scale(0.55).next_to(src, LEFT, buff=0.12),
            MathTex(r"6\Omega", color=OHM).scale(0.55).next_to(r6, LEFT, buff=0.12),
            MathTex(r"8\Omega", color=OHM).scale(0.55).next_to(r8, LEFT, buff=0.12),
            MathTex(r"9\Omega", color=OHM).scale(0.55).next_to(r9, RIGHT, buff=0.12),
            MathTex(r"12\Omega", color=OHM).scale(0.55).next_to(r12, RIGHT, buff=0.12),
            # Further off its resistor than the rest are off theirs: this is
            # the one label sitting above a zigzag rather than beside one, and
            # at the others' buff it lands in the teeth.
            MathTex(r"5\Omega", color=OHM).scale(0.6).next_to(r5, UP, buff=0.26),
        )

        circuit = VGroup(wires, r10, src, r6, r8, r9, r12, r5, labels)

        # The three mesh areas, kept unfilled and invisible: they exist to be
        # copied and lit, never drawn as themselves.
        def mesh(x0, x1, y0, y1):
            return Rectangle(width=x1 - x0, height=y1 - y0).move_to(
                [(x0 + x1) / 2, (y0 + y1) / 2, 0]
            ).set_stroke(width=0).set_fill(opacity=0)

        parts = {
            "m1": mesh(XL, XM, YB, YT),
            "m2": mesh(XM, XR, YM, YT),
            "m3": mesh(XM, XR, YB, YM),
            "r6": r6,
            "r8": r8,
            "r5": r5,
            "src": src,
        }
        return circuit, parts

    def build_equation(self):
        """[R][I] = [V], symbolic to start with and filled in as it goes."""
        R = Matrix(
            [["R_{11}", "R_{12}", "R_{13}"],
             ["R_{21}", "R_{22}", "R_{23}"],
             ["R_{31}", "R_{32}", "R_{33}"]],
            h_buff=1.5,
        )
        I = Matrix([["I_1"], ["I_2"], ["I_3"]])
        V = Matrix([["V_1"], ["V_2"], ["V_3"]])
        equals = MathTex("=")

        equation = VGroup(R, I, equals, V).arrange(RIGHT, buff=0.14)
        # Scaled to the frame rather than authored at a chosen size: the
        # symbolic entries are the widest this ever gets, so fitting them
        # fits every value that later replaces them. The factor is kept
        # because replace_entry needs it -- an entry built afterwards has to
        # be set at the size the rest of the matrix ended up at.
        target = config.frame_width - 0.7
        self.entry_scale = target / equation.width
        equation.scale_to_fit_width(target)
        equation.move_to([0, -3.9, 0])
        return equation, R, I, V
