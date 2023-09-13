from typing import Tuple

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parser import person_intel_parser, PersonIntel
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweet
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent


def ice_break(name: str) -> Tuple[PersonIntel, str]:
    # Get the URL using the lookup agent in agents
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    # Scrape the URL using the scrape_linkedin_profile function from linkedin.py under third_parties

    # Hardcoded an URL here because need to pay money for SERPAPI or Linkedin not sure which
    # linkedin_data = scrape_linkedin_profile(
    #     linkedin_profile_url="https://gist.githubusercontent.com/emarco177"
    #     "/0d6a3f93dd06634d95e46a2782ed7490/raw"
    #     "/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden"
    #     "-marco.json"
    # )
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    print(linkedin_data)
    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweet(username=twitter_username, num_tweets=100)
    summary_template = """
       Given the LinkedIn information {linkedin_information} and twitter {twitter_information} about a person, please provide the following
       1) A brief summary of the person
       2) Two interesting facts about them
       3) A topic that may interest them
       4) 2 creative Ice breakers to open a conversation with them.
       \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    # Feed the chain with linkedin and twitter data for the model to extract information from.
    result = chain.run(linkedin_information=linkedin_data, twitter_information=tweets)
    print(result)
    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Hello LangChain!")
    #ice_break(name="Ramesh Venkatraman")
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile


if __name__ == "__main__":
    print("Hello LangChain!")

    linkedin_profile_url = linkedin_lookup_agent(name="Ramesh Venkatraman HCL")

    summary_template = """
         given the Linkedin information {information} about a person from I want you to create:
         1. a short summary
         2. two interesting facts about them
     """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    print(chain.run(information=linkedin_data))