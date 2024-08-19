from flask import Flask, request, jsonify, render_template_string
import pandas as pd

app = Flask(__name__)

# Import Tables
table21 = pd.read_csv('table21.csv', sep=',')
table22 = pd.read_csv('table22.csv', sep=',')
table23 = pd.read_csv('table23.csv', sep=',')
table41 = pd.read_csv('table41.csv', sep=',')
table51 = pd.read_csv('table51.csv', sep=',')
table61 = pd.read_csv('table61.csv', sep=',')
table62 = pd.read_csv('table62.csv', sep=',')

# Set Variables
impairment_standard = str()
impairment_number = str()
occupational_group = str()
age = str()

# Integrated Calculator for California Adjustment
def california_adjustment(impairment_standard, impairment_number, occupational_group, age):
    # Step 01: Find the FEC Rank for the given Impairment Number
    FEC_rank = table22.loc[table22['Impairment Number'] == str(impairment_number), 'Rank'].values[0]
    
    # Step 02: Find the FEC Adjustment for the given Impairment Standard and FEC Rank
    df_fec_adjustment = pd.DataFrame(table23)
    df_fec_adjustment.set_index('FEC Rank', inplace=True)
    FEC_adjustment = df_fec_adjustment.loc[FEC_rank, str(impairment_standard)]
    
    # Step 03: Find the Occupational Variant for the given Impairment Number and Occupational Group
    df_occupational_variant = pd.DataFrame(table41)
    df_occupational_variant.set_index('Impairment Number', inplace=True)
    occupational_variant = df_occupational_variant.loc[impairment_number, str(occupational_group)]
    
    # Step 04: Find the Occupational Adjustment for the given FEC Adjustment and Occupational Variant
    df_occupational_adjustment = pd.DataFrame(table51)
    df_occupational_adjustment.set_index('Occupational Variant', inplace=True)
    occupational_adjustment = df_occupational_adjustment.loc[occupational_variant, str(FEC_adjustment)]
    
    # Step 05: Find the Age Group for the given Age
    df_age_group = pd.DataFrame(table61)
    
    def get_age_group(age):
        result = df_age_group.loc[df_age_group['Age'] == age, 'Age Group']
        return result.values[0] if not result.empty else "Age not found"
    
    age_group = get_age_group(age)
    
    # Step 06: Find the Age Adjustment for the given Occupational Adjustment and Age Group
    df_age_adjustment = pd.DataFrame(table62)
    df_age_adjustment.set_index('Age Group', inplace=True)
    age_adjustment = df_age_adjustment.loc[age_group, str(occupational_adjustment)]
    
    # Output the final result
    return age_adjustment

# Route to serve the HTML form
@app.route('/')
def form():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>California Adjustment Calculator</title>
    </head>
    <body>
        <h1>California Adjustment Calculator</h1>
        <form id="adjustmentForm">
            <label for="impairment_standard">Impairment Standard:</label><br>
            <input type="text" id="impairment_standard" name="impairment_standard"><br><br>

            <label for="impairment_number">Impairment Number:</label><br>
            <input type="text" id="impairment_number" name="impairment_number"><br><br>

            <label for="occupational_group">Occupational Group:</label><br>
            <input type="text" id="occupational_group" name="occupational_group"><br><br>

            <label for="age">Age:</label><br>
            <input type="text" id="age" name="age"><br><br>

            <input type="button" value="Calculate" onclick="submitForm()">
        </form>

        <h2>Result</h2>
        <p id="result"></p>

        <script>
            function submitForm() {
                var formData = {
                    impairment_standard: document.getElementById('impairment_standard').value,
                    impairment_number: document.getElementById('impairment_number').value,
                    occupational_group: document.getElementById('occupational_group').value,
                    age: document.getElementById('age').value
                };

                fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').innerText = "Age Adjustment: " + data.age_adjustment;
                })
                .catch(error => console.error('Error:', error));
            }
        </script>
    </body>
    </html>
    """)

# Route to handle the form submission
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    print(f"Received data: {data}")
    impairment_standard = data['impairment_standard']
    impairment_number = data['impairment_number']
    occupational_group = data['occupational_group']
    age = data['age']
    result = california_adjustment(impairment_standard, impairment_number, occupational_group, age)
    print(f"Calculated result: {result}")
    return jsonify({"age_adjustment": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)