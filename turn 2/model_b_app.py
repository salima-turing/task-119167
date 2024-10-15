from flask import Flask, render_template, session, request, jsonify
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'  # Set a secret key for sessions

VARIANTS = {
    "home": ["home_variant_a.html", "home_variant_b.html"]
}

def get_variant(page_name):
    variants = VARIANTS.get(page_name, [])
    if variants:
        selected_variant = session.get(f'variant_{page_name}')
        if not selected_variant:
            selected_variant = random.choice(variants)
            session[f'variant_{page_name}'] = selected_variant
        return selected_variant
    return None

@app.route('/')
def home():
    variant = get_variant("home")
    if variant:
        return render_template(variant)
    return "Page not found", 404

@app.route('/track', methods=['POST'])
def track_interaction():
    page_name = request.json.get('page_name')
    interaction_type = request.json.get('interaction_type')  # Define different interaction types like 'click', 'form_submit', etc.
    variant = session.get(f'variant_{page_name}')

    # Store the interaction and result in a database or data storage
    # For simplicity, let's use a list in memory for demonstration purposes
    if not hasattr(app, 'interaction_data'):
        app.interaction_data = []
    app.interaction_data.append({
        'variant': variant,
        'page_name': page_name,
        'interaction_type': interaction_type
    })

    return jsonify({'message': 'Interaction tracked successfully'})

if __name__ == '__main__':
    app.run(debug=True)
