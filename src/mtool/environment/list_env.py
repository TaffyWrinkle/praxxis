"""
This file lists all of the environment variables
"""

def list_env(args, scene_root, history_db, current_scene_db, start, end):
    """lists the environment variables in scene"""
    import os
    from src.mtool.util.sqlite import sqlite_scene
    from src.mtool.util.sqlite import sqlite_environment
    from src.mtool.display import display_env
    
    env_list = sqlite_environment.list_env(current_scene_db, start, end)

    display_env.display_list_env(env_list)
    return env_list


def list_notebook_env(args, library_db, current_scene_db):
    """List all environments in the current notebook"""
    from src.mtool.util.sqlite import sqlite_environment
    from src.mtool.notebook import notebook
    from src.mtool.display import display_env

    name = args.notebook
    tmp_name = notebook.get_notebook_by_ordinal(current_scene_db, name)
    if tmp_name != None:
        name = tmp_name

    sqlite_environment.get_all_env(current_scene_db)
    
    display_env.display_view_env(sqlite_environment.list_notebook_env(library_db, name), 
                                      sqlite_environment.get_all_env(current_scene_db))


def list_library_env(args, library_db, current_scene_db):
    """Lists all environments in the """
    from src.mtool.util.sqlite import sqlite_environment
    from src.mtool.display import display_env

    name = args.name 
    display_env.display_view_env(sqlite_environment.get_library_environments(library_db, name),
                             sqlite_environment.get_all_env(current_scene_db))
    
