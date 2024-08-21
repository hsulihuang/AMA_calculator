# AMA/California WPI Calculator

- **URL to the App**: [https://hsuli-project-01.uc.r.appspot.com/](https://hsuli-project-01.uc.r.appspot.com/)
- **GitHub Repository**: [https://github.com/hsulihuang/AMA_calculator](https://github.com/hsulihuang/AMA_calculator)

## Description

The AMA/California WPI Calculator is a tool designed to automate and simplify the calculation of the adjusted Whole Person Impairment (WPI). This calculation is based on inputs including the Impairment Standard, Impairment Number, Occupational Group, and Age of the injured worker. It is particularly useful for healthcare professionals who need to document cases in alignment with the commonly used format at the Department of Environmental and Occupational Medicine (EOM) at National Taiwan University Hospital (NTUH).

## Version History

- **Version 0.1.2 (2024/08/21)**: Updated a new function "combining ratings".
- **Version 0.1.1 (2024/08/20)**: Updated the output format to align with the commonly used format at the EOM at NTUH.
- **Version 0.1 (2024/08/19)**: Initial deployment to the web using Google Cloud App Engine.

## Terminology

The terms used in this app adhere to the Schedule for Rating Permanent Disabilities by the State of California (referred to as "the Schedule"). The Schedule can be accessed at [this link](https://www.dir.ca.gov/dwc/pdr.pdf).

- **Impairment Standard**

The Impairment Standard refers to a Whole Person Impairment (WPI) rating provided by the evaluating physician, based on the AMA Guides to the Evaluation of Permanent Impairment (referred to as "the AMA Guides"). This standard represents the degree of impairment for a theoretical average worker, with average occupational demands and at the average age of 39.

- **Injury Category & Impairment Number**

The Impairment Number identifies the affected body part, organ system, and/or nature of the injury. It follows the format “xx.xx.xx.xx,” where the first two digits (Injury Category) correspond to the chapter number in the AMA Guides that addresses the specific body part or organ system. The subsequent digits further specify the impairment.

- **Occupational Group**

The Occupational Group refers to the type of occupation the employee was engaged in at the time of injury. The Schedule categorizes the labor market into 45 numbered groups, each assigned a three-digit code. The first digit indicates the physical arduousness of the job (from 1 to 5), the second digit classifies occupations into broad categories, and the third digit differentiates between occupations within these groups.

- **Age**

The Age is the injured worker's age at the time of the injury.

- **Final Permanent Disability Rating**

The Final Permanent Disability Rating represents the overall disability percentage for a **single impairment**. This rating, often referred to as the adjusted WPI, is determined by adjusting an AMA impairment rating to account for factors such as diminished future earning capacity, occupation, and age.

- **Combined Final Permanent Disability Rating**

Impairments and disabilities are typically combined using the formula \[ a + b(1-a) \], where "a" and "b" represent the decimal equivalents of the impairment or disability percentages.

When combining three or more ratings on the same scale into a single rating, begin by combining the two largest ratings first, rounding the result to the nearest whole percent. Then, combine that result with the next largest rating, and repeat this process until all ratings are combined. Ensure that each successive calculation result is rounded before proceeding with the next combination.

All impairments are initially converted to the whole person scale, adjusted as necessary, and then combined to determine the final overall disability rating.

## How to Use

### 1. Calculate Adjusted WPI

This function allows you to determine the adjusted Whole Person Impairment (WPI) for a single impairment based on specific inputs:

1. **Impairment Standard**: Enter the Whole Person Impairment (WPI) rating provided by the evaluating physician. This rating should be based on the AMA Guides to the Evaluation of Permanent Impairment.

2. **Injury Category & Impairment Number**: Select the injury category and corresponding impairment number that identifies the affected body part or system.

3. **Occupational Group**: Enter the three-digit code that represents the type of occupation the injured worker was engaged in at the time of injury.

4. **Age**: Enter the age of the injured worker at the time of the injury.

#### Example:

- **Impairment Standard**: 20
- **Injury Category**: 16 Upper Extremities
- **Impairment Number**: 16.01.03.00 Arm - Peripheral vascular
- **Occupational Group**: 240
- **Age**: 50

**Result**:

DBI: 16.01.03.00 Arm - Peripheral vascular
FEC (5): 25%
Occupation (240, E): 23%
Age (50): 26%

### 2. Combine Ratings

The Combine Ratings function allows you to combine multiple impairment ratings into a single overall disability rating using the formula \[ a + b(1-a) \], where "a" and "b" represent the decimal equivalents of the impairment or disability percentages.

**Example**:

If you input the following impairment percentages:

- 10%, 30%, 20%

**Result**:

- Combine 30% with 20% = 44%
- Combine 44% with 10% = 50%

The final combined rating is 50%.