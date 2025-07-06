import json
import os

def get_file_content(filename):
    """Reads the content of a file and returns it as a string."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{filename}' not found."
    except Exception as e:
        return f"Error reading file '{filename}': {str(e)}"

def main():
    """
    Reads all persona-related markdown files and compiles them into a single JSON object,
    then prints the JSON object to standard output.
    """
    persona_files = [
        "persona_attributes.md",
        "interaction_prompts_responses.md",
        "llm_implementation_guidelines.md",
        "example_scenarios.md",
        "llm_refinement_log.md",
        "PROFESSOR_NONA_GUIDE.md"
    ]

    # For local testing, if files are in a subdirectory (e.g., 'persona_docs')
    # you might prepend a path. Assuming they are in the same directory as the script for now.
    # script_dir = os.path.dirname(__file__)

    persona_data = {}

    for md_file in persona_files:
        # In a real repo, ensure these paths are correct relative to script execution
        # file_path = os.path.join(script_dir, md_file) # Use this if files are co-located
        file_path = md_file # Assuming files are in current working directory when script runs

        content = get_file_content(file_path)
        # Use a descriptive key, e.g., removing the .md extension
        key_name = md_file.replace(".md", "")
        persona_data[key_name] = content

    # Serialize the dictionary to a JSON formatted string
    try:
        json_output = json.dumps(persona_data, indent=4)
        print(json_output)
    except TypeError as e:
        print(f"Error serializing data to JSON: {str(e)}")
        # Fallback: print the dictionary representation if JSON serialization fails
        # This can happen if file read errors introduced non-serializable content.
        print("\nRaw data (due to JSON serialization error):")
        print(persona_data)

if __name__ == "__main__":
    main()
