import spacy
from spacy.matcher import Matcher
from nltk.tokenize.treebank import TreebankWordDetokenizer
import re
import random
from doc_func import add_test_title, add_one_line, add_section_title, add_allowed_time, add_regular_text, add_line_break, add_page_break, add_to_cell, untokenize

prep_ex_text_dir = r'.\source_texts\prep_ex.txt'

def prepositions_exercise_auto(document):
    print("\n" + "-"*30 + "Preposition exercise" + "-"*30)
    choice_bool_char = input("Do you want to give choices?(y/n)")
    if choice_bool_char == 'y':
        choice_bool = True
    elif choice_bool_char == 'n':
        choice_bool = False
    
    print("Reading the source text in " + prep_ex_text_dir + '...')
    f = open(prep_ex_text_dir, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    print("The source text for preposition exercise reads:\n")
    print(text)
    print("\n")
    prep_text, prep_list_str = fill_in_the_blanks_prepositions(text)
    if not choice_bool:
        section_instruction = "Fill in the blanks with the correct form of the given verbs."
    else:
        section_instruction = "Choose the suitable prepositions below to fill in the blanks. You may use each preposition more than once." 
    add_section_title(document, section_instruction)
    if choice_bool:
        table = document.add_table(rows=1, cols=1)
        table.style = 'TableGrid'
        add_to_cell(table, prep_list_str)
    add_regular_text(document, prep_text)
    add_line_break(document)    
    
def fill_in_the_blanks_prepositions(text):
    nlp=spacy.load("en_core_web_sm")
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)

    prep_pattern = [{"TAG": "IN"}]

    matcher.add("preposition", [prep_pattern])

    matches = matcher(doc, as_spans=True)
    prep_list = [str(match).lower() for match in matches]
    random.shuffle(prep_list)

    prep_indices = [match.start for match in matches]

    tokenized = [str(token) for token in doc]

    for idx in prep_indices:
        tokenized[idx] = '__________'
    
    unrepeated_prep_list = list(set(prep_list))
    prep_list_str = '    '.join(unrepeated_prep_list)
    
    processed_text = untokenize(tokenized)

#     processed_text = TreebankWordDetokenizer().detokenize(tokenized)
#     processed_text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', processed_text)
    return processed_text, prep_list_str