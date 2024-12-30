import os
import re
import json
from functools import partial
import anthropic

def read_text(filename):
    with open(filename, 'r') as f: return f.read()

def write_text(filename, text):
    with open(filename, 'w') as f: f.write(text)

def read_json(filename):
    with open(filename, 'r') as f: return json.load(f)

def write_json(filename, data):
    with open(filename, 'w') as f: json.dump(data, f, indent=2)

def remove_json_wrapper(text):
    """ ```json ... ``` -> ... """
    text = text.strip()
    if text.startswith("```json") and text.endswith("```"): text = text[7:-3]
    text = text.strip()
    return text

def basename_(filename):
    name = os.path.basename(filename)
    parts = os.path.splitext(name)
    return parts[0]

RE_DAY = re.compile(r"aoc2024-day(\d+)")

def day_number(path):
    m = RE_DAY.search(path)
    assert m, f"Day number not found in {path}"
    return int(m.group(1))

def call_anthropics_claude(system_prompt, user_message, max_tokens=4096):
    """ Call the Anthropics API to analyze the user message in the context of the system prompt.
        Returns: JSON analysis of the user message.
    """
    # Note: Requires ANTHROPIC_API_KEY environment variable to be set
    client = anthropic.Client()

    # Make the API call
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=max_tokens,
        temperature=0,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    # Response JSON
    text = message.content[0].text
    text = remove_json_wrapper(text)
    # Parse the response as JSON
    try: analysis = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Response: {text}")
        raise

    return analysis

# Markdown helpers

def md_link(path): return f"[{path}]({path})"

def md_list(prefix, add_func, title, vals):
    add_func(f"**{title}**:\n")
    for v in vals: add_func(f"{prefix} {v}\n")
    add_func("\n")

md_numbered_list = partial(md_list, "1.")
md_bulleted_list = partial(md_list, "-")
