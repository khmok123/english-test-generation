# English test generation

I worked on this project during being a tutor in a tutorial center. This project serves to automatically generate English tests for school pupils containing tense exercises, vocabulary exercises, preposition exercises, adjective exercises and reading comprehension. The code can be run simply by executing `./src/main.py` and following the instructions. The `.docx` document is generated as `./src/template/output.docx`. The texts used for grammar exercises are saved in the directory `./src/source_texts`.

The code does not work for vocabulary exercise currently, since webscraping using BeautifulSoup on the website yourdictionary.com is involved and the HTML structure of the website has changed. The reading comprehension part is still incomplete for now.

The Jupyter notebooks are not needed for the code to work. They are there simply for the testing of the codes. 
