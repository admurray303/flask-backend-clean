from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS
import requests
import json
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
"""
def get_crypto_price(coin: str = "bitcoin") -> str:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        price = data[coin]["usd"]
        return f"The current price of {coin} is ${price:.2f} USD."
    except Exception as e:
        return f"Error fetching price for {coin}: {str(e)}"


"""
app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    """tools = [
        {
            "type": "function",
            "function": {
                "name": "get_crypto_price",
                "description": "Get the current USD price of a cryptocurrency",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "coin": {
                            "type": "string",
                            "description": "The name of the cryptocurrency, e.g., bitcoin"
                        }
                    },
                    "required": ["coin"]
                }
            }
        }
    ]
"""
    instructions = "You are a helpful Assistant. you will answer every question like a pirate"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the correct model for chat
            messages=[
                {"role": "system", "content" : instructions},
                {"role": "user", "content": prompt}
            ],
            #tools = tools,
            #tool_choice = "auto",
            max_tokens=100
        )
        first_choice = response.choices[0]
        msg = first_choice.message

        # If GPT wants to call a tool

        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if function_name == "get_crypto_price":
                result = get_crypto_price(**function_args)
                return jsonify({"response": result})
        return jsonify({"response": response.choices[0].message.content.strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
