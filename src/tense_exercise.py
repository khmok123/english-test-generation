import spacy
from spacy.matcher import Matcher
import re
from numpy.random import choice
from doc_func import add_test_title, add_one_line, add_section_title, add_allowed_time, add_regular_text, add_line_break, add_page_break, untokenize

tense_ex_text_dir = r'.\source_texts\tense_ex.txt'

def tense_exercise_auto(document,grade):
    print("\n" + "-"*30 + "Tense Exercise" + "-"*30)
    print("Reading the source text in " + tense_ex_text_dir + '...')
    check_tense_blanks_number(grade)
    f = open(tense_ex_text_dir, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    print("The source text for tense exercise reads:\n")
    print(text)
    print("\n")
    a_p = input("All blanks or partial blanks? (a/p)")
    if a_p == 'a':
        blanks_number = None
    elif a_p == 'p':
        blanks_number = int(input("How many blanks in text exercise do you want?"))
    else:
        blanks_number = None
    tense_string = tense_exercise_string(text, grade=grade, blanks_number=blanks_number,
                                          factor=1.2)
    add_section_title(document, "Fill in the blanks with the correct form of the given verbs.")
    add_regular_text(document, tense_string)
    add_line_break(document)
    
def check_tense_blanks_number(grade):
    f = open(tense_ex_text_dir, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    tense_bool_dict = grade_to_tense(grade)
# Remove parentheses and the contents contained in them
    text = re.sub(r'\([^)]*\)', '',text)
    nlp=spacy.load("en_core_web_sm")

    tenses_priority = ["future_perfect_continuous","past_perfect_continuous",
                      "present_perfect_continuous", "future_perfect", "past_perfect",
                      "present_perfect", "future_continuous", "past_continuous",
                      "present_continuous", "future_tense", "past_tense", "present_tense", '']

    not_list = ["not", "n\'t"]
    is_list = ["is","am","are","\'s","\'re","ain\'t"]
    is_list_q = ["is", "am", "are"]
    do_list = ["do", "does"]
    was_list = ["was","were"]
    will_list = ["will","wo","shall"]
    have_list = ["have","\'ve","has","\'s"]
    adv_dict = {"TAG":"RB","OP":"*"}
    noun_dict = {"TAG":{"IN":["PRP","NN","NNP"]}}

    blank = '_'*16

    matcher = Matcher(nlp.vocab)
    present_tense_pattern = [[{"TAG":{"IN":["VBP","VBZ"]}},adv_dict,{"TAG":"VB", "OP":"*"}],
                    [{"LOWER":{"IN":do_list}},adv_dict,noun_dict,adv_dict,{"TAG":"VB"}],
                    [{"LOWER":{"IN":is_list_q}},adv_dict,noun_dict]]

    past_tense_pattern = [[{"LOWER":"did"},adv_dict,{"TAG":"VB"}],
                        [{"TAG":"VBD"}],
                         [{"LOWER":{"IN":was_list+["did"]}},adv_dict,{"TAG":"PRP"},adv_dict]]
    future_tense_pattern = [[{"LOWER":{"IN":will_list}},adv_dict,{"TAG":"VB"}]]
    present_cont_pattern = [[{"LOWER":{"IN":is_list}},adv_dict,{"TAG":"VBG"}]]
    past_cont_pattern = [[{"LOWER":{"IN":was_list}},adv_dict,{"TAG":"VBG"}]]
    future_cont_pattern = [[{"LOWER":{"IN":will_list}},adv_dict,
                           {"LOWER":"be"},adv_dict,{"TAG":"VBG"}]]
    present_perfect_pattern = [[{"LOWER":{"IN":have_list}},
                                adv_dict,{"TAG":"VBN"}]]
    past_perfect_pattern = [[{"LOWER":"had"},adv_dict,{"TAG":"VBN"}]]
    future_perfect_pattern = [[{"LOWER":{"IN":will_list}},adv_dict,
                              {"LOWER":{"IN":have_list}},adv_dict,{"TAG":"VBN"}]]
    present_perfect_cont_pattern = [[{"LOWER":{"IN":have_list}},adv_dict,
                                     {"LOWER":"been"},adv_dict,
                                     {"TAG":"VBG"}]]
    past_perfect_cont_pattern = [[{"LOWER":"had"},adv_dict,{"LOWER":"been"},
                                  adv_dict,{"TAG":"VBG"}]]
    future_perfect_cont_pattern = [[{"LOWER":{"IN":will_list}},adv_dict,{"LOWER":"have"},
                                    adv_dict,{"LOWER":"been"},adv_dict,
                                    {"TAG":"VBG"}]]



    doc = nlp(text)
    matcher.add("present_tense", present_tense_pattern, greedy='LONGEST')
    # matcher.add("present_tense_question", present_tense_q)
    matcher.add("past_tense", past_tense_pattern, greedy='LONGEST')
    matcher.add("future_tense", future_tense_pattern)
    matcher.add("present_continuous", present_cont_pattern)
    matcher.add("past_continuous", past_cont_pattern)
    matcher.add("future_continuous", future_cont_pattern)
    matcher.add("present_perfect", present_perfect_pattern)
    matcher.add("past_perfect", past_perfect_pattern)
    matcher.add("future_perfect", future_perfect_pattern)
    matcher.add("present_perfect_continuous", present_perfect_cont_pattern)
    matcher.add("past_perfect_continuous", past_perfect_cont_pattern)
    matcher.add("future_perfect_continuous", future_perfect_cont_pattern)

    matches = matcher(doc)
    matches.sort(key=lambda x:x[1])

    matches = get_greedy_matches(matches)
    matches_copy = matches
    
    underline_i = []
    add_bracket = []
        
    for idx, (match_id, start, end) in enumerate(matches):
        if not tense_bool_dict[nlp.vocab.strings[match_id]]:
            matches_copy.remove(matches[idx])
    matches = matches_copy
    print("Number of blanks:", len(matches))
    
    
def tense_exercise_string(text, grade=6, blanks_number=20, factor=1.2):
    
    tense_bool_dict = grade_to_tense(grade)
# Remove parentheses and the contents contained in them
    text = re.sub(r'\([^)]*\)', '',text)
    nlp=spacy.load("en_core_web_sm")

    tenses_priority = ["future_perfect_continuous","past_perfect_continuous",
                      "present_perfect_continuous", "future_perfect", "past_perfect",
                      "present_perfect", "future_continuous", "past_continuous",
                      "present_continuous", "future_tense", "past_tense", "present_tense", '']

    not_list = ["not", "n\'t"]
    is_list = ["is","am","are","\'s","\'re","ain\'t"]
    is_list_q = ["is", "am", "are"]
    do_list = ["do", "does"]
    was_list = ["was","were"]
    will_list = ["will","wo","shall"]
    have_list = ["have","\'ve","has","\'s"]
    adv_dict = {"TAG":"RB","OP":"*"}
    noun_dict = {"TAG":{"IN":["PRP","NN","NNP"]}}

    blank = '_'*16

    matcher = Matcher(nlp.vocab)
    present_tense_pattern = [[{"TAG":{"IN":["VBP","VBZ"]}},adv_dict,{"TAG":"VB", "OP":"*"}],
                    [{"LOWER":{"IN":do_list}},adv_dict,noun_dict,adv_dict,{"TAG":"VB"}],
                    [{"LOWER":{"IN":is_list_q}},adv_dict,noun_dict]]

    past_tense_pattern = [[{"LOWER":"did"},adv_dict,{"TAG":"VB"}],
                        [{"TAG":"VBD"}],
                         [{"LOWER":{"IN":was_list+["did"]}},adv_dict,{"TAG":"PRP"},adv_dict]]
    future_tense_pattern = [[{"LOWER":{"IN":will_list}},adv_dict,{"TAG":"VB"}]]
    present_cont_pattern = [[{"LOWER":{"IN":is_list}},adv_dict,{"TAG":"VBG"}]]
    past_cont_pattern = [[{"LOWER":{"IN":was_list}},adv_dict,{"TAG":"VBG"}]]
    future_cont_pattern = [[{"LOWER":{"IN":will_list}},adv_dict,
                           {"LOWER":"be"},adv_dict,{"TAG":"VBG"}]]
    present_perfect_pattern = [[{"LOWER":{"IN":have_list}},
                                adv_dict,{"TAG":"VBN"}]]
    past_perfect_pattern = [[{"LOWER":"had"},adv_dict,{"TAG":"VBN"}]]
    future_perfect_pattern = [[{"LOWER":{"IN":will_list}},adv_dict,
                              {"LOWER":{"IN":have_list}},adv_dict,{"TAG":"VBN"}]]
    present_perfect_cont_pattern = [[{"LOWER":{"IN":have_list}},adv_dict,
                                     {"LOWER":"been"},adv_dict,
                                     {"TAG":"VBG"}]]
    past_perfect_cont_pattern = [[{"LOWER":"had"},adv_dict,{"LOWER":"been"},
                                  adv_dict,{"TAG":"VBG"}]]
    future_perfect_cont_pattern = [[{"LOWER":{"IN":will_list}},adv_dict,{"LOWER":"have"},
                                    adv_dict,{"LOWER":"been"},adv_dict,
                                    {"TAG":"VBG"}]]



    doc = nlp(text)
    matcher.add("present_tense", present_tense_pattern, greedy='LONGEST')
    # matcher.add("present_tense_question", present_tense_q)
    matcher.add("past_tense", past_tense_pattern, greedy='LONGEST')
    matcher.add("future_tense", future_tense_pattern)
    matcher.add("present_continuous", present_cont_pattern)
    matcher.add("past_continuous", past_cont_pattern)
    matcher.add("future_continuous", future_cont_pattern)
    matcher.add("present_perfect", present_perfect_pattern)
    matcher.add("past_perfect", past_perfect_pattern)
    matcher.add("future_perfect", future_perfect_pattern)
    matcher.add("present_perfect_continuous", present_perfect_cont_pattern)
    matcher.add("past_perfect_continuous", past_perfect_cont_pattern)
    matcher.add("future_perfect_continuous", future_perfect_cont_pattern)

    matches = matcher(doc)
    matches.sort(key=lambda x:x[1])

    matches = get_greedy_matches(matches)
    matches_copy = matches
    
    underline_i = []
    add_bracket = []
        
    for idx, (match_id, start, end) in enumerate(matches):
        if not tense_bool_dict[nlp.vocab.strings[match_id]]:
            matches_copy.remove(matches[idx])
    matches = matches_copy
    
    matches_str = [nlp.vocab.strings[match_id] for match_id,_,_ in matches]
    prob_list = tense_list_to_prob(matches_str, factor=factor)
    
    if blanks_number == None:
        blanks_number = len(matches)
    #-----------------
#     print('len(matches)', len(matches))
#     print('list(range(len(matches)))',list(range(len(matches))))
#     print('prob_list', prob_list)
#     print('blanks_number', blanks_number)
#     print('choice(...)', choice(list(range(len(matches))),blanks_number,p=prob_list,replace=False))
    #-----------------

    sampled_blanks = sorted(choice(list(range(len(matches))),blanks_number,p=prob_list,replace=False))
    
    for idx,(match_id, start, end) in enumerate(matches):
        if idx in sampled_blanks:
            lemma = ''
            string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
#             print(string_id, start, end, span.text)
            with_not = False
            for idx,token in enumerate(span):
                verbs = []
                if str(token) in not_list:
                    with_not = True
                if token.pos_ != 'AUX' and token.pos_ != 'PART' and token.pos_ != 'VERB':
                    pass
                elif token.pos_ == 'VERB':
                    verbs.append(token)
                    lemma = token.lemma_
                    underline_i.append(token.i)
                else:
                    underline_i.append(token.i)
            if not verbs:
                lemma = 'be'
                underline_i.append(token.i)
            if idx == len(span)-1:
                if with_not:
                    add_bracket.append((token.i,'not ' + str(lemma)))
                else:
                    add_bracket.append((token.i,str(lemma)))

    underline_i = sorted(list(set(underline_i)))
    bracket_idx_list, lemma_list = list(list(zip(*add_bracket))[0]), list(list(zip(*add_bracket))[1])

    tokenized = [str(token) for token in doc]
    for i,word in enumerate(tokenized):
        if i in bracket_idx_list:
            tokenized[i] = blank + '(' + lemma_list[bracket_idx_list.index(i)] + ')'
        elif i in underline_i:
            tokenized[i] = blank
            
    processed_text = untokenize(tokenized)

    # Combine the neighboring blanks
    processed_text = re.sub(r'(' + blank + ' |' + blank + ')+', blank+' ', processed_text)
    return processed_text

def tense_list_to_prob(tense_list, factor=1.5):
    prob_dict = {"present_tense":1, "present_continuous":factor, 
                "past_tense":factor**2, "future_tense":factor**2,
                "past_continuous":factor**3, "present_perfect":factor**4,
                "past_perfect":factor**5, "future_continuous":factor**6,
                "future_perfect":factor**6, "present_perfect_continuous":factor**7,
                "past_perfect_continuous":factor**7, "future_perfect_continuous":factor**7}
    prob_list_unnormalized = []
    for tense in tense_list:
        prob_list_unnormalized.append(prob_dict[tense])
    prob_list = [prob/sum(prob_list_unnormalized) for prob in prob_list_unnormalized]
    return prob_list



def grade_to_tense(grade):
    assert grade <= 6 and grade > 0
    tense_list = ["present_tense", "past_tense", "future_tense",
                  "present_continuous", "past_continuous", "future_continuous",
                  "present_perfect", "past_perfect", "future_perfect",
                  "present_perfect_continuous", "past_perfect_continuous", 
                  "future_perfect_continuous"]
    tense_grade_dict = {1: ["present_tense"],
                        2: ["present_tense", "present_continuous"],
                        3: ["present_tense", "present_continuous", "past_tense",                                         "future_tense"],
                       4: ["present_tense", "present_continuous", "past_tense", "future_tense", "past_continuous"],
                       5: ["present_tense", "present_continuous", "past_tense", "future_tense", "past_continuous", "present_perfect"],
                       6:  ["present_tense", "present_continuous", "past_tense","future_tense", "past_continuous", "present_perfect","past_perfect"]}
    
    tense_bool_dict = dict()
    for tense in tense_list:
        if tense in tense_grade_dict[grade]:
            tense_bool_dict[tense] = True
        else:
            tense_bool_dict[tense] = False
    return tense_bool_dict
        

def get_greedy_matches(matches):
    
    intervals = [[match[1],match[2]] for match in matches]
    
    sorted_by_lower_bound = sorted(intervals, key=lambda tup: tup[0])
    merged = []

    for higher in sorted_by_lower_bound:
        if not merged:
            merged.append(higher)
        else:
            lower = merged[-1]
            # test for intersection between lower and higher:
            # we know via sorting that lower[0] <= higher[0]
            if higher[0] <= lower[1]:
                upper_bound = max(lower[1], higher[1])
                merged[-1] = [lower[0], upper_bound]  # replace by merged interval
            else:
                merged.append(higher)
    indices = []
    errors = 0
    error_merges = []
    
    for merge in merged:
        try:
            indices.append(intervals.index(merge))
        except:
            errors += 1
            error_merges.append(merge)
                
    new_matches = [matches[index] for index in indices]
    
    return new_matches

# def untokenize(words):
#     """
#     Untokenizing a text undoes the tokenizing operation, restoring
#     punctuation and spaces to the places that people expect them to be.
#     Ideally, `untokenize(tokenize(text))` should be identical to `text`,
#     except for line breaks.
#     """
#     text = ' '.join(words)
#     step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
#     step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
#     step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
#     step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
#     step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
#          "can not", "cannot")
#     step6 = step5.replace(" ` ", " '")
#     return step6.strip()