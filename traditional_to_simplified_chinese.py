# main.py

from typing import List, Optional, Set, Tuple
from fastapi import FastAPI, Query
import json
import chinese_converter as cc
import re

description = """
This API translates traditional Chinese to simplified Chinese.
"""
app = FastAPI(title="Traditional to simplified Chinese translation API", description= description)

@app.get("/translateQuery/", tags = ["Translate traditional Chinese to simplified Chinese"])
async def translate_traditional_to_simplified_chinese(query_id: Optional[int] = 0, query: Optional[str] = Query(None, alias="q")):
    # If there are Chinese characters present
    if re.search("[\u4e00-\u9FFF]", query):
        # convert traditional chinese to simplified chinese
        chinese_simplified = cc.to_simplified(query)
        results = {"query_id": query_id,"traditional chinese": query, "simplified chinese": chinese_simplified}
        return results
    elif query == "":
        return 'You have not entered a query'
    else:
        return 'Invalid query. Only Chinese characters are accepted.'

@app.get("/translateQueryJson/", tags = ["JSON object: Translate traditional Chinese to simplified Chinese"])
async def translate_traditional_to_simplified_chinese_json(query_id: Optional[int] = 0, query: Optional[str] = Query(None, alias="q")):
    """
    Check the type if it's a JSON string or a JSON object literal
    """
    # If it's a string, attempt to convert it to a JSON object literal
    if type(query) == str:
        query_json = json.loads(query)
        # If after converting and it's not a dictionary, return "invalid query"
        if not type(query_json) == dict:
            return query_json
    # If the query is not a dictionary, e.g: int, boolean
    elif not type(query) == dict:
        return "This is not a dictionary"
    # If it's a valid query, set query_json as a variable
    else:
        query_json = query

    # Transform the field's values into string format if they're not string
    query_json_clean = {field:str(value) for field, value in query_json.items()}
    # Convert Traditional chinese into Simplified Chinese
    query_json_convert = {field:cc.to_simplified(value) for field, value in query_json_clean.items()}
    results = {"query_id": query_id,"traditional chinese": query, "simplified chinese": query_json_convert}
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('traditional_to_simplified_chinese:app', reload=True, host="localhost", port=8000)
    