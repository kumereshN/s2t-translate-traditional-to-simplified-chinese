# main.py

from json.decoder import JSONDecodeError
from typing import List, Optional, Set, Tuple
from fastapi import FastAPI, Query
import json
import chinese_converter as cc
import re

from fastapi.param_functions import Body

description = """
This API translates traditional Chinese to simplified Chinese.
"""
app = FastAPI(title="Traditional to simplified Chinese translation API", description= description)

@app.get("/translate-query/", tags = ["Translate traditional Chinese to simplified Chinese"])
async def translate_traditional_to_simplified_chinese(queryID: Optional[int] = 0, query: Optional[str] = Query(None, alias="q")):
    # If there are Chinese characters present
    if re.search("[\u4e00-\u9FFF]", query):
        # convert traditional chinese to simplified chinese
        chinese_simplified = cc.to_simplified(query)
        results = {"queryID": queryID,"traditionalChinese": query, "simplifiedChinese": chinese_simplified}
        return results
    elif query == "":
        return 'You have not entered a query'
    else:
        return 'Invalid query. Only Chinese characters are accepted.'

@app.get("/translate-query-json/", tags = ["JSON object: Translate traditional Chinese to simplified Chinese"])
async def translate_traditional_to_simplified_chinese_json(queryId: Optional[int] = 0, query: Optional[str] = Query(None, alias="q")):
    """
    API to translate JSON object with traditional Chinese to simplified Chinese.
    """
    # Use try and except to check if json.loads(query) works
    try:
        """
        Deserialize s (a str, bytes or bytearray instance containing a JSON document) to a Python object using this conversion table.
        """       
        query_json = json.loads(query)
    except JSONDecodeError:
        return f"{query} is not a valid query. It needs to be in JSON format."
    
    # Transform the field's values into string format if they're not string
    query_json_clean = {field:str(value) for field, value in query_json.items()}
    # Convert Traditional chinese into Simplified Chinese
    query_json_convert = {field:cc.to_simplified(value) for field, value in query_json_clean.items()}
    results = {"queryId": queryId,"traditional_chinese": query_json, "simplified_chinese": query_json_convert}
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('traditional_to_simplified_chinese:app', reload=True, host="localhost", port=8000)
    