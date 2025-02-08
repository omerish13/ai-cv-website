# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import json

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CV data
CV_DATA = {
    "name": "[Your Name]",
    "title": "[Your Title]",
    "summary": "[Your Professional Summary]",
    "experience": [
        {
            "company": "[Company Name]",
            "position": "[Position]",
            "duration": "[Duration]",
            "highlights": [
                "[Achievement 1]",
                "[Achievement 2]",
                "[Achievement 3]"
            ]
        }
    ],
    "education": [
        {
            "institution": "[Institution Name]",
            "degree": "[Degree]",
            "year": "[Year]"
        }
    ],
    "skills": [
        "[Skill 1]",
        "[Skill 2]",
        "[Skill 3]"
    ]
}

# Initialize the model
model = pipeline(
    "text-generation",
    model="HuggingFaceH4/starchat-alpha",  # Free model
    max_length=500
)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # Create prompt with CV context
        prompt = f"""
        Context: You are an AI assistant representing {CV_DATA['name']}. 
        You have access to their CV data: {json.dumps(CV_DATA)}
        
        Question: {request.message}
        
        Answer: Let me help you with information about {CV_DATA['name']}'s experience.
        """
        
        # Generate response
        response = model(prompt, max_length=200, num_return_sequences=1)
        
        # Extract and clean response
        answer = response[0]['generated_text'].split('Answer: ')[-1].strip()
        
        return {"message": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn app.main:app --reload