# main.py

from typing import Optional
from fastapi import FastAPI, Query
import chinese_converter as cc
import re

app = FastAPI()

@app.get("/query/")
async def translate_traditional_to_simplified(query_id: Optional[int] = 0, query: Optional[str] = Query(None, alias="q")):
    # If there are Chinese characters present
    if re.search("[\u4e00-\u9FFF]", query):
        # convert traditional chinese to simplified chinese
        chinese_simplified = cc.to_simplified(query)
        results = {"query_id": query_id,"traditional chinese": query, "simplified chinese": chinese_simplified}
        return results
    else:
        return 'Invalid query. Only accepts Chinese characters'
    