
from flask import Flask, render_template
from flask_ab import AB, Experiment

app = Flask(__name__)
ab = AB(app)

# Define your experiments and variants
@ab.experiment(name="Homepage Layout")
def homepage_layout():
    @ab.variant(name="Control")
    def control():
        return render_template("homepage_control.html")

    @ab.variant(name="Variant 1")
    def variant1():
        return render_template("homepage_variant1.html")

    @ab.variant(name="Variant 2")
    def variant2():
        return render_template("homepage_variant2.html")

@ab.experiment(name="Blog Post Section")
def blog_post_section():
    @ab.variant(name="Control")
    def control():
        return render_template("blog_post_control.html")

    @ab.variant(name="Variant with New Feature")
    def variant_with_new_feature():
        return render_template("blog_post_variant_with_new_feature.html")

@app.route('/')
def homepage():
    experiment = ab.get_experiment("Homepage Layout")
    variant = experiment.get_variant()
    return variant()

if __name__ == "__main__":
    app.run(debug=True)
