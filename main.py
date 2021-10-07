# main.py

from typing import Optional
from fastapi import FastAPI, Query
import chinese_converter as cc

app = FastAPI()

@app.get("/query/")
async def translate_traditional_to_simplified(query_id: Optional[int] = None, query: Optional[str] = Query(None, alias="q")):
    # convert traditional chinese to simplified chinese
    chinese_simplified = cc.to_simplified(query)
    results = {"traditional chinese": query, "simplified chinese": chinese_simplified}
    return results
    