from typing import TypeVar, Generic

T = TypeVar('T')

class Task(Generic[T]):
    def __init__(self, name: str, desc: str, points: int):
        self.name: str = name
        self.desc: str = desc
        self.points: int = points

    def submit(self, value: T) -> bool:
        return False

class AnswerTask(Task[str]):
    def __init__(self, name: str, desc: str, points: int, correct_answer: str):
        super().__init__(name, desc, points)
        self.correct_answer = correct_answer

    def submit(self, value: str) -> bool:
        return value == self.correct_answer


# TODO: Dokończenie i rozszerzenie modułów

class Module:
    def __init__(self, name: str, desc: str,  tasks: list[Task]):
        self.name = name
        self.desc = desc
        self.tasks: list[Task] = tasks
        self.total_points = 0
        for task in tasks:
            self.total_points += task.points






