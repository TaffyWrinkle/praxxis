"""
This file is responsible for running all of the functions identified by app.py
"""

import os

## database roots for mtool. Should be changed to remove hard coding
_root = os.path.join(os.getenv('APPDATA'), "mtool")
_library_root = os.path.join(_root, "library")
_library_db = os.path.join(_library_root, "libraries.db")
_scene_root = os.path.join(_root, "scene")
_outfile_root = os.path.join(_root, "output")
_history_db = os.path.join(_scene_root, "current_scene.db")
_azure_data_studio_location = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'Azure Data Studio', 'azuredatastudio')

_query_start = 0
_query_end = 100


def get_current_scene_db():
    """calls the function to get the location of the history db"""
    from src.mtool.util import sqlite_util
    scene = sqlite_util.get_current_scene(_history_db)
    return os.path.join(_scene_root, scene, f"{scene}.db")


def run_notebook(arg):
    """calls the function to run a notebook"""
    from src.mtool.notebook import run_notebook
    current_scene_db = get_current_scene_db()
    run_notebook.run_notebook(arg, _root, _outfile_root, current_scene_db, _library_root, _library_db)
    return
 

def open_notebook(arg):
    """calls the function to open a notebook"""
    from src.mtool.notebook import open_notebook
    open_notebook.open_notebook(arg, get_current_scene_db(), _library_db, _azure_data_studio_location)
    return
 

def search_notebook(arg):
    """calls the function to search a notebook"""
    from src.mtool.notebook import search_notebook
    search_notebook.search_notebook(arg, _library_db, _query_start, _query_end)
    return


def list_notebook(arg):
    """calls the function to list notebooks"""
    from src.mtool.notebook import list_notebook
    current_scene_db = get_current_scene_db()
    list_notebook.list_notebook(_scene_root, _library_db, _history_db, current_scene_db, _query_start, _query_end)
    return


def next_notebook(arg):
    """calls the function to get the next notebook"""
    ##TODO  implement this
    return "coming soon"


def history(arg):
    """calls the function to display scene history"""
    from src.mtool.scene import history
    current_scene_db = get_current_scene_db()
    history.history(arg, _history_db, current_scene_db)
    return


def new_scene(arg):
    """calls the function to create a new scene"""
    from src.mtool.scene import new_scene
    new_scene.new_scene(arg, _scene_root, _history_db)
    return
 

def end_scene(arg):
    """calls the function to end a scene"""
    from src.mtool.scene import end_scene
    current_scene = get_current_scene_db()
    end_scene.end_scene(arg, _scene_root, _history_db, current_scene)
    return
 

def change_scene(arg):
    """calls the function to change the current scene"""
    from src.mtool.scene import change_scene
    change_scene.change_scene(arg, _scene_root, _history_db)
    return
 

def resume_scene(arg):
    """calls the function to resume an ended scene"""
    from src.mtool.scene import resume_scene
    resume_scene.resume_scene(arg, _scene_root, _history_db)
    return
 

def delete_scene(arg):
    """ calls the function to delete a scene"""
    from src.mtool.scene import delete_scene
    delete_scene.delete_scene(arg, _scene_root, _history_db)
    return


def list_scene(arg):
    """calls the function to list scenes"""
    from src.mtool.scene import list_scene
    list_scene.list_scene(_scene_root, _history_db)
    return


def set_env(arg):
    """calls the function to set an environment"""
    from src.mtool.environment import set_env
    current_scene = get_current_scene_db()
    set_env.set_env(arg, _scene_root, _history_db, current_scene)
    return


def delete_env(arg):
    """calls the function to delete an environment"""
    from src.mtool.environment import delete_env
    current_scene = get_current_scene_db()
    delete_env.delete_env(arg, _scene_root, _history_db, current_scene)
    return


def list_env(arg):
    """calls the function to list environments in current scene"""
    from src.mtool.environment import list_env       
    list_env.list_env(arg, _scene_root, _history_db, _query_start, _query_end)
    return


def add_library(arg):
    """calls the function to add a library"""
    ##TODO: implement this
    return "coming soon"


def list_library(arg):
    """calls the function to list loaded libraries"""
    from src.mtool.library import list_library
    current_scene_db = get_current_scene_db()
    list_library.list_library(_library_root, _library_db, current_scene_db)
    return


def load_library(arg):
    """calls the function to load libraries"""
    from src.mtool.library import load_library
    load_library.load_libraries(_library_root, _library_db)
    return


def default(arg):
    """calls the default function, which is to display the current scene."""
    ##TODO:set up running notebook as default 
    from src.mtool.scene import current_scene
    current_scene.current_scene(_scene_root, _history_db)
    return
 
 
def command(argument):
    """uses a dictionary as a switch statement to determine which funciton to run."""

    ##Creates the appdata mtool folder if it doesn't exist
    if not os.path.exists(_root):
        os.mkdir(_root)

    switcher = {
        "run_notebook": run_notebook,
        "open_notebook": open_notebook,
        "search_notebooks": search_notebook,
        "list_notebooks": list_notebook,
        "history": history,
        "next_notebook": next_notebook,
        "new_scene": new_scene,
        "end_scene": end_scene,
        "change_scene": change_scene,
        "resume_scene": resume_scene,
        "delete_scene": delete_scene,
        "list_scene": list_scene,
        "add_library": add_library,
        "list_library": list_library,
        "set_env": set_env,
        "delete_env": delete_env,
        "list_env": list_env,
        "load_library": load_library
    }
    if hasattr(argument, "which"):
        func = switcher.get(argument.which)
    else:
        func=default
    
    return func(argument)
    