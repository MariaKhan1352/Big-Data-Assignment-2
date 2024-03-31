#!/usr/bin/env python
import sys
import re

# Dictionary to hold word information with the structure {word: [unique_id, count]}
word_info = {}
current_id = 1  # Start ID counter at 1

for line in sys.stdin:
    line = line.strip()
    columns = line.split(',')
    if len(columns) > 3:  # Assuming 'SECTION_TEXT' is at index 3
        section_text = columns[3].lower().replace('\n', '')
        words = re.findall(r'\b\w+\b', section_text)
        for word in words:
            if word not in word_info:
                # Assign a unique ID to the new word, initialize count to 1
                word_info[word] = [current_id, 1]
                current_id += 1
            else:
                # If the word already has an ID, just increment the count
                word_info[word][1] += 1

# Emit each word, its unique ID, and count
for word, (id, count) in word_info.items():
    print(f"{word}\t{id}\t{count}")
