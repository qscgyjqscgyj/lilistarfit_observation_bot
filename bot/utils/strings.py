def chunk_text_by_linebreaks(text, max_length=500):
    lines = text.split("\n")

    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            if not current_chunk:
                current_chunk = line
            else:
                current_chunk += "\n" + line

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
