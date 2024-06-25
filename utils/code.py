import nbformat
from nbformat.v4 import new_code_cell

import os


def code_to_notebook(code):
    file_path = "generated_code.ipynb"
    
    if os.path.exists(file_path):
        nb = nbformat.read(file_path, as_version=4)
    else:
        nb = nbformat.v4.new_notebook()
    
    new_cell = new_code_cell(source=code)

    last_cell = nb.cells[-1].source
    if last_cell == code:
        pass
    else:
        nb.cells.append(new_cell)

    print(nb.cells[-1].source)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        nbformat.write(nb, file)


