from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load CSV tables
table21 = pd.read_csv('table21.csv', sep=',')
table22 = pd.read_csv('table22.csv', sep=',')
table23 = pd.read_csv('table23.csv', sep=',')
table41 = pd.read_csv('table41.csv', sep=',')
table51 = pd.read_csv('table51.csv', sep=',')
table61 = pd.read_csv('table61.csv', sep=',')
table62 = pd.read_csv('table62.csv', sep=',')

def california_adjustment(impairment_standard, impairment_number, occupational_group, age):
    try:
        # Step 1: Get FEC Rank
        FEC_rank = table22.loc[table22['Impairment Number'] == str(impairment_number), 'Rank'].values[0]
        
        # Step 2: Get FEC Adjustment
        df_fec_adjustment = table23.set_index('FEC Rank')
        FEC_adjustment = df_fec_adjustment.loc[FEC_rank, str(impairment_standard)]
        
        # Step 3: Get Occupational Variant
        df_occupational_variant = table41.set_index('Impairment Number')
        occupational_variant = df_occupational_variant.loc[impairment_number, str(occupational_group)]
        
        # Step 4: Get Occupational Adjustment
        df_occupational_adjustment = table51.set_index('Occupational Variant')
        occupational_adjustment = df_occupational_adjustment.loc[occupational_variant, str(FEC_adjustment)]
        
        # Step 5: Get Age Group
        age_group = table61.loc[table61['Age'] == int(age), 'Age Group']
        if age_group.empty:
            return {"error": "Age not found in dataset"}, 400
        age_group = age_group.values[0]
        
        # Step 6: Get Age Adjustment
        df_age_adjustment = table62.set_index('Age Group')
        age_adjustment = df_age_adjustment.loc[age_group, str(occupational_adjustment)]
        
        return {"age_adjustment": age_adjustment}, 200

    except KeyError as e:
        return {"error": f"KeyError: {str(e)}"}, 400
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    impairment_standard = data.get('impairment_standard')
    impairment_number = data.get('impairment_number')
    occupational_group = data.get('occupational_group')
    age = data.get('age')

    if not all([impairment_standard, impairment_number, occupational_group, age]):
        return jsonify({"error": "All fields are required"}), 400

    result, status_code = california_adjustment(impairment_standard, impairment_number, occupational_group, age)
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
