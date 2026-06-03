from pydantic import BaseModel

# classes used on GET "Meme Token Detail - Single" endpoint
class GetV3TokenMemeDetailSingleTxRef(BaseModel):
    """
        Reference to a blockchain transaction associated with a meme token lifecycle event
        (creation, last update, or graduation). All fields are `None` when the event has
        not yet occurred.

        Attributes:
            tx_hash: base-58 transaction signature; `None` when the event has not occurred.
            slot: Solana slot number in which the transaction was confirmed; `None` when not
                yet confirmed or not applicable.
            block_time: unix timestamp (seconds) of the block that included the transaction;
                `None` when not available.
    """
    tx_hash: str | None = None
    slot: int | None = None
    block_time: int | None = None

class GetV3TokenMemeDetailSinglePool(BaseModel):
    """
        On-chain pool (bonding curve) state for a meme token at the time of the API call.
        Reserve values are returned as decimal strings because they are large integers that
        cannot be represented exactly as JSON numbers.

        Attributes:
            address: contract address of the bonding-curve pool.
            real_sol_reserves: actual SOL reserves held in the pool, in lamports (as string).
            real_token_reserves: actual token reserves held in the pool, in the token's
                raw (non-UI) units (as string).
            token_total_supply: total token supply tracked by the pool, in raw units (as string).
            virtual_token_reserves: virtual token reserves used by the bonding-curve pricing
                formula, in raw units (as string).
    """
    address: str
    real_sol_reserves: str
    real_token_reserves: str
    token_total_supply: str
    virtual_token_reserves: str

class GetV3TokenMemeDetailSingleMemeInfo(BaseModel):
    """
        Meme-platform-specific metadata for a token, covering its origin, lifecycle events,
        current bonding-curve state, and graduation status.

        Attributes:
            source: meme launchpad that originated the token (e.g. ``"pump_dot_fun"``);
                `None` if not determined.
            platform_id: contract address of the launchpad program on the chain; `None` if
                not available.
            created_at: transaction reference for the token creation event; `None` if not
                available.
            creation_time: unix timestamp (seconds) of the token creation; `None` if not
                available.
            creator: wallet address that deployed the token; `None` if not available.
            updated_at: transaction reference for the most recent on-chain update; `None` if
                not available.
            graduated_at: transaction reference for the graduation event (migration from the
                bonding curve to a DEX pool); all fields are `None` while the token has not
                yet graduated.
            graduated: `True` once the token has graduated to a DEX pool.
            graduated_time: unix timestamp (seconds) of the graduation event; `None` before
                graduation.
            pool: current bonding-curve pool state; `None` if pool data is unavailable.
            progress_percent: percentage of the bonding-curve funding target that has been
                reached (0–100); `None` if not available.
            address: contract address of the meme token (mirrors the top-level
                ``data.address`` field); `None` if not available.
    """
    source: str | None = None
    platform_id: str | None = None
    created_at: GetV3TokenMemeDetailSingleTxRef | None = None
    creation_time: int | None = None
    creator: str | None = None
    updated_at: GetV3TokenMemeDetailSingleTxRef | None = None
    graduated_at: GetV3TokenMemeDetailSingleTxRef | None = None
    graduated: bool | None = None
    graduated_time: int | None = None
    pool: GetV3TokenMemeDetailSinglePool | None = None
    progress_percent: float | None = None
    address: str | None = None

class GetV3TokenMemeDetailSingleData(BaseModel):
    """
        Full detail payload for a single meme token as returned by the Birdeye v3
        Meme Token Detail endpoint.

        Attributes:
            address: contract address of the meme token on the selected chain.
            name: human-readable name of the token; `None` if not available.
            symbol: ticker symbol of the token; `None` if not available.
            decimals: number of decimal places used by the token; `None` if not available.
            extensions: free-form metadata bag containing optional social and descriptive
                fields (e.g. ``twitter``, ``website``, ``description``); individual values
                may be `None`, and the whole dict is `None` when Birdeye has no metadata.
            logo_uri: URL of the token logo image; `None` if not available.
            price: latest known price of the token in USD; `None` if not available.
            liquidity: current on-chain liquidity of the token in USD; `None` if not
                available.
            circulating_supply: circulating token supply in UI units; `None` if not
                available.
            market_cap: market capitalisation in USD; `None` if not available.
            total_supply: total token supply in UI units; `None` if not available.
            fdv: fully-diluted valuation in USD; `None` if not available.
            meme_info: meme-platform-specific metadata including launchpad origin,
                bonding-curve pool state, and graduation status; `None` if not available.
    """
    address: str
    name: str | None = None
    symbol: str | None = None
    decimals: int | None = None
    extensions: dict[str, str | None] | None = None
    logo_uri: str | None = None
    price: float | None = None
    liquidity: float | None = None
    circulating_supply: float | None = None
    market_cap: float | None = None
    total_supply: float | None = None
    fdv: float | None = None
    meme_info: GetV3TokenMemeDetailSingleMemeInfo | None = None

class GetV3TokenMemeDetailSingleResponse(BaseModel):
    """
        Model used to represent the **Meme Token Detail - Single** endpoint from the
        Birdeye v3 API.

        Attributes:
            data: full detail payload for the requested meme token.
            success: `True` when the API call completed without errors.
    """
    data: GetV3TokenMemeDetailSingleData
    success: bool
