from typing import Any

from pydantic import BaseModel, Field

# classes used on GET "Token - Security" endpoint
class GetTokenSecurityDataSolana(BaseModel):
    """
        Solana-specific security/risk profile of a token returned by the Birdeye
        **Token - Security** endpoint.

        All ownership and authority fields are optional because Birdeye returns
        `null` for them when the token has renounced/cleared the corresponding
        on-chain authority. Balance and percentage fields refer to the holdings
        of the related authority over the token's total supply.

        Attributes:
            creator_address: address that created the token (alias `creatorAddress`); `None` if unknown.
            creator_owner_address: owner of `creator_address` at the time of token creation
                (alias `creatorOwnerAddress`); `None` if the creator was an EOA or no longer tracked.
            owner_address: current on-chain owner of the token authority (alias `ownerAddress`);
                `None` when ownership has been renounced.
            owner_of_owner_address: owner of `owner_address` (alias `ownerOfOwnerAddress`);
                `None` if owner is an EOA or ownership has been renounced.
            creation_transaction: signature of the transaction that created the token
                (alias `creationTx`); `None` if unknown.
            creation_time_unix: unix-second timestamp of the creation transaction (alias `creationTime`).
            creation_slot: slot of the creation transaction (alias `creationSlot`).
            mint_transaction: signature of the mint transaction (alias `mintTx`).
            mint_time_unix: unix-second timestamp of the mint transaction (alias `mintTime`).
            mint_slot: slot of the mint transaction (alias `mintSlot`).
            mintable: whether the token can still be minted; `None` if the API cannot determine it.
            renounce: whether the mint authority has been renounced; `None` if undetermined.
            creator_balance: token balance currently held by the creator address (alias `creatorBalance`).
            creator_percentage: creator balance expressed as a fraction (0..1) of total supply
                (alias `creatorPercentage`).
            owner_balance: token balance currently held by the owner address (alias `ownerBalance`).
            owner_percentage: owner balance expressed as a fraction (0..1) of total supply
                (alias `ownerPercentage`).
            metaplex_update_authority: Metaplex metadata update authority (alias `metaplexUpdateAuthority`).
            metaplex_owner_update_authority: owner of the Metaplex update authority address
                (alias `metaplexOwnerUpdateAuthority`); `None` when no upstream owner is tracked.
            metaplex_update_balance: token balance held by the Metaplex update authority
                (alias `metaplexUpdateAuthorityBalance`).
            metaplex_update_percentage: Metaplex update authority balance expressed as a fraction (0..1)
                of total supply (alias `metaplexUpdateAuthorityPercent`).
            mutable_metadata: whether the on-chain Metaplex metadata of the token is still mutable
                (alias `mutableMetadata`).
            top_10_holder_balance: cumulative token balance of the top-10 holders (alias `top10HolderBalance`).
            top_10_holder_percentage: top-10 holders' cumulative balance as a fraction (0..1) of total
                supply (alias `top10HolderPercent`).
            top_10_user_balance: cumulative token balance of the top-10 *user* wallets (excluding programs)
                (alias `top10UserBalance`).
            top_10_user_percentage: top-10 users' cumulative balance as a fraction (0..1) of total supply
                (alias `top10UserPercent`).
            is_true_token: Birdeye flag marking the token as one of its verified entries
                (alias `isTrueToken`); `None` when unverified.
            fake_token: Birdeye flag marking the token as a known scam/fake (alias `fakeToken`);
                `None` when Birdeye has not categorised it.
            total_supply: total on-chain supply of the token, expressed in UI units (alias `totalSupply`).
            pre_market_holder: list of addresses that received tokens before any public market existed
                (alias `preMarketHolder`).
            lock_info: free-form payload describing on-chain locks (e.g. team vesting); `None` when no
                lock information is known (alias `lockInfo`).
            freezeable: whether the SPL freeze authority can still freeze accounts; `None` if undetermined.
            freeze_authority: address that owns the freeze authority (alias `freezeAuthority`);
                `None` when the freeze authority has been renounced.
            transfer_fee_enable: whether the Token-2022 transfer-fee extension is active
                (alias `transferFeeEnable`); `None` if the extension is absent or undetermined.
            transfer_fee_data: free-form payload describing the active transfer-fee parameters
                (alias `transferFeeData`); `None` when no fee data is available.
            is_token_2022: whether the token is an SPL Token-2022 mint (alias `isToken2022`).
            non_transferable: whether the Token-2022 non-transferable extension is active
                (alias `nonTransferable`); `None` if undetermined.
            jup_strict_list: whether the token is part of Jupiter's strict token list
                (alias `jupStrictList`); `None` when Birdeye did not populate the flag.
    """
    creator_address: str | None = Field(alias = "creatorAddress", default = None)
    creator_owner_address: str | None = Field(alias = "creatorOwnerAddress", default = None)
    owner_address: str | None = Field(alias = "ownerAddress", default = None)
    owner_of_owner_address: str | None = Field(alias = "ownerOfOwnerAddress", default = None)
    creation_transaction: str | None = Field(alias = "creationTx", default = None)
    creation_time_unix: int | None = Field(alias = "creationTime", default = None)
    creation_slot: int | None = Field(alias = "creationSlot", default = None)
    mint_transaction: str | None = Field(alias = "mintTx", default = None)
    mint_time_unix: int | None = Field(alias = "mintTime", default = None)
    mint_slot: int | None = Field(alias = "mintSlot", default = None)
    mintable: bool | None = None
    renounce: bool | None = None
    creator_balance: float | None = Field(alias = "creatorBalance", default = None)
    creator_percentage: float | None = Field(alias = "creatorPercentage", default = None)
    owner_balance: float | None = Field(alias = "ownerBalance", default = None)
    owner_percentage: float | None = Field(alias = "ownerPercentage", default = None)
    metaplex_update_authority: str = Field(alias = "metaplexUpdateAuthority")
    metaplex_owner_update_authority: str | None = Field(alias = "metaplexOwnerUpdateAuthority", default = None)
    metaplex_update_balance: float = Field(alias = "metaplexUpdateAuthorityBalance")
    metaplex_update_percentage: float = Field(alias = "metaplexUpdateAuthorityPercent")
    mutable_metadata: bool = Field(alias = "mutableMetadata")
    top_10_holder_balance: float = Field(alias = "top10HolderBalance")
    top_10_holder_percentage: float = Field(alias = "top10HolderPercent")
    top_10_user_balance: float = Field(alias = "top10UserBalance")
    top_10_user_percentage: float = Field(alias = "top10UserPercent")
    is_true_token: bool | None = Field(alias = "isTrueToken", default = None)
    fake_token: bool | None = Field(alias = "fakeToken", default = None)
    total_supply: float = Field(alias = "totalSupply")
    pre_market_holder: list[str] = Field(alias = "preMarketHolder")
    lock_info: Any | None = Field(alias = "lockInfo", default = None)
    freezeable: bool | None = None
    freeze_authority: str | None = Field(alias = "freezeAuthority", default = None)
    transfer_fee_enable: bool | None = Field(alias = "transferFeeEnable", default = None)
    transfer_fee_data: Any | None = Field(alias = "transferFeeData", default = None)
    is_token_2022: bool = Field(alias = "isToken2022")
    non_transferable: bool | None = Field(alias = "nonTransferable", default = None)
    jup_strict_list: bool | None = Field(alias = "jupStrictList", default = None)

class GetTokenSecurityResponse(BaseModel):
    """
        Model used to represent the **Token - Security** endpoint from birdeye API.

        Attributes:
            data: security profile of the token. When the request targets Solana the payload is
                parsed into the typed [`GetTokenSecurityDataSolana`][cyhole.birdeye.schema.GetTokenSecurityDataSolana]
                schema; for every other supported chain the payload is left as a free-form
                dictionary because Birdeye returns a chain-specific (EVM-style) shape.
            success: `True` when the API call completed without errors.
    """
    data: GetTokenSecurityDataSolana | dict[str, Any]
    success: bool

