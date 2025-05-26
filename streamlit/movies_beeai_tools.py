# https://github.com/i-am-bee/beeai-framework/blob/main/python/examples/tools/custom/base.py

import asyncio
import sys
import logging
import json
from typing import Any

from pydantic import BaseModel, Field

from beeai_framework.context import RunContext
from beeai_framework.emitter import Emitter
from beeai_framework.errors import FrameworkError
from beeai_framework.tools import StringToolOutput, Tool, ToolRunOptions

from next_gen_ui_testing import data_set_movies

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MovieSearchByTitleToolInput(BaseModel):
    title: str = Field(description="Movie title e.g. 'Toy Story'")


class MovieSearchByTitleTool(
    Tool[MovieSearchByTitleToolInput, ToolRunOptions, StringToolOutput]
):
    name = "movie_search_by_title"
    description = "Search movies based on title."
    input_schema = MovieSearchByTitleToolInput

    def __init__(self, options: dict[str, Any] | None = None) -> None:
        super().__init__(options)

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "movies", "movie_search_by_title"],
            creator=self,
        )

    async def _run(
        self,
        input: MovieSearchByTitleToolInput,
        options: ToolRunOptions | None,
        context: RunContext,
    ) -> StringToolOutput:
        logger.debug("movie_search_by_title, title=%s", input.title)
        movies_data = data_set_movies.find_movie(input.title)
        m_str = json.dumps(movies_data, default=str)
        logger.debug("movie: %s", m_str)
        return StringToolOutput(result=m_str)


async def main() -> None:
    tool = MovieSearchByTitleTool()
    tool_input = MovieSearchByTitleToolInput(title="Toy Story")
    result = await tool.run(tool_input)
    print(result)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        sys.exit(e.explain())
