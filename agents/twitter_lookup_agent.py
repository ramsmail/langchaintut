from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """given the fullname  {name_of_person} I want you to get me a link to their Twitter profile page. 
    Your final answer should only contain the person's username"""

    tools_for_agent = [
        Tool(
            name="crawl Google for twitter profile page",
            func=get_profile_url,
            description="useful for when you need to get the Twitter Page URL",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    twitter_username = agent.run(prompt_template.format_prompt(name_of_person=name))
    return twitter_username
