import sys

# Initialize variables
current_word = None
word_count = 0
term_frequency = {}
idf_values = {}  # Assuming we have precomputed IDF values for each word
last_id_for_word = {}  # New dictionary to track the last ID for each word

# Read input from stdin
for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')
    if len(parts) == 3:
        word, id, count = parts[0], parts[1], int(parts[2])  # Convert count to integer
        # Check if it's the same word as the previous one
        if current_word == word:
            word_count += count  # Update word count
            last_id_for_word[word] = id  # Update last seen ID for the word
        else:
            # If moving to a new word, save the previous word's count and ID
            if current_word is not None:
                term_frequency[current_word] = word_count
                # last_id_for_word[current_word] is already updated
            current_word = word
            word_count = count
            last_id_for_word[word] = id  # Update last seen ID for the new word
    else:
        # Handle error or invalid line format
        print(f"Invalid line format: {line}", file=sys.stderr)

# Don't forget the last word
if current_word is not None:
    term_frequency[current_word] = word_count

# Calculate TF-IDF for each word and sort by the TF-IDF value (or word, depending on your preference)
tf_idf = {word: count * idf_values.get(word, 1) for word, count in term_frequency.items()}
sorted_tf_idf = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)  # Sorting by TF-IDF value, descending

# Display the TF-IDF for each word, alongside the last ID seen for that word
for word, tf_idf_value in sorted_tf_idf:
    print(f"{word}\t{tf_idf_value}\t{last_id_for_word[word]}")
