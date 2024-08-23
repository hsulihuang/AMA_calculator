from flask import Flask, request, jsonify, render_template # type: ignore
import pandas as pd # type: ignore
from f_combine import f_combine  # Import the f_combine function from f_combine.py

app = Flask(__name__)

# Load tables in main.py
table21 = pd.read_csv('tables/table21.csv', sep=',', dtype=str)
table22 = pd.read_csv('tables/table22.csv', sep=',', dtype=str)
table23 = pd.read_csv('tables/table23.csv', sep=',', dtype=str)
table41 = pd.read_csv('tables/table41.csv', sep=',', dtype=str)
table51 = pd.read_csv('tables/table51.csv', sep=',', dtype=str)
table61 = pd.read_csv('tables/table61.csv', sep=',', dtype=str)
table62 = pd.read_csv('tables/table62.csv', sep=',', dtype=str)

# This route handles the main form page of the application.
@app.route('/')
def form():
    categories = table21['Category'].unique().tolist()
    return render_template('index.html', categories=categories)

# This route dynamically fetches impairment numbers and descriptions based on the selected injury category.
@app.route('/get_impairment_numbers', methods=['GET'])
def get_impairment_numbers():
    try:
        selected_category = request.args.get('category')
        # Fetch both the impairment number and impairment description
        impairment_numbers = table22.loc[table22['Category'] == str(selected_category), ['Impairment Number', 'Impairment Description']]

        # Return a list of dictionaries with both the number and the description
        return jsonify([{'Impairment_Number': row['Impairment Number'], 'Impairment_Description': row['Impairment Description']} for _, row in impairment_numbers.iterrows()])

    except Exception as e:
        print(f"Error fetching impairment numbers: {e}")
        return jsonify([]), 500

# Perform California adjustment
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        input_mode = request.form.get('input_mode', 'off') == 'on'
    
        if input_mode:
            # Simplified input mode
            impairment_standard = request.form.get('impairment_standard')
            FEC_rank = request.form.get('FEC_rank')
            occupational_variant = request.form.get('occupational_variant')
            age = request.form.get('age')

            # Ensure that the variables are not None or empty
            if not FEC_rank or not occupational_variant:
                return jsonify({"error": "FEC Rank and Occupational Variant must be provided in simplified mode"}), 400
            
            FEC_adjustment = table23.loc[table23['FEC Rank'] == str(FEC_rank), str(impairment_standard)].values[0]
            occupational_adjustment = table51.loc[table51['Occupational Variant'] == str(occupational_variant), str(FEC_adjustment)].values[0]
            age_group = table61.loc[table61['Age'] == str(age), 'Age Group'].values[0]
            age_adjustment = table62.loc[table62['Age Group'] == str(age_group), str(occupational_adjustment)].values[0]
            
            return jsonify({
                "impairment_standard": impairment_standard,
                "FEC_rank": FEC_rank,
                "FEC_adjustment": FEC_adjustment,
                "occupational_variant": occupational_variant,
                "occupational_adjustment": occupational_adjustment,
                "age": age,
                "age_adjustment": age_adjustment
            })

        else:
            # Completed input mode
            impairment_standard = request.form.get('impairment_standard')
            category = request.form.get('category')
            impairment_number = request.form.get('impairment_number')
            occupational_group = request.form.get('occupational_group')
            age = request.form.get('age')

            # Validate inputs
            if not category or not impairment_number or not occupational_group:
                return jsonify({"error": "Category, Impairment Number, and Occupational Group are required"}), 400

            impairment_description = table22.loc[table22['Impairment Number'] == str(impairment_number), 'Impairment Description'].values[0]
            FEC_rank = table22.loc[table22['Impairment Number'] == str(impairment_number), 'Rank'].values[0]
            FEC_adjustment = table23.loc[table23['FEC Rank'] == str(FEC_rank), str(impairment_standard)].values[0]
            occupational_variant = table41.loc[table41['Impairment Number'] == str(impairment_number), str(occupational_group)].values[0]
            occupational_adjustment = table51.loc[table51['Occupational Variant'] == str(occupational_variant), str(FEC_adjustment)].values[0]
            age_group = table61.loc[table61['Age'] == str(age), 'Age Group'].values[0]
            age_adjustment = table62.loc[table62['Age Group'] == str(age_group), str(occupational_adjustment)].values[0]

            return jsonify({
                "impairment_standard": impairment_standard,
                "impairment_number": impairment_number,
                "impairment_description": impairment_description,
                "FEC_rank": FEC_rank,
                "FEC_adjustment": FEC_adjustment,
                "occupational_group": occupational_group,
                "occupational_variant": occupational_variant,
                "occupational_adjustment": occupational_adjustment,
                "age": age,
                "age_adjustment": age_adjustment
            })

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
# Route to handle combining ratings
@app.route('/f_combine', methods=['POST'])
def combine():
    try:
        ratings = request.json.get('ratings', [])
        if not ratings or not all(isinstance(r, int) for r in ratings):
            return jsonify({"error": "Please provide a list of integer ratings."}), 400

        combined_rating = f_combine(ratings)
        return jsonify({"combined_rating": combined_rating})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred while combining ratings."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)