import os
from pyswip import Prolog
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Set environment variables for SWI-Prolog
os.environ['SWI_HOME_DIR'] = r'C:\Program Files\swipl'  # Path to SWI-Prolog installation
os.environ['PATH'] += os.pathsep + r'C:\Program Files\swipl\bin'  # Adding bin to PATH
os.environ['PLLIBDIR'] = r'C:\Program Files\swipl\lib'  # SWI-Prolog library path

# Initialize Prolog after setting paths
try:
    prolog = Prolog()
    prolog.consult("skincare.pl")
except Exception as e:
    print(f"Error initializing Prolog: {e}")

# Initialize stop words
stop_words = set(stopwords.words('english'))

# Global state to track user intentions
awaiting_routine_confirmation = False
awaiting_product_confirmation = False
awaiting_other_questions = False
current_skin_types = []
current_query_type = None

def preprocess_input(user_input):
    # Tokenize and remove stopwords
    words = word_tokenize(user_input.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    return filtered_words

def determine_skin_types(filtered_words):
    # Simple keyword-based approach to determine skin types
    skin_types = []
    if 'oily' in filtered_words:
        skin_types.append('oily')
    if 'normal' in filtered_words:
        skin_types.append('normal')
    if 'dry' in filtered_words:
        skin_types.append('dry')
    if 'combination' in filtered_words:
        skin_types.append('combination')
    if 'acne' in filtered_words or 'acne-prone' in filtered_words:
        skin_types.append('acne_prone')
    if 'damaged' in filtered_words or 'damage' in filtered_words:
        skin_types.append('damaged')
    return skin_types

def fetch_recommendations(skin_type):
    # Query Prolog for recommendations
    query = f"recommendation({skin_type}, Recommendations)"
    result = list(prolog.query(query))
    if result:
        return result[0]['Recommendations']
    return []

def fetch_products(skin_type):
    # Query Prolog for product recommendations
    query = f"products({skin_type}, Products)"
    result = list(prolog.query(query))
    if result:
        return result[0]['Products']
    return []

def provide_treatment_info():
    return (
        "For treatment of damaged skin, you can visit Dr. Wai Skin Care and Treatment Service:\n"
        "Facebook Page: [Dr Wai Skin Care and Treatment Service](https://www.facebook.com/drwaiclinic?mibextid=LQQJ4d)\n"
        "Location: 39 A, 8 Street, Lanmadaw Township, Yangon, Myanmar\n"
        "Coordinates: 16.86264° N, 96.11076° E\n"
        "Phone: 09965031567"
    )

def handle_input(user_input):
    global awaiting_routine_confirmation, awaiting_product_confirmation, awaiting_other_questions, current_skin_types, current_query_type
    
    filtered_words = preprocess_input(user_input)
    
    affirmative_responses = ['yes', 'y', 'sure', 'of course', 'okay', 'ok', 'definitely']
    negative_responses = ['no', 'n', 'not interested', 'nope', 'nah']
    
    # Provide treatment/cure/service information if requested
    if 'treatment' in filtered_words or 'cure' in filtered_words or 'service' in filtered_words:
        return provide_treatment_info()
    
    # Handle responses when waiting for confirmation
    if awaiting_routine_confirmation or awaiting_product_confirmation:
        if any(word in affirmative_responses for word in filtered_words):
            awaiting_routine_confirmation = False
            awaiting_product_confirmation = False
            response = ""
            
            if current_query_type == 'tips':
                for skin_type in current_skin_types:
                    recommendations = fetch_recommendations(skin_type)
                    response += f"### Recommendations for {skin_type.capitalize()} Skin ###\n"
                    for idx, rec in enumerate(recommendations, start=1):
                        response += f"{idx}. {rec}\n"
                    response += "\n"
                    
            elif current_query_type == 'products':
                for skin_type in current_skin_types:
                    products = fetch_products(skin_type)
                    response += f"### Product Suggestions for {skin_type.capitalize()} Skin ###\n"
                    for idx, prod in enumerate(products, start=1):
                        response += f"{idx}. {prod}\n"
                    response += "\n"
            
            return response

        elif any(word in negative_responses for word in filtered_words):
            awaiting_routine_confirmation = False
            awaiting_product_confirmation = False
            awaiting_other_questions = True
            return "So, do you have any other questions?"

    if awaiting_other_questions:
        if any(word in affirmative_responses for word in filtered_words):
            awaiting_other_questions = False
            return "What else can I assist you with?"

        if any(word in negative_responses for word in filtered_words):
            print("Thank you for using the Skincare Recommendation Bot! Have a great day! 😊")
            exit()
        
        return "So, do you have any other questions?"
    
    # Determine skin types from user input
    skin_types = determine_skin_types(filtered_words)
    
    if skin_types:
        current_skin_types = skin_types
        
        if 'product' in filtered_words or 'products' in filtered_words:
            current_query_type = 'products'
            response = ""
            for skin_type in skin_types:
                products = fetch_products(skin_type)
                response += f"### Product Suggestions for {skin_type.capitalize()} Skin ###\n"
                for idx, prod in enumerate(products, start=1):
                    response += f"{idx}. {prod}\n"
                response += "\n"
            return response
        
        if 'routine' in filtered_words or 'routines' in filtered_words:
            current_query_type = 'tips'
            response = ""
            for skin_type in skin_types:
                recommendations = fetch_recommendations(skin_type)
                response += f"### Recommendations for {skin_type.capitalize()} Skin ###\n"
                for idx, rec in enumerate(recommendations, start=1):
                    response += f"{idx}. {rec}\n"
                response += "\n"
            return response

        # If user hasn't specified products or routine, show both
        response = ""
        for skin_type in skin_types:
            recommendations = fetch_recommendations(skin_type)
            response += f"### Recommendations for {skin_type.capitalize()} Skin ###\n"
            for idx, rec in enumerate(recommendations, start=1):
                response += f"{idx}. {rec}\n"
            response += "\n"
            
            products = fetch_products(skin_type)
            response += f"### Product Suggestions for {skin_type.capitalize()} Skin ###\n"
            for idx, prod in enumerate(products, start=1):
                response += f"{idx}. {prod}\n"
            response += "\n"
        
        current_query_type = None
        return response

    if 'thanks' in filtered_words or 'thank you' in filtered_words:
        return "You're welcome! 😊 If you have any more questions, feel free to ask."

    return "I'm sorry, I couldn't determine your skin type. Please specify if your skin is oily, normal, dry, combination, acne-prone, or damaged."

def main():
    print("Welcome to the Skincare Recommendation Bot!")
    print("Feel free to ask about skincare tips or product recommendations based on your skin type.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye! Stay glowing! 😊")
            break

        response = handle_input(user_input)
        print(response)

if __name__ == "__main__":
    main()
