#!/usr/bin/env python3
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
import json

client = OpenAI()

def translate_value(key_value):
    key, value = key_value
    print(f"Translating '{key}: {value}'...")
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a highly proficient translator. You will be given JSON lines containing texts from the UI of a blog publishing platform. The key is English, and the value in Spanish. Respond ONLY with the value in Greek. DO NOT BE VERBOSE."},
        {"role": "user", "content": f"\"{key}\":\"{value}\","}
    ])
    translated_value = response.choices[0].message.content
    if translated_value.startswith('"'):
        translated_value = translated_value[1:]
    if translated_value.endswith('",'):
        translated_value = translated_value[:-2]
    if translated_value.endswith('"'):
        translated_value = translated_value[:-1]
    print(f"Translated '{key}' to Greek: '{translated_value}'")
    return key, translated_value

def translate_to_greek(input_file, output_file):
    print(f"Reading data from {input_file}...")
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    translated_data = {}
    print("Translating values from Spanish to Greek...")
    with ThreadPoolExecutor() as executor:
        results = executor.map(translate_value, data.items())
        for key, translated_value in results:
            translated_data[key] = translated_value

    print(f"Writing translated data to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=4)
    
    print("Translation completed successfully.")

components = ['comments', 'ghost', 'portal', 'signup-form']
with ThreadPoolExecutor() as executor:
    executor.map(lambda component: translate_to_greek(f'es/{component}.json', f'el/{component}.json'), components)
