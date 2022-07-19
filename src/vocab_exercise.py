from bs4 import BeautifulSoup
import requests, operator, re, json, requests, spacy, random
from doc_func import add_test_title, add_one_line, add_section_title, add_allowed_time, add_regular_text, add_line_break, add_page_break

vocab_ex_words_dir = r'.\source_texts\vocab_words.txt'

def vocab_exercise_auto(document):
    print("\n" + "-"*30 + "Vocab Exercise" + "-"*30)
    f = open(vocab_ex_words_dir, 'r', encoding='utf-8')
    wordlist = []
    for word in f.readlines():
        wordlist.append(word.strip())
    print("Words loaded from ", vocab_ex_words_dir)
    print("The wordlist:")
    for word in wordlist:
        print(word)
    oxford_tf = input("Do you want to get example sentences from Oxford dictionary API?(y/n)")
    if oxford_tf == 'y':
        oxford = True
    elif oxford_tf == 'n':
        oxford = False
    yourdict_tf = input("Do you want to get example sentences from yourdict?(y/n)")
    if yourdict_tf == 'y':
        yourdict = True
        number = int(input("How many sentences from yourdict do you want to scrape?"))
    elif yourdict_tf == 'n':
        yourdict = False
        number = 10
    
    print("Scraping sentences...")
    sentences_dict = get_sentences_dict(wordlist, oxford=oxford, yourdict=yourdict, number=number)
    random.shuffle(wordlist)
    chosen_sentences = []
    final_strings = []
    for word in wordlist:
        print("word:", word)
        print("Which sentence do you find the best?")
        for idx,sent in enumerate(sentences_dict[word]):
            print(str(idx+1)+'.', sent)
        num = int(input("Enter the sentence number: "))
        chosen_sentences.append((word, sentences_dict[word][num-1]))
    for comb in chosen_sentences:
        final_strings.append(replace_word_with_underscore(comb[1],comb[0]))
    add_section_title(document, "Fill in the blanks with suitable words.")
    for string in final_strings:
        add_regular_text(document, string)
    add_line_break(document)
        
def replace_word_with_underscore(sentence, word):
    underscore = '_'*16
    nlp=spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    idx_list = []
    for token in doc:
        if str(token.lemma_).lower() == word.lower():
            idx_list.append(token.i)
    doc_list = [str(token) for token in doc]
    for idx in idx_list:
        doc_list[idx] = underscore
    new_sent = untokenize(doc_list)
    return new_sent
    
# Get a dictionary of example sentences from a wordlist, for example:
# wordlist = ['eye', 'hand', 'leg']
# sentences_dict = {'eye':[...], 'hand':[...], 'leg':[...]}
def get_sentences_dict(wordlist, oxford=True, yourdict=True, number=10, lang='en'):
    sentences_dict = dict()
    for word in wordlist:
        print("Scraping the word", word, "...")
        sentences_dict[word] = get_word_sentences(word, oxford=oxford, yourdict=yourdict,
                                                  number=number, lang=lang)
    return sentences_dict

def get_word_sentences(word_id, oxford=True, yourdict=True, number=10, lang='en'):
    app_id, app_key = get_oxford_apikey()
    if oxford:
        oxford_sentences = oxford_example_list(word_id, app_id, app_key, lang=lang)
    else:
        oxford_sentences = []
    if yourdict:
        yourdict_sentences = yourdict_example_list(word_id, number=number)
    else:
        yourdict_sentences = []
    sentences = oxford_sentences + yourdict_sentences
    sentences_remove_none = []
    for sentence in sentences:
        if sentence:
            sentences_remove_none.append(sentence)
    return sentences_remove_none

def get_oxford_apikey():
    oxford_apikey_dir = r".\apikey\oxford_apikey.txt"
    f = open(oxford_apikey_dir, 'r')
    id_and_key = []
    for line in f.readlines():
        id_and_key.append(line.strip())
    return id_and_key[0],id_and_key[1]
   
def yourdict_example_list(word, number=10):
    base_url = 'https://sentence.yourdictionary.com/'

    url = base_url + word
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    script = soup.find('script')
    script_text = str(script)
    sentences = []
    str1=',audio'.join('sentences:'.join(script_text.split('sentences:')[1:]).split(',audio:')[:-1])
    for i in str1[2:].split('},{'):
        sentences.append("\"".join(i.split("\"")[1:-1]))
        
    if number:
        return sentences[:number]
    else:
        return sentences

def oxford_dict_json(word_id, app_id, app_key, lang = 'en'):
    endpoint = "entries"
    language_code = lang
    url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + word_id.lower()
    r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
    json_string = json.dumps(r.json())
    return json_string

def get_examples(json_string):
    word_json = json.loads(json_string)
    try:
        dict_ = word_json['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]
    except:
        return None
    try:
        examples2 = [subsense_dict['examples'][0]['text'] for subsense_dict in dict_['subsenses']]
        examples = [dict_['examples'][0]['text']] + examples2
    except:
        try:
            examples = [dict_['examples'][0]['text']]
        except:
            return None
    return examples

def truecase(sentence):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    tagged_sent = [(w.text, w.tag_) for w in doc]
    normalized_sent = [w.capitalize() if t in ["NNP"] else w for (w,t) in tagged_sent]
    normalized_sent[0] = normalized_sent[0].capitalize()
    string = re.sub(" (?=[\.,'!?:;])", "", ' '.join(normalized_sent))
    return string

def oxford_example_list(word_id, app_id, app_key, lang = 'en'):
    json_string = oxford_dict_json(word_id, app_id, app_key, lang = lang)
    examples_lowercase = get_examples(json_string)
    if examples_lowercase:
        examples = [truecase(example)+'.' for example in examples_lowercase]
    else:
        examples = ['']
    return examples

def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
         "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()