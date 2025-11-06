import re
from collections import Counter
from pathlib import Path
from typing import List, Tuple, Dict

def analyze_word_frequency(file_path: str) -> List[Tuple[str, int]]:
    """
    Analyzes a file, extracts words of 3 or more characters, and returns 
    a sorted list of word counts from most frequent to least frequent.

    Args:
        file_path: The path to the file to analyze.

    Returns:
        A list of tuples (word, count) sorted by count descending.
    """
    
    # 1. Read the file content
    file = Path(file_path)
    if not file.exists():
        print(f"Error: File not found at '{file_path}'")
        return []
    
    try:
        text = file.read_text(encoding='utf-8').lower()
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    # 2. Extract words
    # The regex pattern r'\b\w{3,}\b' finds sequences of 3 or more 
    # alphanumeric characters (including underscore) that are whole words.
    words = re.findall(r'\b\w{3,}\b', text)
    
    # 3. Count word occurrences
    # Counter is highly efficient for counting hashable objects.
    word_counts = Counter(words)
    
    # 4. Return sorted list
    # most_common() returns a list of (element, count) tuples, 
    # sorted from most to least common.
    return word_counts.most_common()

def print_word_analysis(results: List[Tuple[str, int]]):
    """Prints the analysis results in a readable format."""
    
    if not results:
        print("No words found or file analysis failed.")
        return

    total_unique_words = len(results)
    total_occurrences = sum(count for word, count in results)

    print("\n" + "="*50)
    print(f"🎉 Word Frequency Analysis")
    print("="*50)
    print(f"Total Unique Words (>= 3 chars): **{total_unique_words:,}**")
    print(f"Total Word Occurrences: **{total_occurrences:,}**")
    print("-"*50)
    
    print("\nTop 20 Most Frequent Words:")
    # Print the top 20 or all, whichever is smaller
    for word, count in results[:40]:
        # Using ljust to align the word column
        print(f"  {word.ljust(40)} : {count:,}")
        
    print("\n" + "="*50)


# --- Example Usage ---
if __name__ == "__main__":
    # --- ⚠️ IMPORTANT: Change this to the path of your file ---
    target_file = "pygone-mini.py" 
    
    # 1. Run the analysis
    analysis_results = analyze_word_frequency(target_file)
    
    # 2. Print the results
    print_word_analysis(analysis_results)
    
    # 3. Access the full list of unique results
    # Example: Get the 50th most frequent word and its count (if it exists)
    if len(analysis_results) >= 50:
        word, count = analysis_results[49] # index 49 is the 50th element
        print(f"\nExample Check: 50th most frequent word is '{word}' ({count:,} times)")