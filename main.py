# Import Modules
import pandas as pd
import numpy as np

# Import Tables
table21 = pd.read_csv('table21.csv', sep=',')
table22 = pd.read_csv('table22.csv', sep=',')
table23 = pd.read_csv('table23.csv', sep=',')
table41 = pd.read_csv('table41.csv', sep=',')
table51 = pd.read_csv('table51.csv', sep=',')
table61 = pd.read_csv('table61.csv', sep=',')
table62 = pd.read_csv('table62.csv', sep=',')

# Inputs
impairment_standard = 20
impairment_number = '16.04.01.00'
occupational_group = 240
age = 45

# Integrated Calculator for California Adjustment
# To combine all the above steps into a single function with the four input variables 
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

# Example usage:
# APDR = california_adjustment(impairment_standard=5, impairment_number='03.05.00.00', occupational_group=220, age=35)
# print(f"The Adjusted Permanent Disability Rating is {APDR}.")

# Example:
APDR = california_adjustment(impairment_standard, impairment_number, occupational_group, age)
print(f"The Adjusted Permanent Disability Rating is {APDR}.")

# Calculator for AMA Impairment Combination
# Combine multiple Age Adjustments as the Overall Permanent Disability Rating

# Step 1: Define the list of numbers
numbers = [30, 20, 5, 40, 10]

# Step 2: Reorder the numbers from largest to smallest
numbers.sort(reverse=True)

# Step 3: Divide all numbers by 100
numbers = [num / 100 for num in numbers]

# Step 4: Define the formula A + B - A * B
def combine(a, b):
    return a + b - a * b

# Step 5: Combine the numbers until only one is left
while len(numbers) > 1:
    # Combine the first two elements using the formula
    combined_value = combine(numbers[0], numbers[1])
    # Replace the first two elements with the combined value
    numbers = [combined_value] + numbers[2:]

# The final number after all combinations
result = round(numbers[0] * 100)

print(f"The Overall Permanent Disability Rating is: {result}%")