from autogen_agentchat.agents import CodeExecutorAgent
from config.docker_util import get_docker_executor
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

def get_code_executor_agent(code_executor):

    code_executor_agent = CodeExecutorAgent(
        name="Python_Code_Executor",
        code_executor=code_executor,
        description="Python code executor agent that runs code in a Docker container."
    )
    
    return code_executor_agent