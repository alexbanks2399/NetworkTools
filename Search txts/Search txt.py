from pathlib import Path
import os

directory = os.getcwd()
path = Path(fr'{directory}\Files to search')

search_string = input("String to search for: ")

files_checked = 0
for o in path.rglob('*.txt'):
    files_checked = files_checked + 1
    if o.is_file():
        text = o.read_text()
        if search_string in text:
            print(o)
            # print(text)
            f = open(fr'{directory}\Output.txt', "a")
            f.write(f"{str(o)}\n")
            f.close()
    print(f"Files checked {files_checked}")

print(f"Total files checked {files_checked}")