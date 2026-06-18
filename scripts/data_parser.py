import os
import json
import re
from pathlib import Path
from config.config import OUTPUT_DATA_DIR, RAW_DIR

def parse_srt(file_path) -> list:

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    
    # Extract season and episode from the filename
    filename = os.path.basename(file_path)
    name_found = re.search(r"S(\d{2})E(\d{2})", filename, re.IGNORECASE)
    if not name_found:
        raise ValueError(f"Filename {filename} does not match the expected format.")
    season, episode = map(int, name_found.groups())

    # Read the content of the SRT file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split the content into blocks
    blocks = re.split(r'\n\n+', content.strip())
    
    replies = []
    buffer = ""
    buffer_time_code = None

    # Process each block to extract time codes and text
    for i, block in enumerate(blocks):
        lines = block.split('\n')
        time_code = lines[1] if len(lines) > 1 else None
        text = " ".join(re.sub(r'<[^>]+>', '', line).removeprefix("- ") for line in lines[2:]) if len(lines) > 2 else ''
        if "перевод субтитров" in text.lower() or "netflix" in text.lower():
            continue
        if not buffer:
            buffer_time_code = time_code
        buffer += (" " + text if buffer else text)
        next_text = " ".join(re.sub(r'<[^>]+>', '', line) for line in blocks[i + 1].split('\n')[2:]) if i + 1 < len(blocks) else ''
        if buffer.endswith(('.', '!', '?')) and (i == len(blocks) - 1 or not next_text.islower()):
            if buffer.strip():
                replies.append({"season": season, "episode": episode, "time_code": buffer_time_code, "text": buffer.strip()})
            buffer = ""
            buffer_time_code = None
        else:
            continue
    
    # Handle any remaining buffer after processing all blocks
    if buffer.strip():
        replies.append({"season": season, "episode": episode, "time_code": buffer_time_code, "text": buffer.strip()})
    
    # Save the parsed replies to a JSON file
    output_file = os.path.join(OUTPUT_DATA_DIR, f"S{season}E{episode}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(replies, f, ensure_ascii=False, indent=4)

    print(f"Parsed replies saved to {output_file} at {OUTPUT_DATA_DIR}")
    return replies

if __name__ == "__main__":
    raw_dir = RAW_DIR
    files = Path(raw_dir).glob("*.srt")
    total_replies = 0
    total_files = 0
    for file in files:
        try:
            replies = parse_srt(file)
            total_replies += len(replies)
            total_files += 1
        except ValueError as e:
            print(f"Skipping file {file}: {e}")
        except FileNotFoundError as e:
            print(e)
    print(f"Обработано {total_files} файлов, всего {total_replies} реплик")