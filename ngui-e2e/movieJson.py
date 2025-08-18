import asyncio

from langchain_openai import ChatOpenAI
from next_gen_ui_langgraph.agent import NextGenUILangGraphAgent
from langgraph.prebuilt import create_react_agent
from langchain_mistralai import ChatMistralAI
from next_gen_ui_langgraph.readme_example import search_movie, movies_agent, ngui_cfg, ngui_agent

ngui_agent

llm = ChatOpenAI(model="granite3-dense:8b", base_url="http://localhost:11434/v1")

def search_movie(title: str):
    movies_agent = create_react_agent(
        model=llm,
        tools=[search_movie("toy story")],
        prompt="You are useful movies assistant to answer user questions")
    ngui_agent = NextGenUILangGraphAgent(model=llm).build_graph()
    ngui_cfg = {"configurable": {"component_system": "json"}}

def run():

    movie_response = movies_agent.invoke(
        {"messages":[{"role":"user", "content": "hi"}]}
    )
    # print("==movies text answer==", movie_response["messages"][-1].content)
    ngui_response = asyncio.run(
        ngui_agent.ainvoke(movie_response, ngui_cfg)
    )

    # print(ngui_cfg)
    # print(f"===Next Gen UI {ngui_cfg['configurable']['component_system']} Rendition===", ngui_response["renditions"][0].content)

    print(ngui_response["renditions"][0].content)

if __name__ == '__main__':
    run()