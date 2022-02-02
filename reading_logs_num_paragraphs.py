# from scripts.reading_logs import analyze_num_paragraphs_content_quiz, analyze_num_paragraphs_reading_speed
from scripts.reading_logs.num_paragraphs_analysis import analyze_paragraph_length_reading_speed, \
    analyze_avg_paragraph_length, analyze_num_paragraphs

if __name__ == '__main__':
    analyze_num_paragraphs()
    # analyze_paragraph_length_reading_speed()
    analyze_avg_paragraph_length()
