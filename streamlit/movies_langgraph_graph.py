from typing import TypedDict, Optional, Literal
import logging

from langgraph.prebuilt import create_react_agent
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from next_gen_ui_langgraph import NextGenUILangGraphAgent
from next_gen_ui_testing import data_set_movies


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


### Movies Agent
@tool(
    "movie_search_by_title",
    response_format="content",
    parse_docstring=True,
    return_direct=True,
)
def movie_search_by_title(title: Optional[str]):
    """Search movies based on title.
    You get all details about a movie including plot, release date, budget, IMDB rating and also poster as URL and what movies the actor played

    Args:
        title: Movie title e.g. 'Toy Story'
    """
    logger.debug("movie_search_by_title, title=%s", title)
    return data_set_movies.find_movie(title)


# @tool(
#     "actor_detail", response_format="content", parse_docstring=True, return_direct=True
# )
# def actors_search_tool(name: str):
#     """Search one actor based on its name.
#     You get all details about actor including biography, birth date, actor's image and list of movies the actor played

#     Args:
#         name: Actor's name e.g. 'Tom Hanks'
#     """
#     return actors_search(name, 10)


def create_assistant_graph(model: ChatOpenAI, ngui_model: ChatOpenAI):
    """
    Create Assistant Graph by using given model and ngui_model
    """

    movies_agent = create_react_agent(model=model, tools=[movie_search_by_title])

    ### Assistant (Supervisor)
    ### Graph State Schema
    class AgentState(MessagesState):
        """Graph State Schmea"""

    ### Graph Config Schema
    class AgentConfig(TypedDict):
        summary_enabled: Optional[bool]
        component_system: Literal["rhds", "patternfly"]

    def movies_agent_node(state: AgentState, config: RunnableConfig):
        result = movies_agent.invoke(state, config)

        # Pick just last messages till human message
        agent_result = []
        result_messages = list(reversed(result["messages"]))
        for m in result_messages:
            if m.type == "human":
                break
            agent_result.append(m)
        agent_result.reverse()
        return {"messages": agent_result}

    ngui_agent = NextGenUILangGraphAgent(ngui_model)
    ngui_graph = ngui_agent.build_graph()

    async def ngui_node(state: MessagesState, config: RunnableConfig):
        configurable: AgentConfig = config.get("configurable", {})
        component_system = configurable.get("component_system")
        if not component_system:
            component_system = "rhds"
        logger.debug(f"\n\n---- RUN NGUI ---- component_system={component_system}")
        result = await ngui_graph.ainvoke(
            state,
            {
                "configurable": {
                    "component_system": component_system,
                }
            },
        )
        # Pick just last messages till human message
        agent_result = []
        result_messages = list(reversed(result["messages"]))
        for m in result_messages:
            if m.type == "human":
                break
            agent_result.append(m)
        agent_result.reverse()

        return {"messages": agent_result}

    async def summary(state: AgentState, config: RunnableConfig):
        configurable: AgentConfig = config.get("configurable", {})
        enabled = configurable.get("summary_enabled", True)
        logger.debug(f"\n\n----RUN SUMMARY ---- enabled: {enabled}")
        if not enabled:
            return
        # Get transformed data
        # TODO: Tune summary
        system_prompt = (
            "You are useful assistant to answer the user's question about movies."
            "If you'are asked to show picture or play trailer just say 'Here it is.'"
        )

        all_messages = [
            {"role": "system", "content": system_prompt},
        ]
        for m in state["messages"]:
            if NextGenUILangGraphAgent.is_next_gen_ui_message(m):
                continue
            all_messages.append(m)

        response = await model.ainvoke(all_messages)
        return {"messages": [response]}

    workflow = StateGraph(
        state_schema=AgentState,
        input=MessagesState,
        output=MessagesState,
        config_schema=AgentConfig,
    )
    workflow.add_node("movies", movies_agent_node)
    workflow.add_node("ngui", ngui_node)
    workflow.add_node("summary", summary)

    workflow.add_edge(START, "movies")
    workflow.add_edge("movies", "ngui")
    workflow.add_edge("ngui", "summary")
    workflow.add_edge("summary", END)

    assistant_graph = workflow.compile()

    return assistant_graph
