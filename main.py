from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import re

# Load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize FastAPI app
app = FastAPI()

# Predefined medication list for validation
VALID_MEDICATIONS = {"paracetamol", "ibuprofen", "amoxicillin"}

# Input Model
class TaskInput(BaseModel):
    command: str

# Helper function: Intent classification
def classify_intent(doc):
    text = doc.text.lower()
    if "add" in text and "patient" in text:
        return "add_patient"
    elif "assign" in text and "medication" in text:
        return "assign_medication"
    elif "schedule" in text and "follow-up" in text:
        return "schedule_followup"
    return "unknown"

# Helper function: Extract entities based on intent
def extract_entities(intent, doc):
    entities = {}
    # Entity extraction based on intent
    if intent == "add_patient":
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities["name"] = ent.text
            elif ent.label_ == "AGE":
                entities["age"] = int(re.search(r"\d+", ent.text).group())
            elif ent.label_ in ["DISEASE", "GPE", "ORG"]:
                entities["condition"] = ent.text.lower()
            elif ent.label_ == "GPE" and "male" in ent.text.lower() or "female" in ent.text.lower():
                entities["gender"] = ent.text.lower()

    elif intent == "assign_medication":
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities["patient_name"] = ent.text
        # Extract medication details via regex
        medication_match = re.search(r"medication\s+(\w+)", doc.text)
        dosage_match = re.search(r"(\d+mg)", doc.text)
        frequency_match = re.search(r"(\btwice a day\b|\bonce a day\b)", doc.text)

        if medication_match:
            medication = medication_match.group(1).capitalize()
            if medication not in VALID_MEDICATIONS:
                entities["medication"] = "Invalid Medication"
            else:
                entities["medication"] = medication
        if dosage_match:
            entities["dosage"] = dosage_match.group(1)
        if frequency_match:
            entities["frequency"] = frequency_match.group(1)

    elif intent == "schedule_followup":
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities["patient_name"] = ent.text
            if ent.label_ == "DATE":
                entities["date"] = ent.text

    return entities

# API Endpoint
@app.post("/parse-task/")
def parse_task(input: TaskInput):
    # Process the input with spaCy
    doc = nlp(input.command)

    # Step 1: Classify intent
    intent = classify_intent(doc)
    if intent == "unknown":
        return {"error": "Unable to determine intent. Please check the command."}

    # Step 2: Extract entities
    entities = extract_entities(intent, doc)

    # Step 3: Return structured response
    return {"intent": intent, "entities": entities}
