from langchain_community.tools import DuckDuckGoSearchRun
from typing import Dict, Any


def create_search_tool() -> DuckDuckGoSearchRun:
    return DuckDuckGoSearchRun()


def execute_search(query: str, max_results: int = 5) -> str:
    search = DuckDuckGoSearchRun()
    results = search.run(query)
    return results


def format_search_results(raw_results: str) -> Dict[str, Any]:
    lines = raw_results.split("\n")
    formatted_results = []

    current_result = {}
    for line in lines:
        line = line.strip()
        if not line:
            if current_result:
                formatted_results.append(current_result)
                current_result = {}
            continue

        if (
            line.startswith("[1]")
            or line.startswith("[2]")
            or line.startswith("[3]")
            or line.startswith("[4]")
            or line.startswith("[5]")
        ):
            if current_result:
                formatted_results.append(current_result)
                current_result = {}
            current_result["index"] = line[1:2]
            content = line[3:].strip()
            if " - " in content:
                title, url = content.rsplit(" - ", 1)
                current_result["title"] = title.strip()
                current_result["url"] = url.strip()
            else:
                current_result["title"] = content
        elif current_result:
            if "snippet" not in current_result:
                current_result["snippet"] = []
            current_result["snippet"].append(line)

    if current_result:
        formatted_results.append(current_result)

    for result in formatted_results:
        if "snippet" in result:
            result["snippet"] = " ".join(result["snippet"])

    return {"results": formatted_results, "count": len(formatted_results)}
