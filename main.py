import sys
import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# Path to the script content JSON file
SCRIPT_CONTENT_PATH = os.path.join(app.static_folder, 'script_content.json')

def load_script_content():
    """Load the script content from the JSON file."""
    try:
        with open(SCRIPT_CONTENT_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading script content: {e}")
        return {}

def save_script_content(content):
    """Save the script content to the JSON file."""
    try:
        with open(SCRIPT_CONTENT_PATH, 'w') as f:
            json.dump(content, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving script content: {e}")
        return False

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/script', methods=['GET'])
def get_script():
    """API endpoint to get the script content."""
    return jsonify(load_script_content())

@app.route('/api/script', methods=['POST'])
def update_script():
    """API endpoint to update the script content."""
    content = request.json
    success = save_script_content(content)
    return jsonify({"success": success})

@app.route('/api/script/section/<section>/button/<button_name>', methods=['POST'])
def update_section_button(section, button_name):
    """API endpoint to update a specific button in a section."""
    content = load_script_content()
    data = request.json
    
    if section in content:
        if button_name not in content[section] and not data.get('content'):
            return jsonify({"success": False, "error": "Button not found and no content provided"}), 400
        
        content[section][button_name] = data['content']
        success = save_script_content(content)
        return jsonify({"success": success})
    
    return jsonify({"success": False, "error": "Section not found"}), 404

@app.route('/api/script/section/<section>/button', methods=['POST'])
def add_section_button(section):
    """API endpoint to add a new button to a section."""
    content = load_script_content()
    data = request.json
    
    if section in content:
        if not data.get('name') or not data.get('content'):
            return jsonify({"success": False, "error": "Button name and content are required"}), 400
        
        button_name = data['name']
        if button_name in content[section]:
            return jsonify({"success": False, "error": "Button already exists"}), 400
        
        content[section][button_name] = data['content']
        success = save_script_content(content)
        return jsonify({"success": success})
    
    return jsonify({"success": False, "error": "Section not found"}), 404

@app.route('/api/script/section/<section>/button/<button_name>', methods=['DELETE'])
def delete_section_button(section, button_name):
    """API endpoint to delete a button from a section."""
    content = load_script_content()
    
    if section in content:
        if button_name not in content[section]:
            return jsonify({"success": False, "error": "Button not found"}), 404
        
        if button_name == 'default':
            return jsonify({"success": False, "error": "Cannot delete default button"}), 400
        
        del content[section][button_name]
        success = save_script_content(content)
        return jsonify({"success": success})
    
    return jsonify({"success": False, "error": "Section not found"}), 404

@app.route('/api/script/objection/<name>', methods=['POST'])
def update_objection(name):
    """API endpoint to update a specific objection."""
    content = load_script_content()
    data = request.json
    
    if 'objections' in content and name in content['objections']:
        content['objections'][name] = data['content']
        success = save_script_content(content)
        return jsonify({"success": success})
    
    return jsonify({"success": False, "error": "Objection not found"}), 404

@app.route('/api/script/objection', methods=['POST'])
def add_objection():
    """API endpoint to add a new objection."""
    content = load_script_content()
    data = request.json
    
    if 'objections' in content and data.get('name') and data.get('content'):
        content['objections'][data['name']] = data['content']
        success = save_script_content(content)
        return jsonify({"success": success})
    
    return jsonify({"success": False, "error": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
