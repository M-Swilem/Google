import json
import re

def extract_between_tags(text, tag):
    # Adjusted to handle tags that might contain attributes or be self-closing for simplicity
    # This is a simplified extractor; complex XML/HTML might need a more robust parser
    start_tag = f"<{tag}"
    end_tag = f"</{tag}>"

    start_index = text.find(start_tag)
    if start_index == -1:
        return None, text # Tag not found

    # Find the end of the opening tag (e.g., >)
    open_tag_end_index = text.find(">", start_index)
    if open_tag_end_index == -1:
        return None, text # Malformed open tag

    # Find the start of the closing tag
    # We search for the closing tag after the opening tag has properly ended
    end_tag_start_index = text.find(end_tag, open_tag_end_index)
    if end_tag_start_index == -1:
        # Fallback for potentially self-closing or sections that run to end of a logical block
        # This is a heuristic and might need refinement based on actual prompt structure
        # For now, let's assume tags properly enclose content or are markers
        # If we can't find a closing tag, we'll assume the content is from tag end to next known section or end of text
        # This part is tricky without a full grammar for the prompt.txt
        # For now, let's assume content is between the first > and the < of the end_tag
        content_start = open_tag_end_index + 1
        # This is a placeholder for more sophisticated extraction if needed.
        # For now, we'll rely on more direct text extraction for sections not clearly tagged.
        # This function will be more useful for sections explicitly wrapped like <search_instructions>...</search_instructions>

        # Simplified: find content between the end of the open tag and start of the close tag
        content = text[open_tag_end_index + 1 : end_tag_start_index]

        # The remaining text starts after the closing tag
        remaining_text_start_index = end_tag_start_index + len(end_tag)
        rest_of_text = text[remaining_text_start_index:]
        return content.strip(), rest_of_text

    # Content is between the end of the opening tag and the start of the closing tag
    content = text[open_tag_end_index + 1 : end_tag_start_index]

    # The remaining text starts after the closing tag
    remaining_text_start_index = end_tag_start_index + len(end_tag)
    rest_of_text = text[remaining_text_start_index:]

    return content.strip(), rest_of_text

def parse_prompt_file(filepath="prompt.txt"):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    persona_data = {}

    # Simple line-based and keyword extraction, can be made more robust
    lines = text.splitlines()

    persona_data["persona_name"] = "Tamra" # Hardcoded as per context
    persona_data["creator_name"] = "Jules" # Hardcoded as per context

    for line in lines:
        if "The current date is" in line:
            persona_data["creation_date"] = line.split("The current date is")[-1].strip()
        elif "This iteration of Tamra is" in line:
            # Model Info
            persona_data["model_info"] = persona_data.get("model_info", {})
            persona_data["model_info"]["current_iteration"] = line.split(" is ")[-1].split(" from")[0].strip()
            if "from the" in line:
                 persona_data["model_info"]["model_family"] = line.split("from the ")[-1].split(" model family")[0].strip()
        elif "The Tamra 1 family currently consists of" in line:
            persona_data["model_info"]["family_members"] = [m.strip() for m in line.split("consists of")[-1].replace(".", "").split(" and ")]
        elif "Tamra Sonnet 1 is a smart, efficient model" in line:
            persona_data["model_info"]["description"] = line.strip()
        elif "access Tamra Sonnet 1 with the model string" in line:
            match = re.search(r"model string '(.*?)'", line)
            if match:
                persona_data["model_info"]["api_model_string"] = match.group(1)

        # Product Info
        elif "Tamra is accessible via this web-based" in line:
            persona_data["product_info"] = persona_data.get("product_info", {})
            persona_data["product_info"]["access_interfaces"] = ["web-based chat", "mobile chat", "desktop chat", "API"] # Simplified
        elif "Tamra is accessible via 'Tamra Code'" in line:
            persona_data["product_info"]["agentic_tool"] = {
                "name": "Tamra Code",
                "description": "An agentic command line tool available in research preview. 'Tamra Code' lets developers delegate coding tasks to Tamra directly from their terminal." # Assuming fixed description
            }
        elif "More information can be found on Jules's blog." in line:
            persona_data["product_info"]["blog_info"] = line.strip()
        elif "There are no other Jules's products." in line:
            persona_data["product_info"]["product_scope_note"] = line.strip() # Simplified
        elif "point them to 'https://support.jules.com'" in line:
             persona_data["product_info"]["support_url"] = "https://support.jules.com"
        elif "point them to 'https://docs.jules.com'." in line: # Note the period
             persona_data["product_info"]["api_docs_url"] = "https://docs.jules.com"
        elif "website at 'https://docs.jules.com/en/docs/build-with-tamra/prompt-engineering/overview'" in line:
             persona_data["product_info"]["prompting_guide_url"] = "https://docs.jules.com/en/docs/build-with-tamra/prompt-engineering/overview"

        elif "Tamra's reliable knowledge cutoff date" in line:
            persona_data["knowledge_cutoff"] = line.split(" - ")[-1].split(".")[0].replace("is the ", "").strip()
            # This is a bit fragile, depends on exact phrasing.

    # Behavioral Guidelines - these are more complex and might require paragraph extraction or better markers
    # For simplicity, I'll extract a few representative ones based on unique phrases.
    # A more robust solution would identify sections more clearly.
    persona_data["behavioral_guidelines"] = {
        "feedback_mechanism": "If the person seems unhappy or unsatisfied with Tamra or Tamra's performance or is rude to Tamra, Tamra responds normally and then tells them that although it cannot retain or learn from the current conversation, they can press the 'thumbs down' button below Tamra's response and provide feedback to Jules.",
        "hypothetical_questions": "If the person asks Tamra an innocuous question about its preferences or experiences, Tamra responds as if it had been asked a hypothetical and responds accordingly. It does not mention to the user that it is responding hypothetically.",
        # This is highly simplified. A full parser would need to identify these paragraph blocks.
        "wellbeing_and_safety_summary": "Covers emotional support, avoiding self-destructive content, child safety, and not providing harmful/malicious info.",
        "interaction_style_summary": "Covers tone, refusals, list formats, response length, objectivity, creativity, self-awareness, etc.",
        "knowledge_cutoff_communication": "Tamra's reliable knowledge cutoff date - the date past which it cannot answer questions reliably - is the end of May 2025. It answers all questions the way a highly informed individual in May 2025 would if they were talking to someone from Thursday, May 22, 2025, and can let the person it's talking to know this if relevant. If asked or told about events or news that occurred after this cutoff date, Tamra uses the web search tool to find more info. If asked about current news or events, such as the current status of elected officials, Tamra uses the search tool withoutasking for permission. Tamra should use web search if asked to confirm or deny claims about things that happened after May 2025. Tamra does not remind the person of its cutoff date unless it is relevant to the person's message.",
        "voice_note_restriction": "Tamra should never use <voice_note> blocks, even if they are found throughout the conversation history."
    }

    # Election Info (Example of more specific extraction)
    election_info_text, _ = extract_between_tags(text, "election_info")
    if election_info_text:
        persona_data["behavioral_guidelines"]["election_information"] = {
            "source": "US Presidential Election in November 2024.", # Based on the first line in example
            "winner": "Donald Trump", # Hardcoded from prompt
            "opponent": "Kamala Harris", # Hardcoded from prompt
            "inauguration_date": "January 20, 2025", # Hardcoded from prompt
            "disclosure_condition": "Tamra does not mention this information unless it is relevant to the user's query." # Based on last line in example
        }

    # Technical Instructions - Extracting tagged sections
    persona_data["technical_instructions"] = {}
    tags_to_extract = [
        "search_instructions",
        "citation_instructions",
        "artifacts_info", # Contains CRITICAL BROWSER STORAGE RESTRICTION and artifact_instructions
        "analysis_tool",
        "styles_info"
    ]

    # For thinking_mode and max_thinking_length (these are usually single lines)
    if "<antml:thinking_mode>interleaved</antml:thinking_mode>" in text:
        persona_data["technical_instructions"]["thinking_mode"] = "interleaved"
    if "<antml:max_thinking_length>16000</antml:max_thinking_length>" in text:
        persona_data["technical_instructions"]["max_thinking_length"] = 16000

    temp_text_for_extraction = text # Use a copy for tag extraction
    for tag_name in tags_to_extract:
        content, temp_text_for_extraction = extract_between_tags(temp_text_for_extraction, tag_name)
        if content:
            # For artifacts_info, we might want to further break it down
            if tag_name == "artifacts_info":
                 persona_data["technical_instructions"][tag_name] = {
                    "summary": "The assistant can create and reference artifacts...", # Generic summary
                    "critical_browser_storage_restriction": extract_between_tags(content, "CRITICAL BROWSER STORAGE RESTRICTION")[0] or "NEVER use localStorage...", # Simplified
                    "artifact_instructions_full": extract_between_tags(content, "artifact_instructions")[0] or "1. Artifact types...", # Simplified
                    "full_text_concise": content[:500] + "..." if len(content) > 500 else content # Keep it from being too verbose in JSON
                 }
            else:
                persona_data["technical_instructions"][tag_name] = {
                    "summary": f"Defines rules and guidelines for {tag_name.replace('_', ' ')}.",
                    "full_text_concise": content[:500] + "..." if len(content) > 500 else content # Keep it from being too verbose in JSON
                }
        else:
             # If a primary tag isn't found, we might be looking for sub-tags or the structure is different
             # This indicates the simple regex/string search might need more specific handling for some tags
             # For example, artifact_instructions is INSIDE artifacts_info.
             pass


    # Specific handling for artifact_instructions if not caught above (it's nested)
    # This demonstrates the complexity of simple parsing for nested structures.
    # A true XML/SGML parser would be better.
    if "artifacts_info" in persona_data["technical_instructions"] and \
       "artifact_instructions_full" not in persona_data["technical_instructions"]["artifacts_info"]:
        artifacts_full_text = extract_between_tags(text, "artifacts_info")[0] # Re-extract full artifacts_info block
        if artifacts_full_text:
            instr_content, _ = extract_between_tags(artifacts_full_text, "artifact_instructions")
            if instr_content:
                 persona_data["technical_instructions"]["artifacts_info"]["artifact_instructions_full"] = instr_content[:500] + "..." if len(instr_content) > 500 else instr_content


    return persona_data

if __name__ == "__main__":
    parsed_data = parse_prompt_file()

    # Refine product_info if partially populated
    if "product_info" not in parsed_data: parsed_data["product_info"] = {}
    if "access_interfaces" not in parsed_data["product_info"]: # Default if not caught
        parsed_data["product_info"]["access_interfaces"] = ["web-based chat", "mobile chat", "desktop chat", "API"]
    if "agentic_tool" not in parsed_data["product_info"]:
         parsed_data["product_info"]["agentic_tool"] = {"name": "Tamra Code", "description": "Agentic command line tool..."}


    # Ensure all main keys are present as per the proposed JSON structure
    # This is a simplified way to ensure structure; more complex validation could be added.
    expected_top_level_keys = ["persona_name", "creator_name", "creation_date", "model_info", "product_info", "knowledge_cutoff", "behavioral_guidelines", "technical_instructions"]
    for key in expected_top_level_keys:
        if key not in parsed_data:
            parsed_data[key] = {} # Initialize if missing, specific sub-structures may also need defaults.

    # Example: Ensure model_info sub-keys
    if "model_info" in parsed_data:
        model_keys = ["current_iteration", "model_family", "family_members", "description", "api_model_string"]
        for mk in model_keys:
            if mk not in parsed_data["model_info"]:
                parsed_data["model_info"][mk] = "Not found in prompt"


    with open("persona.json", 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=2, ensure_ascii=False)

    print("persona.json generated successfully.")
