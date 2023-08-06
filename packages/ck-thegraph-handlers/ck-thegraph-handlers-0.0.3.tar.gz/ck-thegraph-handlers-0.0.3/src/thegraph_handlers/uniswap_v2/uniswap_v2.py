from thegraph_handlers._protocols import AClosableHTTPClient
from thegraph_handlers.shared.base_swap import BaseSwap
from thegraph_handlers.shared.dispatch import ParserDispatch
from thegraph_handlers.uniswap_v2.parsers import (
    parse_burn,
    parse_liquidity_position,
    parse_mint,
    parse_swap,
)


class UniswapV2(BaseSwap):
    def __init__(self, client: AClosableHTTPClient) -> None:
        parser_dispatch = ParserDispatch(
            burn=parse_burn,
            liquidity_position=parse_liquidity_position,
            mint=parse_mint,
            swap=parse_swap,
        )

        url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
        BaseSwap.__init__(self, client, url, parser_dispatch)

    async def __aenter__(self) -> "UniswapV2":
        return self
