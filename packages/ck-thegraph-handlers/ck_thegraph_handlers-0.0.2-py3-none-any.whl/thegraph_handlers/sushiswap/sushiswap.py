from thegraph_handlers._protocols import AClosableHTTPClient
from thegraph_handlers.shared.base_swap import BaseSwap
from thegraph_handlers.shared.dispatch import ParserDispatch
from thegraph_handlers.sushiswap.parsers import (
    parse_burn,
    parse_liquidity_position,
    parse_mint,
    parse_swap,
)


class Sushiswap(BaseSwap):
    def __init__(self, client: AClosableHTTPClient) -> None:
        parser_dispatch = ParserDispatch(
            burn=parse_burn,
            liquidity_position=parse_liquidity_position,
            mint=parse_mint,
            swap=parse_swap,
        )
        url = "https://api.thegraph.com/subgraphs/name/sushiswap/exchange"
        # url = (
        #    "https://api.thegraph.com/subgraphs/name/dimitarnestorov/sushiswap-subgraph"
        # )

        BaseSwap.__init__(self, client, url, parser_dispatch)

    async def __aenter__(self) -> "Sushiswap":
        return self
