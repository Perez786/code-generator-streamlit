# Import necessary libraries
import streamlit as st
from together import Together

# Handle TOGETHER_API_KEY access and initialize Together client
try:
    api_key = st.secrets["secrets"]["TOGETHER_API_KEY"]  # Access nested key
    client = Together(api_key=api_key)  # Pass API key directly to Together client
except KeyError:
    st.error("TOGETHER_API_KEY is missing in the secrets configuration. Ensure it's set correctly.")
except Exception as e:
    st.error(f"Error initializing Together client: {e}")

# Function to generate Python code using CodeLlama
def generate_code_with_codellama(description):
    """
    Generate Python code based on a natural language description using CodeLlama.

    Parameters:
    description (str): A plain-text description of the desired Python code.

    Returns:
    str: Generated Python code or an error message.
    """
    try:
        # Construct the prompt
        prompt = (
            f"You are a Python programming assistant. Based on the following description, "
            f"generate the Python code. Ensure the code is clear, well-commented, and includes necessary imports.\n\n"
            f"Description: {description}\n\n"
            f"Generated Python Code:"
        )

        # Call Together AI
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",  # CodeLlama model
            messages=[{"role": "user", "content": prompt}]
        )

        # Check if the response structure is valid
        if not hasattr(response, "choices") or not response.choices:
            raise ValueError("Invalid response from Together API.")

        # Extract the generated code
        generated_code = response.choices[0].message.content.strip()
        return generated_code

    except Exception as e:
        # Handle any errors during the API call
        return f"Error with CodeLlama: {e}"

# Streamlit app layout
st.title("Python Code Generator with CodeLlama")
st.write("Enter a description of the Python application or code you need. CodeLlama will generate the corresponding Python code.")

# Input box for the user to enter a description
description = st.text_area("Application or Code Description", placeholder="Describe the application or code you want")

# Button to trigger code generation
if st.button("Generate Code"):
    if description.strip():
        # Validate description length
        if len(description.strip()) > 1000:
            st.error("Description is too long. Please keep it under 1000 characters.")
        else:
            st.write("### Generated Python Code")
            # Generate code
            generated_code = generate_code_with_codellama(description)
            st.code(generated_code, language="python")
    else:
        st.error("Please provide a valid description.")


