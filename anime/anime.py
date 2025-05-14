from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# File path to store Animes' data
DATA_FILE = 'C:\\Users\\Kaz\\accl-fansite\\Anime\\anime.json'

# Function to load existing data from the JSON file
def load_Animes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            app.logger.debug(f"Loaded Animes data: {data}")
            return data
    else:
        app.logger.debug(f"Anime file {DATA_FILE} does not exist.")
    return []

# Function to save the data back to the JSON file
def save_Animes(Animes):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(Animes, f, indent=2, ensure_ascii=False)  # include ensure_ascii=False if you want Unicode (e.g., Japanese text) preserved
        app.logger.debug(f"Animes saved to {DATA_FILE}: {Animes}")


@app.route('/')
def index():
    return render_template('template.html')

@app.route('/save-Anime', methods=['POST'])
def save_Anime():
    try:
        # Get the Anime data from the request
        Anime_data = request.get_json()
        app.logger.debug(f"Received Anime data: {Anime_data}")
        
        if not Anime_data:
            return jsonify({"error": "No valid JSON data received"}), 400

        # Load existing Animes from the file
        Animes = load_Animes()

        # Ensure the 'id' is treated as an integer when comparing
        char_id = Anime_data.get('id')

        if char_id is not None:
            # Make sure char_id is an integer
            char_id = int(char_id)
            app.logger.debug(f"Updating Anime with ID: {char_id}")

            for i, char in enumerate(Animes):
                # Ensure that the 'id' in the Anime list is an integer
                char['id'] = int(char['id'])  # cast id to int

                app.logger.debug(f"Comparing with Anime ID: {char['id']}")

                if char['id'] == char_id:
                    # Update the existing Anime
                    Animes[i] = Anime_data
                    save_Animes(Animes)
                    return jsonify({"message": "Anime updated successfully", "id": char_id})

            # If the Anime ID doesn't exist, return a not found error
            return jsonify({"error": "Anime with this ID not found"}), 404

        # If no ID is provided, create a new Anime with a new ID
        next_id = max([int(char['id']) for char in Animes], default=0) + 1  # cast id to int
        Anime_data['id'] = next_id
        Animes.append(Anime_data)
        save_Animes(Animes)

        return jsonify({"message": "Anime saved successfully", "id": next_id})

    except Exception as e:
        # Log the exception to the Flask console for debugging
        app.logger.error(f"Error in saving Anime: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/get-Anime/<int:char_id>', methods=['GET'])
def get_Anime(char_id):
    try:
        # Load the list of Animes
        Animes = load_Animes()

        app.logger.debug(f"Looking for Anime with ID: {char_id}")

        # Look for the Anime with the given ID
        for char in Animes:
            app.logger.debug(f"Comparing with Anime ID: {char['id']}")

            # Ensure we compare as integers
            char['id'] = int(char['id'])  # Cast to int if needed

            if char['id'] == char_id:
                app.logger.debug(f"Anime with ID {char_id} found: {char}")
                return jsonify(char)

        # If Anime with given ID is not found
        app.logger.debug(f"Anime with ID {char_id} not found.")
        return jsonify({"error": "Anime not found"}), 404

    except Exception as e:
        app.logger.error(f"Error in getting Anime: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

