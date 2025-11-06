# api_handler.py

from openai import OpenAI

def analyze_job_description(client: OpenAI, model: str, job_desc: str, excluded_terms: list, section_names: dict) -> str:
    """
    يحلل الوصف الوظيفي باستخدام النموذج المحدد ويقترح محتوى للسيرة الذاتية بأسماء أقسام مخصصة.
    """
    
    instructions = []
    format_examples = []
    
    for i, (key, name) in enumerate(section_names.items()):
        if key == 'profile':
            instructions.append(f"{i+1}. **Generate a {name}:** Write a 2-3 sentence professional summary for the top of the CV, tailored to this job.")
            format_examples.append(f"### {name}\nA results-oriented professional with experience in...")
        else:
            instructions.append(f"{i+1}. **Generate {name}:** Create a bulleted list of essential items for this section (like skills, interests, etc.) based on the job description.")
            format_examples.append(f"### {name}\n- Item A\n- Item B")

    dynamic_instructions = "\n".join(instructions)
    dynamic_format_examples = "\n\n".join(format_examples)
    
    prompt = f"""
You are an expert CV and resume assistant. Your task is to analyze the provided job description and generate relevant, concise, and ATS-friendly content for a CV.

**Job Description:**
---
{job_desc}
---

**Instructions:**
{dynamic_instructions}
- **DO NOT use the following words in your response:** {', '.join(excluded_terms) if excluded_terms else "None"}
- **Format your entire response clearly** with headings for each section using "###" followed by the exact section name provided in the instructions. Do not add any extra text before or after the content.

**Example Output Format:**
{dynamic_format_examples}
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def parse_ai_response(response_text: str, section_names: dict) -> dict:
    """
    يحلل استجابة الذكاء الاصطناعي ويستخرج الأقسام المختلفة بناءً على الأسماء المخصصة.
    """
    data = {}
    for key in section_names:
        if key == 'profile':
            data[key] = ""
        else:
            data[key] = []
            
    title_to_key_map = {f"### {name}".lower(): key for key, name in section_names.items()}
    current_section_key = None

    for line in response_text.splitlines():
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        line_lower = line_stripped.lower()

        matched_title = next((title for title in title_to_key_map if line_lower.startswith(title)), None)
        if matched_title:
            current_section_key = title_to_key_map[matched_title]
            continue

        if current_section_key:
            if current_section_key == 'profile':
                if not line_stripped.startswith("###"):
                    data[current_section_key] += line_stripped + " "
            elif line_stripped.startswith("-") or line_stripped.startswith("*"):
                content = line_stripped[1:].strip()
                if isinstance(data.get(current_section_key), list):
                    data[current_section_key].append(content)
    
    if 'profile' in data:
        data['profile'] = data['profile'].strip()
        
    return data