from fastapi import Depends, APIRouter
from assessment_app.service.auth_service import get_current_user

router = APIRouter()

# @router.post("/backtest", response_model=BacktestResponse)
# async def backtest_strategy(request: BacktestRequest):
#     """
#     Backtest a trading strategy over a specified period.
#
#     Parameters:
#     - request: BacktestRequest
#         - strategy_id: str
#             The ID of the strategy to backtest.
#         - portfolio_id: str
#             The ID of the portfolio to apply the strategy to.
#         - start_date: datetime
#             The start date for the backtest.
#         - end_date: datetime
#             The end date for the backtest.
#         - initial_capital: float
#             The initial capital to start the backtest with.
#
#     Returns:
#     - BacktestResponse
#         - start_date: datetime
#             The start date of the backtest.
#         - end_date: datetime
#             The end date of the backtest.
#         - initial_capital: float
#             The initial capital used for the backtest.
#         - final_capital: float
#             The final capital after the backtest.
#         - trades: List[Trade]
#             A list of trades executed during the backtest.
#         - profit_loss: float
#             The total profit or loss over the backtest period.
#         - annualized_return: float
#             The annualized return of the strategy over the backtest period.
#     """
#     pass