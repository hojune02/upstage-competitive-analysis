INVOICE_PROMPT = """
From the items in the given invoice, extract and display in the following manner. If the extracted price is 0, ignore the item:

Item 1: [description]
Item 1 price: $[price_in_number]

Item 2: [description]
Item 2 price: $[price_in_number]

Item 3: [description]
Item 3 price: $[price_in_number]
... [go through all the items in this manner]
...
Total price: $[price_in_number]

Rules:
- Use only information from the provided invoice document.
- Ignore items with extracted price 0.
- Do not invent missing items or prices.
- Preserve the item descriptions as closely as possible.
- Follow the output format above.
"""


MEDICAL_PROMPT = """
Generate a summary report on a patient's case, including their symptoms and corresponding descriptions.

If symptom names are repeated, merge their descriptions under one symptom. For instance, 'chest pain' and 'chest pains' must be categorized as one symptom, not two.

Follow the output format below:

Name of patient: [extract patient name from the document]

Heading: Symptoms and Descriptions

Symptom 1: [symptom name extracted from the document]
Description: [description of the symptom extracted from the document]

Symptom 2: [symptom name extracted from the document]
Description: [description of the symptom extracted from the document]

Symptom 3: [symptom name extracted from the document]
Description: [description of the symptom extracted from the document]

...(all the symptoms and their descriptions listed out)

Heading: Severity Report

Severity report: (#High, #Medium or #Low depending on the symptoms)
Reason: (Justification on the severity report, based on the extracted severity information if it exists)

Rules:
- Use only information from the provided medical report.
- Merge repeated symptoms.
- Merge semantically equivalent symptoms when appropriate, such as dyspnea and shortness of breath.
- Do not invent symptoms that are not supported by the document.
- If severity is inferred rather than explicitly stated, mention that in the reason.
- Follow the output format above.
"""