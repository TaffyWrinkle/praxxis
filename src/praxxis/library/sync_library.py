"""
    This file loads libraries into the library database file
"""

import os

def sync_library(library_root, library_db, custom_path = False, library_name = None, remote = None, remote_origin = None):
    from src.praxxis.sqlite import sqlite_library
    from src.praxxis.util import error
    from src.praxxis.display import display_error
    from src.praxxis.notebook import notebook
    from src.praxxis.display import display_library
    from src.praxxis.sqlite import sqlite_parameter
    from src.praxxis.util import get_raw_git_url
    import os
    import re

    for root, dirs, files in os.walk(library_root):
        current_library = ""
        for name in files:
            if custom_path:
                relative_path = [library_root.split(os.path.sep)[-1]]
            else:
                relative_path = root.split(os.path.sep)[len(library_root.split(os.path.sep)):]
            
            if library_name == None:
                library_name = "_".join(relative_path)

            if relative_path == []:
                continue

            if not library_name == current_library:
                print(library_name)
                print(current_library)
                display_library.display_loaded_library(root, True)
                display_library.loaded_notebook_message()
                current_library = library_name

            readme_location = os.path.join(root, "README.md")
            readme_data = None

            if os.path.isfile(readme_location):
                f = open(readme_location, "r")
                readme_data = "  ".join(f.readlines()[:3])

            counter = 0
            try:
                library_list = sqlite_library.get_library_by_name(library_db, library_name)
                orig_name = library_name
                if not len(library_list) == 0:
                    library_metadata = sqlite_library.get_library_by_root(library_db, root)
                    if library_metadata == []:
                        while sqlite_library.check_library_exists(library_db, library_name):
                            counter += 1
                            library_name = f"{orig_name}-{counter}"
                    if library_metadata[0][0] == root:
                        library_name = library_metadata[0][2]
                    else:
                        raise error.LibraryNotFoundError
            except error.LibraryNotFoundError:
                pass

            file_name, file_extension = os.path.splitext(name)
            if(file_extension == ".ipynb"):
                file_root = os.path.join(root, name)
                        
                sqlite_library.sync_library(library_db, root, readme_data, library_name, remote)

                notebook_data = notebook.Notebook([file_root, file_name, library_name])
                #create a notebook object out of the file data
                for parameter in notebook_data._parameters:
                    #load the parameters out of the notebook object and into the db
                    sqlite_parameter.set_notebook_parameters(library_db, file_name, parameter[0].strip(), parameter[1], library_name)
                display_library.display_loaded_notebook(name)

                library_url = ("/").join(relative_path)
                raw_url = get_raw_git_url.get_raw_url_for_file(remote_origin, name, f"/{library_url}/")
                sqlite_library.load_notebook(library_db, file_root, file_name, library_name, raw_url)
