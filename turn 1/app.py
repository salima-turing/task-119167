from flask import Flask, render_template
import random

app = Flask(__name__)

VARIANTS = {
	"home": ["home_variant_a.html", "home_variant_b.html"]
}

def get_variant(page_name):
	variants = VARIANTS.get(page_name, [])
	if variants:
		return random.choice(variants)
	return None

@app.route('/')
def home():
	variant = get_variant("home")
	if variant:
		return render_template(variant)
	return "Page not found", 404

if __name__ == '__main__':
	app.run(debug=True)
