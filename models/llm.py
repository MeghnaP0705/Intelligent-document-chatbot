from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from config.config import Config

def get_llm(mode="concise"):
    """
    Initializes and returns an LLM based on available API credentials.
    Supports dynamic switching between Concise and Detailed response styles.
    Prefers Gemini by default if available; otherwise falls back to OpenAI.
    """
    # Select temperature based on response mode
    temp = Config.TEMPERATURE_CONCISE if mode.lower() == "concise" else Config.TEMPERATURE_DETAILED
    
    if Config.GEMINI_API_KEY:
        import logging
        import google.generativeai as genai
        
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            
            # Fetch Models available to this specific API Key
            available_models = [
                m.name for m in genai.list_models()
                if 'generateContent' in m.supported_generation_methods
            ]
            
            if not available_models:
                raise ValueError("No generative models are available for this API key.")
                
            logging.info(f"Dynamically discovered models for this API key: {available_models}")

            # Define preferred model hierarchy
            preferred_models = [
                "models/gemini-1.5-pro",
                "models/gemini-1.5-flash",
                "models/gemini-pro",
                "models/gemini-1.0-pro"
            ]

            selected_model = None
            for p_model in preferred_models:
                if p_model in available_models:
                    selected_model = p_model
                    break
                    
            if not selected_model:
                selected_model = available_models[0] # Pick whatever is granted

            logging.info(f"Selected Model: {selected_model}")
            
            return ChatGoogleGenerativeAI(
                model=selected_model,
                google_api_key=Config.GEMINI_API_KEY,
                temperature=temp
            )
        except Exception as e:
            logging.error(f"Failed to dynamically load models. Error: {e}")
            # Fallback to standard
            return ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                google_api_key=Config.GEMINI_API_KEY,
                temperature=temp
            )
    elif Config.OPENAI_API_KEY:
        # Utilizing OpenAI model
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=Config.OPENAI_API_KEY,
            temperature=temp
        )
    else:
        raise ValueError((
            "No valid API keys found. "
            "Please provide GEMINI_API_KEY or OPENAI_API_KEY."
        ))
