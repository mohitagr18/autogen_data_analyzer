from autogen_agentchat.agents import AssistantAgent
from agents.prompts.data_analyzer_message import DATA_ANALYZER_SYSTEM_MESSAGE

def get_data_analyzer_agent(model_client):

    data_analyzer_agent = AssistantAgent(
        name="Data_Analyzer",
        model_client=model_client,
        system_message=DATA_ANALYZER_SYSTEM_MESSAGE,
        description="Data analysis agent that processes and analyzes data."
    )
    
    return data_analyzer_agent