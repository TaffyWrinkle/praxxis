"""
This file displays the current scene from the scene history db
"""

def current_scene(scene_root, history_db):
    """calls the scene init, and displays the current scene from the sqlite history db""" 
    from src.mtool.sqlite import sqlite_scene
    from src.mtool.scene import scene
    from src.mtool.display import display_scene

    current_scene = sqlite_scene.get_current_scene(history_db)
    display_scene.display_current_scene(current_scene)
    return current_scene
