# Function to perform the California adjustment calculation
def f_california(impairment_standard, impairment_number, occupational_group, age,
                          table22, table23, table41, table51, table61, table62):
    try:
        # Step 00: Get Impairment Description
        impairment_description = table22.loc[table22['Impairment Number'] == str(impairment_number), 'Impairment Description'].values[0]

        # Step 01: Find the FEC Rank for the given Impairment Number
        FEC_rank = table22.loc[table22['Impairment Number'] == str(impairment_number), 'Rank'].values[0]
        
        # Step 02: Find the FEC Adjustment for the given Impairment Standard and FEC Rank
        FEC_adjustment = table23.loc[table23['FEC Rank'] == str(FEC_rank), str(impairment_standard)].values[0]
        
        # Step 03: Find the Occupational Variant for the given Impairment Number and Occupational Group
        occupational_variant = table41.loc[table41['Impairment Number'] == str(impairment_number), str(occupational_group)].values[0]
        
        # Step 04: Find the Occupational Adjustment for the given FEC Adjustment and Occupational Variant
        occupational_adjustment = table51.loc[table51['Occupational Variant'] == str(occupational_variant), str(FEC_adjustment)].values[0]
        
        # Step 05: Find the Age Group for the given Age
        age_group = table61.loc[table61['Age'] == str(age), 'Age Group'].values[0]
        
        # Step 06: Find the Age Adjustment for the given Occupational Adjustment and Age Group
        age_adjustment = table62.loc[table62['Age Group'] == str(age_group), str(occupational_adjustment)].values[0]
        
        # Return all the relevant data as a dictionary
        return {
            "impairment_description": impairment_description,
            "FEC_rank": FEC_rank,
            "FEC_adjustment": FEC_adjustment,
            "occupational_group": occupational_group,
            "occupational_variant": occupational_variant,
            "occupational_adjustment": occupational_adjustment,
            "age": age,
            "age_adjustment": age_adjustment
        }

    except Exception as e:
        return {"error": str(e)}