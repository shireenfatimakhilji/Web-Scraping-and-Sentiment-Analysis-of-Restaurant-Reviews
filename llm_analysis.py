import os
import anthropic
import json
import pandas as pd 
import time 

df = pd.read_csv("IlCortileRestaurant.csv")
reviews900 = df["review_content"]
reviews900 = reviews900.tolist()

#os.environ["ANTHROPIC_API_KEY"] = "your_api_key_here"

client = anthropic.Anthropic()

n = 900

with open('review.json', 'a') as json_file:
    json_file.write("{\n")
    i = 0
    for review in reviews900:
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0,
                system="""
                You are an assistant who analyzes restaurant reviews. 
                Your task for these set of reviews is to extract and categorize the following two pieces of information:
                1. Comments related to food  (e.g., taste, presentation, quality, waiting time).
                2. Comments related to staff (e.g., speed, politeness, professionalism, attitude).

                Please return your response as a list of two strings, where:
                -> The first element (index 0) contains the comments related to food.
                -> The second element (index 1) contains the comments related to staff.

                Make sure to:
                -> Only include relevant comments.
                -> Exclude personal details of the reviewer (e.g., name).
                -> Avoid irrelevant information or hallucinations. 

                Note:
                -> If there is no food or staff related comment just return string none for that index. 
                -> Your responses should be in English         
                """,
                messages=[
                    {
                        "role": "user",
                        "content": review
                        
                    }
                ]
            )

            analysis = message.content

        except anthropic.InternalServerError:
            time.sleep(60)

        analysis_text = analysis[0].text 

        try:
            analysis_json = json.loads(analysis_text)
        except json.JSONDecodeError:
            continue

        analysis_dict = {
            "food": analysis_json[0],  
            "staff": analysis_json[1]  
        }

        print(f"Review ID {i + 1}: ", analysis_dict)

        if i > 0 and i <= n:
            json_file.write(",\n")
        
        json_file.write(f'    "{i + 1}": {json.dumps(analysis_dict)}')

        if i == n:
            break

        i += 1

    json_file.write("\n}")
