from fastapi import FastAPI
from assessment_app.routers.user_mgmt import router as user_mgmt_router
from assessment_app.routers.strategy import router as strategy_router
from assessment_app.routers.market_integration import router as market_router
from assessment_app.routers.analysis import router as analysis_router
from assessment_app.routers.backtest import router as backtest_router

app = FastAPI()

app.include_router(user_mgmt_router, prefix="", tags=["user_mgmt"])
app.include_router(strategy_router, prefix="", tags=["strategy"])
app.include_router(market_router, prefix="", tags=["market_data"])
app.include_router(analysis_router, prefix="", tags=["analysis"])
app.include_router(backtest_router, prefix="", tags=["backtest"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Simulator"}
