from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.code_executor_agent import get_code_executor_agent
from agents.data_analyzer_agent import get_data_analyzer_agent

def get_data_analyzer_team(model_client, code_executor):

    code_executor_agent = get_code_executor_agent(code_executor)

    data_analyzer_agent = get_data_analyzer_agent(model_client)

    text_mention_termination = TextMentionTermination('STOP')

    team = RoundRobinGroupChat(
        participants=[code_executor_agent, data_analyzer_agent],
        termination_condition=text_mention_termination,
        max_turns=20
    )
    
    return team