from flask import Flask, request, jsonify, render_template_string
import pandas as pd

app = Flask(__name__)

# Load tables
table21 = pd.read_csv('/mnt/data/table21.csv')
table22 = pd.read_csv('/mnt/data/table22.csv')
table23 = pd.read_csv('/mnt/data/table23.csv')
table41 = pd.read_csv('/mnt/data/table41.csv')
table51 = pd.read_csv('/mnt/data/table51.csv')
table61 = pd.read_csv('/mnt/data/table61.csv')
table62 = pd.read_csv('/mnt/data/table62.csv')

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

# HTML and JavaScript for a single-page interface
html_code = """
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

        <button type="button" onclick="submitForm()">Calculate</button>
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
"""

@app.route('/')
def form():
    return render_template_string(html_code)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    impairment_standard = data.get('impairment_standard')
    impairment_number = data.get('impairment_number')
    occupational_group = data.get('occupational_group')
    age = data.get('age')
    
    result = california_adjustment(impairment_standard, impairment_number, occupational_group, age)
    return jsonify({"age_adjustment": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
