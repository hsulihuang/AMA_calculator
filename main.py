from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Import Tables
table21 = pd.read_csv('tables/table21.csv', sep=',')
table22 = pd.read_csv('tables/table22.csv', sep=',')
table23 = pd.read_csv('tables/table23.csv', sep=',')
table41 = pd.read_csv('tables/table41.csv', sep=',')
table51 = pd.read_csv('tables/table51.csv', sep=',')
table61 = pd.read_csv('tables/table61.csv', sep=',')
table62 = pd.read_csv('tables/table62.csv', sep=',')

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
        age_group = table61.loc[table61['Age'] == int(age), 'Age Group'].values[0]
        
        # Step 06: Find the Age Adjustment for the given Occupational Adjustment and Age Group
        age_adjustment = table62.loc[table62['Age Group'] == age_group, str(occupational_adjustment)].values[0]
        
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
        impairment_prefix = table21.loc[table21['Category'] == selected_category, 'Category'].values[0][:2]
        
        impairment_numbers = table22[table22['Impairment Number'].str.startswith(impairment_prefix)]['Impairment Number'].unique()
        
        return jsonify([{'Impairment_Number': impairment_number} for impairment_number in impairment_numbers])

    except Exception as e:
        print(f"Error fetching impairment numbers: {e}")
        return jsonify([]), 500


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        impairment_standard = request.form['impairment_standard']
        impairment_number = request.form['impairment_number']
        occupational_group = request.form['occupational_group']
        age = int(request.form['age'])

        result = california_adjustment(impairment_standard, impairment_number, occupational_group, age)
        
        # Convert to standard Python int
        if isinstance(result, pd.Series) or isinstance(result, pd.DataFrame):
            result = result.to_dict()  # If the result is a pandas Series or DataFrame
        else:
            result = int(result)  # Convert int64 to standard int if it's a single number
            
        return jsonify({"age_adjustment": int(result)})

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
