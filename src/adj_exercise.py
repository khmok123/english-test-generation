import spacy
from spacy.matcher import Matcher
from nltk.tokenize.treebank import TreebankWordDetokenizer
import re
import random
from doc_func import add_test_title, add_one_line, add_section_title, add_allowed_time, add_regular_text, add_line_break, add_page_break, add_to_cell, untokenize

adj_ex_text_dir = r'.\source_texts\adj_ex.txt'

def adj_exercise_auto(document):
    print("\n" + "-"*30 + "Adjective/adverb exercise" + "-"*30)
    choice_bool_char = input("Do you want to give choices?(y/n)")
    if choice_bool_char == 'y':
        choice_bool = True
    elif choice_bool_char == 'n':
        choice_bool = False
        
    comparative_bool_char = input("Do you want to test comparative adjectives?(y/n)")
    superlative_bool_char = input("Do you want to test superlative adjectives?(y/n)")
    adverbs_bool_char = input("Do you want to test adverbs?(y/n)")
    
    if comparative_bool_char == 'y':
        comparative_bool = True
    elif comparative_bool_char == 'n':
        comparative_bool = False
    if superlative_bool_char == 'y':
        superlative_bool = True
    elif superlative_bool_char == 'n':
        superlative_bool = False
    if adverbs_bool_char == 'y':
        adverbs_bool = True
    elif adverbs_bool_char == 'n':
        adverbs_bool = False
        
    print("Reading the source text in " + adj_ex_text_dir + '...')
    f = open(adj_ex_text_dir, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    print("The source text for adjective/adverb exercise reads:\n")
    print(text)
    print("\n")
    adj_text, adj_list_str = fill_in_the_blanks_adjectives(text, comparative=comparative_bool, superlative=superlative_bool, adverbs=adverbs_bool)
    if not choice_bool:
        section_instruction = "Fill in the blanks with the correct form of adjectives or adverbs."
    else:
        section_instruction = "Fill in the blanks with the correct form of adjectives or adverbs. You may use each preposition more than once." 
    add_section_title(document, section_instruction)
    if choice_bool:
        table = document.add_table(rows=1, cols=1)
        table.style = 'TableGrid'
        add_to_cell(table, adj_list_str)
    add_regular_text(document, adj_text)
    add_line_break(document)    




def fill_in_the_blanks_adjectives(text, comparative=True, superlative=True, adverbs=True):
    nlp=spacy.load("en_core_web_sm")
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)

    adj_orig_pattern = [[{"TAG":"JJ"}]]
    adj_comp_pattern = [[{"TAG":"JJR"}],
                       [{"POS":"ADV","TAG":"RBR"},{"TAG":"JJ"}]]
    adj_sup_pattern = [[{"LOWER":"the"},{"TAG":"JJS"}],
                      [{"POS":"ADV","TAG":"RBS"},{"TAG":"JJ"}]]
    adv_orig_pattern = [[{"POS":"ADV"}]]
    adv_comp_pattern = [[{"POS":"ADV","TAG":"RBR"}],
                        [{"POS":"ADV","TAG":"RBR"},{"POS":"ADV","TAG":"RB"}]]
    adv_sup_pattern = [[{"POS":"ADV", "TAG":"RBS"}],
                      [{"POS":"ADV","TAG":"RBS"},{"POS":"ADV","TAG":"RB"}]]
    
    matcher.add("Adjective", adj_orig_pattern,greedy="LONGEST")
    if comparative:
        matcher.add("Adjective (comparative)", adj_comp_pattern, greedy="LONGEST")
    if superlative:
        matcher.add("Adjective (superlative)", adj_sup_pattern, greedy="LONGEST")
    if adverbs:
        matcher.add("Adverb", adv_orig_pattern,greedy="LONGEST")
    if adverbs and comparative:
        matcher.add("Adverb (comparative)", adv_comp_pattern, greedy="LONGEST")
    if adverbs and superlative:
        matcher.add("Adverb (superlative)", adv_sup_pattern, greedy="LONGEST")
        
    matches = matcher(doc)
    adj_list = [doc[start].lemma_ for _,start,end in matches]
    random.shuffle(adj_list)
    unrepeated_adj_list = list(set(adj_list))
    adj_list_str = '    '.join(unrepeated_adj_list)
#     for match_id, start, end in matches:
#         string_id = nlp.vocab.strings[match_id]  # Get string representation
#         span = doc[start:end]  # The matched span
#         print(string_id, start, end, span.text)
        
    indices = [start for _,start,_ in matches]

    tokenized = [str(token) for token in doc]

    for idx in indices:
        tokenized[idx] = '_'*16
        
    processed_text = untokenize(tokenized)
    
    return processed_text, adj_list_str
        
    
