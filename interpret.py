import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

def interpret_rule(english_rule):
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="""You are a business rules interpreter for a supply chain automation system.
Your job is to convert plain English business rules into structured JSON.
Return ONLY valid JSON, no explanation, no markdown, no code blocks.
Just the raw JSON object.""",
        messages=[
            {"role": "user", "content": english_rule}
        ]
    )
    raw = message.content[0].text
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(cleaned)

if __name__ == "__main__":
    rule = "When on-hand inventory for any SKU falls below its reorder point, create a purchase order for the reorder quantity"
    
    print("Input rule:")
    print(rule)
    print("\nInterpreted as JSON:")
    try:
        result = interpret_rule(rule)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")