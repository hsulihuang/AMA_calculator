from flask import Flask, request, jsonify, render_template # type: ignore
import pandas as pd # type: ignore
from combine import combine_ratings  # Import the combine_ratings function from combine.py

app = Flask(__name__)

# Import Tables
table21 = pd.read_csv('tables/table21.csv', sep=',', dtype=str)
table22 = pd.read_csv('tables/table22.csv', sep=',', dtype=str)
table23 = pd.read_csv('tables/table23.csv', sep=',', dtype=str)
table41 = pd.read_csv('tables/table41.csv', sep=',', dtype=str)
table51 = pd.read_csv('tables/table51.csv', sep=',', dtype=str)
table61 = pd.read_csv('tables/table61.csv', sep=',', dtype=str)
table62 = pd.read_csv('tables/table62.csv', sep=',', dtype=str)

# Function to perform the California adjustment calculation
def california_adjustment(impairment_standard, impairment_number, occupational_group, age):
    try:
        # Step 01: Find the FEC Rank for the given Impairment Number
        FEC_rank = table22.loc[table22['Impairment Number'] == str(impairment_number), 'Rank'].values[0]
        
        # Step 02: Find the FEC Adjustment for the given Impairment Standard and FEC Rank
        FEC_adjustment = table23.loc[table23['FEC Rank'] == FEC_rank, str(impairment_standard)].values[0]
        
        # Step 03: Find the Occupational Variant for the given Impairment Number and Occupational Group
        occupational_variant = table41.loc[table41['Impairment Number'] == str(impairment_number), str(occupational_group)].values[0]
        
        # Step 04: Find the Occupational Adjustment for the given FEC Adjustment and Occupational Variant
        occupational_adjustment = table51.loc[table51['Occupational Variant'] == occupational_variant, str(FEC_adjustment)].values[0]
        
        # Step 05: Find the Age Group for the given Age
        age_group = table61.loc[table61['Age'] == str(age), 'Age Group'].values[0]
        
        # Step 06: Find the Age Adjustment for the given Occupational Adjustment and Age Group
        age_adjustment = table62.loc[table62['Age Group'] == age_group, str(occupational_adjustment)].values[0]
        
        # Return the Age Adjustment aka the Adjusted WPI
        return age_adjustment

    except Exception as e:
        return str(e)

@app.route('/')
def form():
    categories = table21['Category'].unique().tolist()
    return render_template('index.html', categories=categories)

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

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        impairment_standard = str(request.form['impairment_standard'])
        impairment_number = str(request.form['impairment_number'])
        occupational_group = str(request.form['occupational_group'])
        age = str(request.form['age'])

        # Step 00: Get Impairment Description
        impairment_description = table22.loc[table22['Impairment Number'] == impairment_number, 'Impairment Description'].values[0]
        
        # Step 01: Find the FEC Rank for the given Impairment Number
        FEC_rank = table22.loc[table22['Impairment Number'] == impairment_number, 'Rank'].values[0]
        
        # Step 02: Find the FEC Adjustment for the given Impairment Standard and FEC Rank
        FEC_adjustment = table23.loc[table23['FEC Rank'] == FEC_rank, impairment_standard].values[0]
        
        # Step 03: Find the Occupational Variant for the given Impairment Number and Occupational Group
        occupational_variant = table41.loc[table41['Impairment Number'] == impairment_number, occupational_group].values[0]
        
        # Step 04: Find the Occupational Adjustment for the given FEC Adjustment and Occupational Variant
        occupational_adjustment = table51.loc[table51['Occupational Variant'] == occupational_variant, FEC_adjustment].values[0]
        
        # Step 05: Find the Age Group for the given Age
        age_group = table61.loc[table61['Age'] == age, 'Age Group'].values[0]
        
        # Step 06: Find the Age Adjustment for the given Occupational Adjustment and Age Group
        age_adjustment = table62.loc[table62['Age Group'] == age_group, occupational_adjustment].values[0]
        
        # Return all the relevant data    
        return jsonify({
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
        return "An error occurred", 500

# An old version calculate() to return only the final adjusted WPI
'''
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        impairment_standard = request.form['impairment_standard']
        impairment_number = request.form['impairment_number']
        occupational_group = request.form['occupational_group']
        age = str(request.form['age'])

        result = california_adjustment(impairment_standard, impairment_number, occupational_group, age)
            
        return jsonify(result)

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 500
'''

# New route to handle combining ratings
@app.route('/combine_ratings', methods=['POST'])
def combine():
    try:
        ratings = request.json.get('ratings', [])
        if not ratings or not all(isinstance(r, int) for r in ratings):
            return jsonify({"error": "Please provide a list of integer ratings."}), 400

        combined_rating = combine_ratings(ratings)
        return jsonify({"combined_final_rating": combined_rating})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred while combining ratings."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)