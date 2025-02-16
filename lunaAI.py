import google.generativeai as genai


genai.configure(api_key="AIzaSyAec5h7YVRXlHL_MQw-7-c3rwgkkR9YMWw")

def get_ai_response(prompt):
    try:
        response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
        return response.text  
    except Exception as e:
        return f"Error: {e}"

