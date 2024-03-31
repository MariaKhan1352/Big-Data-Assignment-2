#!/usr/bin/env python
import sys
import re

# Dictionary to hold word information with the structure {word: [unique_id, count]}
word_info = {}
current_id = 1  # Start ID counter at 1
document_count = 0
word_df = {}


def emit_word_info():
    for word, (id, count) in word_info.items():
        print(f"WordInfo\t{word}\t{id}\t{count}")


# Function to calculate IDF 
def calculate_idf(total_documents, document_frequency):
    if document_frequency == 0:
        return 0
    else:
        idf = total_documents / document_frequency
        idf = 1 + (idf ** (1 / 3))  
        return idf


# Function to generate vectorized representation of the query
def generate_query_vector(query):
    query_vector = {}
    query_words = re.findall(r'\b\w+\b', query.lower())
    for word in query_words:
        if word in word_info:
            word_id = word_info[word][0]
            if word_id in query_vector:
                query_vector[word_id] += 1
            else:
                query_vector[word_id] = 1
    return query_vector


# Read query input
query = sys.stdin.readline().strip()

# Generate vectorized representation of the query
query_vector = generate_query_vector(query)

# Emit query vector
for word_id, count in query_vector.items():
    print(f"Query\t{word_id}\t{count}")

# Process document corpus
for line in sys.stdin:
    line = line.strip()
    columns = line.split(',')
    if len(columns) > 3:  # Assuming 'SECTION_TEXT' is at index 3
        document_id = columns[0]  # Assuming document ID is the first column
        section_text = columns[3].lower().replace('\n', '')
        words = re.findall(r'\b\w+\b', section_text)
        document_count += 1
        document_words = set()
        for word in words:
            if word in word_info:
                word_id = word_info[word][0]
                if word_id in document_words:
                    continue
                if word_id in word_df:
                    word_df[word_id] += 1
                else:
                    word_df[word_id] = 1
                document_words.add(word_id)
            else:
                word_info[word] = (current_id, 1)
                word_id = current_id
                current_id += 1
                word_df[word_id] = 1
        document_vector = {}
        for word in words:
            word_id = word_info[word][0]
            if word_id in document_vector:
                document_vector[word_id] += 1
            else:
                document_vector[word_id] = 1
        # Emit document TF representation along with document ID
        for word_id, count in document_vector.items():
            print(f"{document_id}\t{word_id}\t{count}")

# Emit word information
emit_word_info()

# Emit document count
print(f"DocumentCount\t{document_count}")

# Emit word document frequency
for word_id, df in word_df.items():
    print(f"WordDF\t{word_id}\t{df}")
