import nbformat
from nbformat.v4 import new_code_cell

class CodeGeneration:

    @staticmethod
    def generate_code(code):
        if code is None:
            return

        # Define the file path for the notebook
        file_path = "generated_code.ipynb"
        
        try:
            # Try to open and read the existing notebook
            with open(file_path, 'r', encoding='utf-8') as file:
                nb = nbformat.read(file, as_version=4)
        except FileNotFoundError:
            # If the notebook does not exist, create a new one
            nb = nbformat.v4.new_notebook()
            nb.metadata = {
                "language_info": {
                    "name": "python"
                }
            }

        # Check if the last cell contains the same code
        if nb.cells and nb.cells[-1].cell_type == 'code' and nb.cells[-1].source == code:
            print("The last cell already contains the same code. No new cell appended.")
        else:
            # Create a new code cell
            new_cell = new_code_cell(source=code)
            
            # Append the new code cell to the notebook
            nb.cells.append(new_cell)
            
            # Write the updated notebook back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                nbformat.write(nb, file)
            
            print(f"Code appended to {file_path}")


