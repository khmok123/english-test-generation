from doc_func import add_test_title, add_one_line, add_section_title, add_allowed_time, add_regular_text, add_line_break, add_page_break, add_to_cell

def reading_exercise_auto(document):
    add_page_break(document)
    add_section_title(document, "B.  Comprehension (20%)")
    add_section_title(document, "1. Read the article carefully.")
    table1 = document.add_table(rows=1, cols=1)
    table1.style = 'TableGrid'
    add_to_cell(table1, '')
    add_section_title(document, "Answer the questions in complete sentences. (14%)-7@2%")
    for idx in range(7):
        add_regular_text(document, str(idx+1) + '. ')
        add_regular_text(document, '_'*53)
        add_regular_text(document, '_'*53)
    add_section_title(document, "2. Read the article carefully.")
    table2 = document.add_table(rows=1, cols=1)
    table2.style = 'TableGrid'
    add_to_cell(table2, '')
    add_section_title(document, "Give short answers to the following questions? (6%)-6@1%")
    for idx in range(6):
        add_regular_text(document, str(idx+1) + '. ')
        add_regular_text(document, '_'*28)
        
        
        
