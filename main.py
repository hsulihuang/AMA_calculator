from flask import Flask, request, jsonify, render_template, render_template_string
import pandas as pd

app = Flask(__name__)

# Import Tables
try:
    table21 = pd.read_csv('table21.csv', sep=',')
    table22 = pd.read_csv('table22.csv', sep=',')
    table23 = pd.read_csv('table23.csv', sep=',')
    table41 = pd.read_csv('table41.csv', sep=',')
    table51 = pd.read_csv('table51.csv', sep=',')
    table61 = pd.read_csv('table61.csv', sep=',')
    table62 = pd.read_csv('table62.csv', sep=',')
except Exception as e:
    print(f"Error loading tables: {str(e)}")
    raise

# Integrated Calculator for California Adjustment
def california_adjustment(impairment_standard, impairment_number, occupational_group, age):
    try:
        # Step 01: Find the FEC Rank for the given Impairment Number
        FEC_rank = table22.loc[table22['Impairment Number'] == str(impairment_number), 'Rank'].values[0]
    except IndexError:
        return "Impairment Number not found", 400

    try:
        # Step 02: Find the FEC Adjustment for the given Impairment Standard and FEC Rank
        df_fec_adjustment = pd.DataFrame(table23)
        df_fec_adjustment.set_index('FEC Rank', inplace=True)
        FEC_adjustment = df_fec_adjustment.loc[FEC_rank, str(impairment_standard)]
    except KeyError:
        return "Impairment Standard or FEC Rank not found", 400

    try:
        # Step 03: Find the Occupational Variant for the given Impairment Number and Occupational Group
        df_occupational_variant = pd.DataFrame(table41)
        df_occupational_variant.set_index('Impairment Number', inplace=True)
        occupational_variant = df_occupational_variant.loc[impairment_number, str(occupational_group)]
    except KeyError:
        return "Occupational Group or Impairment Number not found", 400

    try:
        # Step 04: Find the Occupational Adjustment for the given FEC Adjustment and Occupational Variant
        df_occupational_adjustment = pd.DataFrame(table51)
        df_occupational_adjustment.set_index('Occupational Variant', inplace=True)
        occupational_adjustment = df_occupational_adjustment.loc[occupational_variant, str(FEC_adjustment)]
    except KeyError:
        return "Occupational Adjustment not found", 400

    try:
        # Step 05: Find the Age Group for the given Age
        df_age_group = pd.DataFrame(table61)

        def get_age_group(age):
            result = df_age_group.loc[df_age_group['Age'] == age, 'Age Group']
            return result.values[0] if not result.empty else "Age not found"

        age_group = get_age_group(age)
        if age_group == "Age not found":
            return age_group, 400
    except KeyError:
        return "Age Group not found", 400

    try:
        # Step 06: Find the Age Adjustment for the given Occupational Adjustment and Age Group
        df_age_adjustment = pd.DataFrame(table62)
        df_age_adjustment.set_index('Age Group', inplace=True)
        age_adjustment = df_age_adjustment.loc[age_group, str(occupational_adjustment)]
    except KeyError:
        return "Age Adjustment not found", 400

    # Output the final result
    return age_adjustment

# Route to serve the HTML form
@app.route('/')
def form():
    return render_template("index.html")

# Route to handle the form submission
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        impairment_standard = data['impairment_standard']
        impairment_number = data['impairment_number']
        occupational_group = data['occupational_group']
        age = data['age']
        result, status = california_adjustment(impairment_standard, impairment_number, occupational_group, age)
        if status == 400:
            return jsonify({"error": result}), 400
        print(f"Calculated result: {result}")
        return jsonify({"age_adjustment": result})
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
