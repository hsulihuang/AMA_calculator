# AMA/California WPI Calculator
**URL to the app:** [https://hsuli-project-01.uc.r.appspot.com/](https://hsuli-project-01.uc.r.appspot.com/)  
**GitHub Repository:** [https://github.com/hsulihuang/AMA_calculator](https://github.com/hsulihuang/AMA_calculator)

## Description
The AMA/California WPI Calculator is a tool designed to automate and simplify the process of calculating the adjusted Whole Person Impairment (WPI). This calculation is based on the Impairment Standard, Impairment Number, Occupational Group, and Age of the injured worker. The tool is particularly useful for healthcare professionals documenting cases in alignment with the custom forms used at the Department of Environmental and Occupational Medicine (EOM) at National Taiwan University Hospital (NTUH).

## Version History
- **Version 0.1.1** (2024/08/21)
  - Updated the output format to align with the custom forms used at the EOM at NTUH.

- **Version 0.1** (2024/08/20)
  - Initial deployment to the web using Google Cloud App Engine.

## Terminology
The terms used in this app adhere to the **Schedule for Rating Permanent Disabilities** by the State of California (referred to as "the Schedule"). The Schedule can be accessed at [this link](https://www.dir.ca.gov/dwc/pdr.pdf).

### Impairment Standard
The Impairment Standard refers to a Whole Person Impairment (WPI) rating provided by the evaluating physician, based on the AMA Guides to the Evaluation of Permanent Impairment (referred to as "the AMA Guides"). This standard represents the degree of impairment for a theoretical average worker, with average occupational demands and at the average age of 39.

### Injury Category & Impairment Number
The Impairment Number identifies the affected body part, organ system, and/or nature of the injury. It follows the format “xx.xx.xx.xx”, where the first two digits (Injury Category) correspond to the chapter number in the AMA Guides that addresses the specific body part or organ system. The subsequent digits further specify the impairment.

### Occupational Group
The Occupational Group refers to the type of occupation the employee was engaged in at the time of injury. The Schedule categorizes the labor market into 45 numbered groups, each assigned a three-digit code. The first digit indicates the physical arduousness of the job (from 1 to 5), the second digit classifies occupations into broad categories, and the third digit differentiates between occupations within these groups.

### Age
The Age is the injured worker's age at the time of the injury.

### Final Permanent Disability Rating
The Final Permanent Disability Rating is the overall disability percentage for a single impairment, as determined by the age adjustment table.
