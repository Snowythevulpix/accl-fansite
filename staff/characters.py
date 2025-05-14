from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# File path to store characters' data
DATA_FILE = 'C:\\Users\\Kaz\\accl-fansite\\staff\\staff.json'

# Function to load existing data from the JSON file
def load_characters():
    if os.path.exists(DATA_FILE):
     with open(DATA_FILE, 'w', encoding='utf-8') as f:
            data = json.load(f)
            app.logger.debug(f"Loaded characters data: {data}")
            return data
    else:
        app.logger.debug(f"Character file {DATA_FILE} does not exist.")
    return []

# Function to save the data back to the JSON file
def save_characters(characters):
    with open(DATA_FILE, 'w') as f:
        json.dump(characters, f, indent=2)
        app.logger.debug(f"Characters saved to {DATA_FILE}: {characters}")

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/save-character', methods=['POST'])
def save_character():
    try:
        # Get the character data from the request
        character_data = request.get_json()
        app.logger.debug(f"Received character data: {character_data}")
        
        if not character_data:
            return jsonify({"error": "No valid JSON data received"}), 400

        # Load existing characters from the file
        characters = load_characters()

        # Ensure the 'id' is treated as an integer when comparing
        char_id = character_data.get('id')

        if char_id is not None:
            # Make sure char_id is an integer
            char_id = int(char_id)
            app.logger.debug(f"Updating character with ID: {char_id}")

            for i, char in enumerate(characters):
                # Ensure that the 'id' in the character list is an integer
                char['id'] = int(char['id'])  # cast id to int

                app.logger.debug(f"Comparing with character ID: {char['id']}")

                if char['id'] == char_id:
                    # Update the existing character
                    characters[i] = character_data
                    save_characters(characters)
                    return jsonify({"message": "Character updated successfully", "id": char_id})

            # If the character ID doesn't exist, return a not found error
            return jsonify({"error": "Character with this ID not found"}), 404

        # If no ID is provided, create a new character with a new ID
        next_id = max([int(char['id']) for char in characters], default=0) + 1  # cast id to int
        character_data['id'] = next_id
        characters.append(character_data)
        save_characters(characters)

        return jsonify({"message": "Character saved successfully", "id": next_id})

    except Exception as e:
        # Log the exception to the Flask console for debugging
        app.logger.error(f"Error in saving character: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/get-character/<int:char_id>', methods=['GET'])
def get_character(char_id):
    try:
        # Load the list of characters
        characters = load_characters()

        app.logger.debug(f"Looking for character with ID: {char_id}")

        # Look for the character with the given ID
        for char in characters:
            app.logger.debug(f"Comparing with character ID: {char['id']}")

            # Ensure we compare as integers
            char['id'] = int(char['id'])  # Cast to int if needed

            if char['id'] == char_id:
                app.logger.debug(f"Character with ID {char_id} found: {char}")
                return jsonify(char)

        # If character with given ID is not found
        app.logger.debug(f"Character with ID {char_id} not found.")
        return jsonify({"error": "Character not found"}), 404

    except Exception as e:
        app.logger.error(f"Error in getting character: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

