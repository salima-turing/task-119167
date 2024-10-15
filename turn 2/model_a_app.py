
from flask import Flask, render_template, request, make_response, jsonify
import random
import uuid

app = Flask(__name__)

VARIANTS = {
	"home": ["home_variant_a.html", "home_variant_b.html"]
}

TEST_RESULTS = {}

def get_variant(page_name):
	variants = VARIANTS.get(page_name, [])
	if variants:
		return random.choice(variants)
	return None

def get_user_id():
	user_id = request.cookies.get('user_id')
	if not user_id:
		user_id = str(uuid.uuid4())
		response = make_response(render_template(variant))
		response.set_cookie('user_id', user_id)
	return user_id

@app.route('/')
def home():
	variant = get_variant("home")
	if variant:
		user_id = get_user_id()
		TEST_RESULTS.setdefault(user_id, {"variant": variant, "clicks": 0})
		return render_template(variant)
	return "Page not found", 404

@app.route('/track_click', methods=['POST'])
def track_click():
	user_id = get_user_id()
	if user_id in TEST_RESULTS:
		TEST_RESULTS[user_id]['clicks'] += 1
	return jsonify({'message': 'Click tracked'})

@app.route('/results')
def show_results():
	variant_a_count = sum(1 for res in TEST_RESULTS.values() if res["variant"] == "home_variant_a.html")
	variant_b_count = sum(1 for res in TEST_RESULTS.values() if res["variant"] == "home_variant_b.html")

	variant_a_clicks = sum(res["clicks"] for res in TEST_RESULTS.values() if res["variant"] == "home_variant_a.html")
	variant_b_clicks = sum(res["clicks"] for res in TEST_RESULTS.values() if res["variant"] == "home_variant_b.html")

	test_result = {}
	if variant_a_count > 0:
		test_result['Variant A CTR'] = f"{variant_a_clicks / variant_a_count * 100:.2f}%"
	if variant_b_count > 0:
		test_result['Variant B CTR'] = f"{variant_b_clicks / variant_b_count * 100:.2f}%"

	return jsonify(test_result)

if __name__ == '__main__':
	app.run(debug=True)
