""" This module provide the to-do model-controller """
# cli_to_do/cli_to_do.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from cli_to_do import DB_READ_ERROR, ID_ERROR
from cli_to_do.database import DatabaseHandler

class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int

class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return the current to-do list."""
        read = self._db_handler.read_todos()
        return read.todo_list


    def add(self, description: List[str], priority: int = 2) -> CurrentTodo:
        description_test = " ".join(description)
        todo = {
            "Description": description_test,
            "Priority": priority,
            "Done": False,
        }
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(Todo, read.error)
        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove(self, todo_id: int) -> CurrentTodo:
        """Remove a to-do from the database using its id or index."""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list.pop(todo_id - 1)
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def set_done(self, todo_id: int) -> CurrentTodo:
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}. read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except indexError:
            return CurrentTodo({}, ID_ERROR)
        todo["Done"] = True
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)