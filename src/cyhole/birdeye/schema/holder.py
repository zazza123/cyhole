from pydantic import BaseModel


# classes used on GET "Token - Holder" endpoint
class GetTokenHolderItem(BaseModel):
    """
        Single top-holder entry returned by the v3 Token - Holder endpoint.

        Attributes:
            mint: contract address of the SPL token being held.
            owner: wallet address that owns the token balance.
            token_account: SPL token account address holding the balance for `owner`.
            amount: raw amount held, expressed in the token's smallest units (string).
            decimals: number of decimal places used by the token.
            ui_amount: UI-formatted amount (i.e. `amount` divided by `10 ** decimals`) as a number.
            is_scaled_ui_token: `True` when the token is a scaled-UI-amount SPL token; `None` if
                undetermined.
            multiplier: scaling multiplier applied to UI amounts of scaled-UI-amount tokens; `None`
                when not applicable.
    """
    mint: str
    owner: str
    token_account: str
    amount: str
    decimals: int
    ui_amount: float
    is_scaled_ui_token: bool | None = None
    multiplier: float | None = None

class GetTokenHolderData(BaseModel):
    """
        Payload of the v3 Token - Holder response.

        Attributes:
            items: ranked list of top holder entries (largest balance first by default).
    """
    items: list[GetTokenHolderItem]

class GetTokenHolderResponse(BaseModel):
    """
        Model used to represent the **Token - Holder** endpoint from birdeye API.

        Attributes:
            data: payload containing the ranked top-holder list.
            success: `True` when the API call completed without errors.
    """
    data: GetTokenHolderData
    success: bool


# classes used on POST "Token - Holder (Batch)" endpoint
class PostTokenHolderBatchItem(BaseModel):
    """
        Single wallet/token balance entry returned by the POST Token - Holder (Batch) endpoint.

        Attributes:
            mint: contract address of the SPL token being held.
            owner: wallet address whose balance is being reported.
            amount: UI-formatted balance (numeric).
            balance: raw balance expressed in the token's smallest units (string).
            decimals: number of decimal places used by the token.
    """
    mint: str
    owner: str
    amount: float
    balance: str
    decimals: int

class PostTokenHolderBatchData(BaseModel):
    """
        Payload of the POST Token - Holder (Batch) response.

        Attributes:
            items: list of balance entries, one per `(owner, mint)` combination requested. Owners
                that have never held the token are omitted from the list.
    """
    items: list[PostTokenHolderBatchItem]

class PostTokenHolderBatchBody(BaseModel):
    """
        Request body for the POST Token - Holder (Batch) endpoint.

        Attributes:
            token_address: contract address of the SPL token whose balances must be looked up.
            wallets: list of wallet addresses whose balance in `token_address` should be returned.
    """
    token_address: str
    wallets: list[str]

class PostTokenHolderBatchResponse(BaseModel):
    """
        Model used to represent the **Token - Holder (Batch)** endpoint from birdeye API.

        Attributes:
            data: payload containing the balance entries.
            success: `True` when the API call completed without errors.
    """
    data: PostTokenHolderBatchData
    success: bool


# classes used on GET "Token - Holder Distribution" endpoint
class GetHolderDistributionEntry(BaseModel):
    """
        Single holder entry in a Token - Holder Distribution response.

        Attributes:
            wallet: wallet (or SPL token-account, depending on the request `address_type`) address.
            holding: balance of the holder expressed in UI units, as a string to preserve precision.
            percent_of_supply: share of the token's total supply held, expressed as a fraction in
                `[0, 1]`.
    """
    wallet: str
    holding: str
    percent_of_supply: float

class GetHolderDistributionPagination(BaseModel):
    """
        Pagination block of a Token - Holder Distribution response.

        Attributes:
            offset: zero-based offset of the current batch within the full result set.
            limit: maximum number of entries returned per call.
            total: total number of entries that match the request filters across all pages.
    """
    offset: int
    limit: int
    total: int

class GetHolderDistributionRange(BaseModel):
    """
        Supply-share range applied by Birdeye when filtering the distribution.

        Attributes:
            min_percent: inclusive lower bound on `percent_of_supply` (in `percent` mode); echoes the
                request parameter or Birdeye's default.
            max_percent: inclusive upper bound on `percent_of_supply` (in `percent` mode); echoes the
                request parameter or Birdeye's default.
    """
    min_percent: float
    max_percent: float

class GetHolderDistributionSummary(BaseModel):
    """
        Aggregate summary of the holders matching the distribution filters.

        Attributes:
            total_holding: cumulative balance of matched holders in UI units, as a string to preserve
                precision.
            percent_of_supply: cumulative `total_holding` expressed as a fraction (`[0, 1]`) of total
                supply.
            wallet_count: number of distinct holders that matched the filter range.
    """
    total_holding: str
    percent_of_supply: float
    wallet_count: int

class GetHolderDistributionData(BaseModel):
    """
        Payload of the Token - Holder Distribution response.

        Attributes:
            token_address: contract address of the token the distribution refers to.
            mode: filter mode actually applied (`top` or `percent`).
            range: supply-share range used by the filter.
            holders: list of individual holder entries (empty when `include_list=false`).
            pagination: pagination metadata describing the returned batch and total match count.
            summary: cumulative figures over the holders that matched the filter range.
    """
    token_address: str
    mode: str
    range: GetHolderDistributionRange
    holders: list[GetHolderDistributionEntry]
    pagination: GetHolderDistributionPagination
    summary: GetHolderDistributionSummary

class GetHolderDistributionResponse(BaseModel):
    """
        Model used to represent the **Token - Holder Distribution** endpoint from birdeye API.

        Attributes:
            data: holder-distribution payload.
            success: `True` when the API call completed without errors.
    """
    data: GetHolderDistributionData
    success: bool


# classes used on GET "Token - Holder Profile" endpoint
class GetHolderProfileSummary(BaseModel):
    """
        Headline counts of the holders aggregated by the Token - Holder Profile endpoint.

        Attributes:
            total_holder: total number of distinct holders Birdeye has observed for the token.
            total_holding: cumulative balance of all holders, in UI units.
            percent_of_supply: cumulative `total_holding` expressed as a percent (`[0, 100]`) of the
                token total supply.
    """
    total_holder: int
    total_holding: float
    percent_of_supply: float

class GetHolderProfileTagBreakdown(BaseModel):
    """
        Aggregate trading and holding figures for one Birdeye holder-tag bucket
        (`bundler`, `sniper`, `insider`, `dev`, `smart_trader`).

        Attributes:
            tag: name of the tag this row describes.
            holder_count: number of distinct wallets currently classified under `tag`.
            hold_amount: cumulative holding of wallets in this tag, in UI units (string).
            percent_of_supply: cumulative `hold_amount` expressed as a percent (`[0, 100]`) of total supply.
            avg_buy_price: average buy price (USD) across the wallets in this tag (string).
            buy_volume: cumulative buy volume of wallets in this tag, in the token UI units (string).
            buy_volume_usd: cumulative buy volume of wallets in this tag, expressed in USD (string).
            sell_volume: cumulative sell volume of wallets in this tag, in the token UI units (string).
            sell_volume_usd: cumulative sell volume of wallets in this tag, expressed in USD (string).
            pnl: cumulative profit-and-loss of wallets in this tag, in USD (string).
    """
    tag: str
    holder_count: int
    hold_amount: str
    percent_of_supply: float
    avg_buy_price: str
    buy_volume: str
    buy_volume_usd: str
    sell_volume: str
    sell_volume_usd: str
    pnl: str

class GetHolderProfileTokenTopHolder(BaseModel):
    """
        Top-10 holder concentration block of the Token - Holder Profile response.

        Attributes:
            hold_amount: cumulative balance of the top-10 holders, in UI units (string).
            percent_of_supply: cumulative `hold_amount` expressed as a percent (`[0, 100]`) of total supply.
    """
    hold_amount: str
    percent_of_supply: float

class GetHolderProfileToken(BaseModel):
    """
        Token-level market snapshot returned alongside the holder profile.

        Attributes:
            creation_time: unix-second timestamp at which Birdeye first detected the token.
            liquidity: total on-chain liquidity in USD.
            market_cap: current market capitalisation in USD.
            volume_1h: traded volume over the trailing 1h window in the token UI units.
            volume_1h_usd: traded volume over the trailing 1h window in USD.
            buy_volume_1h: buy-side traded volume over the trailing 1h window in the token UI units.
            buy_volume_1h_usd: buy-side traded volume over the trailing 1h window in USD.
            sell_volume_1h: sell-side traded volume over the trailing 1h window in the token UI units.
            sell_volume_1h_usd: sell-side traded volume over the trailing 1h window in USD.
            is_scaled_ui_token: `True` when the token is a scaled-UI-amount SPL token; `None` if
                undetermined.
            top10_holder: cumulative-holding snapshot of the top-10 holders.
    """
    creation_time: int
    liquidity: float
    market_cap: float
    volume_1h: float
    volume_1h_usd: float
    buy_volume_1h: float
    buy_volume_1h_usd: float
    sell_volume_1h: float
    sell_volume_1h_usd: float
    is_scaled_ui_token: bool | None = None
    top10_holder: GetHolderProfileTokenTopHolder

class GetHolderProfileData(BaseModel):
    """
        Payload of the Token - Holder Profile response.

        Attributes:
            token: token-level market snapshot (creation time, liquidity, 1h volume breakdown,
                top-10 holder concentration).
            holder_summary: headline holder counts for the token.
            tags: per-tag breakdown of holder and trading figures (always five entries: `bundler`,
                `sniper`, `insider`, `dev`, `smart_trader`).
    """
    token: GetHolderProfileToken
    holder_summary: GetHolderProfileSummary
    tags: list[GetHolderProfileTagBreakdown]

class GetHolderProfileResponse(BaseModel):
    """
        Model used to represent the **Token - Holder Profile** endpoint from birdeye API.

        Attributes:
            data: holder-profile payload.
            success: `True` when the API call completed without errors.
    """
    data: GetHolderProfileData
    success: bool
