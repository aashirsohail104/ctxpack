from src.agent import Agent

def test_agent_run():
    a = Agent("test")
    assert a.run("task") == "test running task"
