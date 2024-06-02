import mkdocs_gen_files
import time
import datetime
import os
# import mammoth
import markdownify
# with mkdocs_gen_files.open("index.md", "r+") as f:
#     data = f.read()
#     f.seek(0)
#     f.write(data)
from mrkdwn_analysis import MarkdownAnalyzer


# from __future__ import print_function
from googleapiclient.discovery import build

from oauth2client.service_account import ServiceAccountCredentials
import re
import requests
from collections import defaultdict, Counter

class DavidMarkdownAnalyzer: ### AHAHAH NEPOTISM AHHAHAH (its too late at night for this)
    def __init__(self, file_path, encoding='utf-8'):
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                self.lines = file.readlines()
        except FileNotFoundError:
            os.remove("./last_updated.txt")
            ## restart this current script
            os.system("python gen_pages.py")
            os._exit(0)
            
    def identify_headers(self):
        result = defaultdict(list)
        pattern = r'^(#{1,6})\s(.*)'
        pattern_image = r'!\[.*?\]\((.*?)\)'  # pattern to identify images
        for i, line in enumerate(self.lines):
            line_without_images = re.sub(pattern_image, '', line)  # remove images from the line
            match = re.match(pattern, line_without_images)
            if match:
                cleaned_line = re.sub(r'^#+', '', line_without_images).strip()
                result["Header"].append(cleaned_line)
        return dict(result)  # Convert defaultdict to dict before returning

    def identify_sections(self):
        result = defaultdict(list)
        pattern = r'^.*\n[=-]{2,}$'
        for i, line in enumerate(self.lines):
            if i < len(self.lines) - 1:
                match = re.match(pattern, line + self.lines[i+1])
            else:
                match = None
            if match:
                if self.lines[i+1].strip().startswith("===") or self.lines[i+1].strip().startswith("---"):
                    result["Section"].append((line.strip(), i))
        return dict(result)  # Convert defaultdict to dict before returning
    
    def identify_paragraphs(lines):
        result = defaultdict(list)
        pattern = r'^(?!#)(?!\n)(?!>)(?!-)(?!=)(.*\S)'
        pattern_underline = r'^.*\n[=-]{2,}$'
        in_code_block = False
        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            if in_code_block:
                continue
            if i < len(lines) - 1:
                match_underline = re.match(pattern_underline, line + lines[i+1])
                if match_underline:
                    continue
            match = re.match(pattern, line)
            if match and line.strip() != '```':  # added a condition to skip lines that are just ```
                result["Paragraph"].append(line.strip())
        return dict(result)

    def identify_blockquotes(lines):
        result = defaultdict(list)
        pattern = r'^(>{1,})\s(.*)'
        blockquote = None
        in_code_block = False
        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block  # Flip the flag
            if in_code_block:
                continue  # Skip processing for code blocks
            match = re.match(pattern, line)
            if match:
                depth = len(match.group(1))  # depth is determined by the number of '>' characters
                text = match.group(2).strip()
                if depth > 2:
                    raise ValueError(f"Encountered a blockquote of depth {depth} at line {i+1}, but the maximum allowed depth is 2")
                if blockquote is None:
                    # Start of a new blockquote
                    blockquote = text
                else:
                    # Continuation of the current blockquote, regardless of depth
                    blockquote += " " + text
            elif blockquote is not None:
                # End of the current blockquote
                result["Blockquote"].append(blockquote)
                blockquote = None

        if blockquote is not None:
            # End of the last blockquote
            result["Blockquote"].append(blockquote)

        return dict(result)

    def identify_code_blocks(lines):
        result = defaultdict(list)
        pattern = r'^```'
        in_code_block = False
        code_block = None
        for i, line in enumerate(lines):
            match = re.match(pattern, line.strip())
            if match:
                if in_code_block:
                    # End of code block
                    in_code_block = False
                    code_block += "\n" + line.strip()  # Add the line to the code block before ending it
                    result["Code block"].append(code_block)
                    code_block = None
                else:
                    # Start of code block
                    in_code_block = True
                    code_block = line.strip()
            elif in_code_block:
                code_block += "\n" + line.strip()

        if code_block is not None:
            result["Code block"].append(code_block)
        
        return dict(result)

    def identify_ordered_lists(lines):
        result = defaultdict(list)
        pattern = r'^\s*\d+\.\s'
        in_list = False
        list_items = []
        for i, line in enumerate(lines):
            match = re.match(pattern, line)
            if match:
                if not in_list:
                    # Start of a new list
                    in_list = True
                # Add the current line to the current list
                list_items.append(line.strip())
            elif in_list:
                # End of the current list
                in_list = False
                result["Ordered list"].append(list_items)
                list_items = []

        if list_items:
            # End of the last list
            result["Ordered list"].append(list_items)

        return dict(result)

    def identify_unordered_lists(lines):
        result = defaultdict(list)
        pattern = r'^\s*((\d+\\\.|[-*+])\s)'
        in_list = False
        list_items = []
        for i, line in enumerate(lines):
            match = re.match(pattern, line)
            if match:
                if not in_list:
                    # Start of a new list
                    in_list = True
                # Add the current line to the current list
                list_items.append(line.strip())
            elif in_list:
                # End of the current list
                in_list = False
                result["Unordered list"].append(list_items)
                list_items = []

        if list_items:
            # End of the last list
            result["Unordered list"].append(list_items)

        return dict(result)
    
    def identify_tables(self):
        result = defaultdict(list)
        table_pattern = re.compile(r'^\|.*\|$', re.MULTILINE)
        table_rows = table_pattern.findall("".join(self.lines))
        for table_row in table_rows:
            result["Table"].append(table_row.strip().split("|"))
        return dict(result)
    
    def identify_links(self):
        result = defaultdict(list)
        text_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        image_link_pattern = r'!\[([^\]]*)\]\((.*?)\)'
        for i, line in enumerate(self.lines):
            text_links = re.findall(text_link_pattern, line)
            image_links = re.findall(image_link_pattern, line)
            for link in text_links:
                result["Text link"].append({"line": i+1, "text": link[0], "url": link[1]})
            for link in image_links:
                result["Image link"].append({"line": i+1, "alt_text": link[0], "url": link[1]})
        return dict(result)
    
    def check_links(self):
        broken_links = []
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for i, line in enumerate(self.lines):
            links = re.findall(link_pattern, line)
            for link in links:
                try:
                    response = requests.head(link[1], timeout=3)
                    if response.status_code != 200:
                        broken_links.append({'line': i+1, 'text': link[0], 'url': link[1]})
                except (requests.ConnectionError, requests.Timeout):
                    broken_links.append({'line': i+1, 'text': link[0], 'url': link[1]})
        return broken_links

    def identify_todos(self):
        todos = []
        todo_pattern = r'^\-\s\[ \]\s(.*)'
        for i, line in enumerate(self.lines):
            match = re.match(todo_pattern, line)
            if match:
                todos.append({'line': i+1, 'text': match.group(1)})
        return todos
    
    def count_elements(self, element_type):
        identify_func = getattr(self, f'identify_{element_type}', None)
        if not identify_func:
            raise ValueError(f"No method to identify {element_type} found.")
        elements = identify_func()
        return len(elements.get(element_type.capitalize(), []))

    def count_words(self):
        text = " ".join(self.lines)
        words = text.split()
        return len(words)

    def count_characters(self):
        text = " ".join(self.lines)
        # Exclude white spaces
        characters = [char for char in text if not char.isspace()]
        return len(characters)
    
    def get_text_statistics(self):
        statistics = []
        for i, line in enumerate(self.lines):
            words = line.split()
            if words:
                statistics.append({
                    'line': i+1,
                    'word_count': len(words),
                    'char_count': sum(len(word) for word in words),
                    'average_word_length': sum(len(word) for word in words) / len(words),
                })
        return statistics
    
    def get_word_frequency(self):
        word_frequency = Counter()
        for line in self.lines:
            word_frequency.update(line.lower().split())
        return dict(word_frequency.most_common())
    
    def search(self, search_string):
        result = []
        for i, line in enumerate(self.lines):
            if search_string in line:
                element_types = [func for func in dir(self) if func.startswith('identify_')]
                found_in_element = None
                for etype in element_types:
                    element = getattr(self, etype)()
                    for e, content in element.items():
                        if any(search_string in c for c in content):
                            found_in_element = e
                            break
                    if found_in_element:
                        break
                result.append({"line": i+1, "text": line.strip(), "element": found_in_element})
        return result
    
    def analyse(self):
        analysis = {
            'headers': self.count_elements('headers'),
            'sections': self.count_elements('sections'),
            'paragraphs': self.count_elements('paragraphs'),
            'blockquotes': self.count_elements('blockquotes'),
            'code_blocks': self.count_elements('code_blocks'),
            'ordered_lists': self.count_elements('ordered_lists'),
            'unordered_lists': self.count_elements('unordered_lists'),
            'tables': self.count_elements('tables'),
            'words': self.count_words(),
            'characters': self.count_characters(),
        }
        return analysis

scope = ['https://www.googleapis.com/auth/drive.readonly']
## get last time updated

def get_files():
    credentials = ServiceAccountCredentials.from_json_keyfile_name('roboloco-key.json', scope)

    # https://developers.google.com/drive/api/v3/quickstart/python
    service = build('drive', 'v3', credentials=credentials)
    def to_safe_string(s):
        ## " < > # % { } | \ ^ ~ [ ] ` are all the unsafe ones
        return s.replace(" ", " ").replace(":", "-").replace('"', "_").replace("<", "_").replace(">", "_").replace("#", "_").replace("%", "_").replace("{", "_").replace("}", "_").replace("|", "_").replace("\\", "_").replace("^", "_").replace("~", "_").replace("[", "_").replace("]", "_").replace("`", "_")
    # Call the Drive v3 API
    results = service.files().list(
        fields="*",supportsAllDrives = True, includeItemsFromAllDrives = True,pageSize=650).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            # print(u'{0} ({1}) - {2}'.format(item['name'], item['id'], item['parents']))
            # print(item['name'])
            original_item = item
            if (item['mimeType'] != 'application/vnd.google-apps.folder'):
                name = item['name']
                pastParentPath = ""
                parentPath = ""
                moreParents = True
                while moreParents:
                    if 'parents' in item:
                        parent = item['parents'][0]
                        item = service.files().get(fileId=parent, fields="*").execute()
                        pastParentPath = parentPath
                        parentPath = "/" + item["name"] + parentPath
                        ## query item's name, using `item`, which is an id
                    
                    else:
                        moreParents = False
                        parentPath = pastParentPath

                path = to_safe_string(parentPath + "/" + name)[1:].strip() +".md"
                print(path)
                if original_item['mimeType'] != 'application/vnd.google-apps.document':
                    continue
                with mkdocs_gen_files.open(path, "w", encoding="utf-8") as f:
                    ## get contents of google doc which is assumed to be file, keep in mind that gdocs are not exportable
                    ## check if file is gdoc
                    # print(original_item['mimeType'])
                    ## check if file is a not a slide
                    
                    
                        ##export as html to preserve images
                        media = service.files().export(fileId=original_item['id'], mimeType='text/html').execute()
                        # print("media done")
                        path = "./docs/" + path
                        markdown = markdownify.markdownify(media)
                        os.makedirs(os.path.dirname(path), exist_ok=True)
                        with open(path, "w", encoding="utf-8") as f2:
                            f2.write(markdown)
                
                        if markdown == "":
                            continue
                
                        # print(media)
                        ## convert docx to markdown
                        # res = mammoth.convert_to_markdown(media, media_file = f)
                        # print(markdown)

                        f.write("# " + original_item['name'] +"\n" + markdown)
                

if not os.path.exists("./last_updated.txt"):
    get_files()
else:
    with open("./last_updated.txt", "r") as f:
        last_updated = f.read()
        print(last_updated)
        ## if last time updated is less than 24 hours ago, don't update
        if time.time() - float(last_updated) > 86400:
            get_files()


with open("./last_updated.txt", "w") as f:
    f.write(str(time.time()))


def get_section_from_file(filepath, section):
    anal = DavidMarkdownAnalyzer(filepath)
    data = anal.identify_sections()['Section']
    print("section: ", section)
    needed_section = None
    nextSection = None
    res = None
    for i, key in enumerate(data):
        print(key)
        if key[0] == section:
            needed_section = key
            if i+1 < len(data):
                nextSection = data[i+1]

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.readlines()
    if needed_section == None:
        try:
            print("trying to eval")
            print(f"data[{section.strip()}]")
            ## interpret section as a slice of the headers, aka try doing data[section]
            res = eval(f"data[{section.strip()}]", globals(), locals())
            print("res", res)
            if res == None:
                return None, None
            ## check if res is a list
            if type(res) == list:  
                needed_section = (None, res[0][1])
                # print(needed_section)
                nextSection = (None, res[-1][1])
                # print(nextSection)
                if nextSection[1] == needed_section[1]:
                    nextSection = None
                # print(needed_section)
            else:
                needed_section = (None, data.index(res))
                nextSection = (None, data.index(res)+1)
                if nextSection[1] == len(data):
                    nextSection = None

            print("finished eval")


        except Exception as e:
            print(e)
            return None, None
        # return "Section not found"
    stringExcerpt = ""
    if nextSection == None:
        stringExcerpt = "\n".join(text[needed_section[1]:])
    else:
        stringExcerpt = "\n".join(text[needed_section[1]:nextSection[1]])
    stringExcerpt = stringExcerpt.replace(section, "",1)
    
    stringExcerpt = stringExcerpt.split("\n", 1)[1]
  
    # print(stringExcerpt)
    if res == None:
        return (stringExcerpt, None)
    return (stringExcerpt, res[0])

'''
checks if string is the format <<python code>>, and if it is, run the python code inside the double angle brackets and return the output

'''
def checkIfDynamicPython(string):
    if string.startswith("<<") and string.endswith(">>"):
        string = string.replace("<<", "")
        string = string.replace(">>", "")
        return eval(string, globals())
    return string

vars = {}

needsParsing = True
changes = 0
while needsParsing:
    python_exp = r"(?P<var>\(.+\))?<<.*?>>"
    rel_exp = r"(?P<var>\(.+\))?<.*?>"
    ##sub for all ${} in the string, js style
    sub_exp = r"\${.*?}"
    files = os.listdir("./docs")
    for file in files:
        print("doing file", file)
        if file == "index.md" or file == "404.md":
            continue
        exp = r"!\[.*\]\[.*\]"
        ## check if file is a markdown file
        if not file.endswith(".md"):
            continue
        print("about to open")
        with mkdocs_gen_files.open(f"{file}", "r+", encoding="utf-8") as f:
            data = f.read()
            for _ in range(4):
                ## match the expression to the data, find all matches, and extract the strings inbetween both brackets
                ## then, get the section from the file
                ## match <<python code>> a
                print("opened")
                python_exp = r"(?P<var>\(.+\))?<<.*?>>"
                rel_exp = r"(?P<var>\(.+\))?<.*?>"
                ##sub for all ${} in the string, js style
                sub_exp = r"\${.*?}"
                # print(re.findall(python_exp, data))
                for match in re.finditer(python_exp, data):
                    # print("found python matches")
                    ## get match's named caputirng group called "var", if it has one
                    # changes += 1
                    match = match.group()
                    print("match: ", match)
                    if match == "":
                        continue
                    dyn = checkIfDynamicPython(match)
                    first_capturing_group = re.search(python_exp, match).groupdict()['var']
                    
                    ## get rid of parentheses in first capturing group
                    if first_capturing_group != None:
                        first_capturing_group = first_capturing_group.replace("(", "",1).replace(")", "",1)
                        ## store dyn in vars
                        vars[first_capturing_group] = dyn
                    print("dyn: ",dyn)
                    data = data.replace(match, dyn)
                print(vars)
            
                print("got past dynamic")
                for match in re.findall(exp, data):
                    # changes += 1
                    print(match)
                    orgstring = match
                    firstMatch = match.split("[")[1].split("]")[0]+'.md'
                    firstMatch = "/" + firstMatch.replace(".md.md", ".md")
                    firstMatch = firstMatch.replace("//", "/")
                    secondMatch = match.split("[")[2].split("]")[0]
            
                    ## extract the string inbetween the brackets

                    ## get the section from the file
                    var = None
                    newMatch = re.search(rel_exp, match)
                    ## get match's named caputirng group called "var", if it has one
                    print(newMatch)

                    if not (newMatch == "" or newMatch == None):
                        ## get rid of first capturing group, if it exists
                        noVarMatch = newMatch.group()
                        if newMatch.groupdict()['var'] != None:
                            # var = match[newMatch.groupdict():newMatch.end("var")]
                            var = newMatch.groupdict()['var']
                            ## store the section in the vars dictionary
                            noVarMatch = newMatch.group().replace(var, "",1)
                            var = var.replace("(", "",1).replace(")", "",1)
                        secondMatch = noVarMatch.replace("<", "",1).replace(">", "",1)

                
                    print("getting section")
                    (section, evalOutput) = get_section_from_file("./docs" + firstMatch, secondMatch)
                    vars[var] = evalOutput
                    print(vars)
                    ## replace the image with the section
                    # print(section)
                    if _ == 3:
                        print("REPLACING")
                        data = data.replace(match, "This data could not be pulled. This probably means that someone forgot to do their documentation or something.")
                    if section == None:
                        continue
                    data = data.replace(match, section)
                print(vars)
                for match in re.findall(sub_exp, data):
                    
                    ## get the match without the ${}
                    newMatch = match.replace("${", "").replace("}", "")
                    ## get the value of the variable in the vars dictionary
                    data = data.replace(match, vars[newMatch])

                print("DONE WITH " + file + "=====================") 
            f.seek(0)
                # f.write(data)
            f.write(data)  
        
    needsParsing = False
                