class Agent:
    def __init__(self, name):
        self.name = name

    def run(self, task):
        return f"{self.name} running {task}"
