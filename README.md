# curenta-project
# Intelligent Task Management Bot for Medical Facilities  
This project implements an **NLP-based assistant** that can parse natural language commands related to nurse tasks, classify the task's intent, and extract relevant entities. The bot returns a structured JSON output for integration into medical task management systems.  

## **Features**  
1. **Intent Recognition**: Determines the type of task (e.g., `add_patient`, `assign_medication`, `schedule_followup`).  
2. **Entity Extraction**: Extracts entities such as patient name, age, condition, medication, dosage, and dates.  
3. **Validation**: Validates medication names against a predefined list of known medications.  
4. **Scalability**: Built as a RESTful API using FastAPI.  

## **Setup**  

### **Prerequisites**  
- Python 3.8+  
- FastAPI  
- spaCy NLP library  
- Uvicorn server  

### **Installation**  
1. Clone this repository:  
   ```bash  
   git clone https://github.com/yourusername/task-bot.git  
   cd task-bot  
   ```  

2. Install the required dependencies:  
   ```bash  
   pip install fastapi uvicorn spacy pydantic  
   python -m spacy download en_core_web_sm  
   ```  

3. Run the FastAPI server:  
   ```bash  
   uvicorn main:app --reload  
   ```  

## **API Usage**  

### Endpoint  
`POST /parse-task/`  

### Request Body  
Send a JSON payload containing the `command`:  
```json  
{  
  "command": "Add a new patient John Doe, male, 45 years old, with diabetes."  
}  
```  

### Response  
The API will respond with a structured JSON:  
```json  
{  
  "intent": "add_patient",  
  "entities": {  
    "name": "John Doe",  
    "age": 45,  
    "condition": "diabetes",  
    "gender": "male"  
  }  
}  
```  

## **Examples**  

### Add Patient  
**Input**:  
```json  
{"command": "Add a new patient John Doe, male, 45 years old, with diabetes."}  
```  
**Response**:  
```json  
{  
  "intent": "add_patient",  
  "entities": {  
    "name": "John Doe",  
    "age": 45,  
    "condition": "diabetes",  
    "gender": "male"  
  }  
}  
```  

### Assign Medication  
**Input**:  
```json  
{"command": "Assign medication Paracetamol 500mg twice a day for John Doe."}  
```  
**Response**:  
```json  
{  
  "intent": "assign_medication",  
  "entities": {  
    "patient_name": "John Doe",  
    "medication": "Paracetamol",  
    "dosage": "500mg",  
    "frequency": "twice a day"  
  }  
}  
```  

### Schedule Follow-Up  
**Input**:  
```json  
{"command": "Schedule a follow-up for John Doe on December 20th."}  
```  
**Response**:  
```json  
{  
  "intent": "schedule_followup",  
  "entities": {  
    "patient_name": "John Doe",  
    "date": "December 20th"  
  }  
}  
```  

## **API Documentation**  
Once the FastAPI server is running, navigate to the following URLs for interactive API documentation:  
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

## **Testing**  
You can use tools like **Postman** or **curl** to test the API.  

Example with `curl`:  
```bash  
curl -X POST "http://127.0.0.1:8000/parse-task/" -H "Content-Type: application/json" -d '{"command": "Assign medication Paracetamol 500mg twice a day for John Doe."}'  
```  
