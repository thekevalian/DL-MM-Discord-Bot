import requests
import json
from typing import Literal


class DeadlockAPI:
    """
    Wrapper for Deadlockapi
    """

    assets_url = "https://assets.deadlock-api.com"
    gameplay_url = "https://api.deadlock-api.com"

    def __init__(self):
        pass

    # Functions for retrieving information

    def _is_valid_request(self, status_code: int) -> bool:
        """Returns True if status code is valid

        Args:
            status_code (int): status code to verify

        Returns:
            bool: Represents status code as a successful or failed request
        """
        return status_code in [200, 201, 202]

    def _retrieve_url(self, url: str, params: dict = {}) -> dict | None:
        """Retrieves results if request is successful

        Args:
            url (str): URL to post GET request
            params (dict): dictionary of query
        Returns:
            dict | None: Returns json as a dict if GET succeeds. None otherwise.
        """
        response = requests.get(url, params=params)
        if self._is_valid_request(response.status_code):
            return response.json()
        return None

    # Assets API
    # Get information about the game's assets

    def get_heroes(
        self, language: str = None, client_version: int = None, only_active: bool = None
    ) -> list | None:
        """Returns the data about the heroes

        Args:
            language (str, optional): Language. Defaults to None.
            client_version (int, optional): Version of the client. Defaults to None.
            only_active (bool, optional): Set true to get playable heroes only. Defaults to None.

        Returns:
            list|None: List of Hero Metadata or None if request fails
        """
        params = {
            k: v for k, v in locals().items() if not k in ["self"] and v is not None
        }
        return self._retrieve_url(f"{self.assets_url}/v2/heroes", params=params)

    def get_hero(
        self, hero_id: int, language: str = None, client_version: int = None
    ) -> dict | None:
        """Returns the metadata of the specified hero from the hero_id

        Args:
            hero_id (int): Hero ID
            language (str, optional): Language. Defaults to None.
            client_version (int, optional): Version of the client. Defaults to None.

        Returns:
            dict|None: Hero Metadata
        """
        params = {
            k: v
            for k, v in locals().items()
            if not k in ["self", "hero_id"] and v is not None
        }
        return self._retrieve_url(
            f"{self.assets_url}/v2/heroes/{hero_id}", params=params
        )

    def get_hero_by_name(
        self, hero_name: str, language: str = None, client_version: int = None
    ) -> dict | None:
        """Returns the metadata of the specified hero from the hero_name

        Args:
            hero_id (str): hero name (casing is ignored by api)
            language (str, optional): Language. Defaults to None.
            client_version (int, optional): Version of the client. Defaults to None.

        Returns:
            dict|None: Hero Metadata
        """
        params = {
            k: v
            for k, v in locals().items()
            if not k in ["self", "hero_name"] and v is not None
        }
        return self._retrieve_url(
            f"{self.assets_url}/v2/heroes/by-name/{hero_name}", params=params
        )
    


    # Items TODO

    def get_items(
        self, language: str = None, client_version: int = None
    ) -> dict | None:
        """Returns metadata of everyithing in the itemshop and all abilities for all characters

        Args:
            language (str, optional): Language. Defaults to None.
            client_version (int, optional): Version of the client. Defaults to None.

        Returns:
            dict | None: Item metadata
        """        
        params = {
        k: v for k, v in locals().items() if k != "self" and v is not None
        }

        return self._retrieve_url(f"{self.assets_url}/v2/items", params=params)

    def get_item(
        self, id_or_class_name: int, language: str = None, client_version: int = None
    ) -> dict | None:
        """Returns metadata of specified items from the id_or_class_name

        Args:
            id_or_class_name (int): item name (casing is ignored by api)
            language (str, optional): Language. Defaults to None.
            client_version (int, optional): Version of the client. Defaults to None.

        Returns:
            dict | None: Item metadata
        """        
        params = {
            k: v
            for k, v in locals().items()
            if k not in ["self", "id_or_class_name"] and v is not None
        }

        return self._retrieve_url(f"{self.assets_url}/v2/items/{id_or_class_name}", params=params)



    # Asset Defaults
    def get_asset_default(
        self,
        option: Literal[
            "client-versions",
            "ranks",
            "build-tags",
            "map",
            "colors",
            "steam-info",
            "icons",
            "sounds",
        ],
    ) -> list | None:
        """Returns the metadata about any of the options

        Args:
            TODO: Not all have been tested
            option (Literal["client-versions",
                            "ranks", "build-tags",
                            "map", "colors", "steam-info",
                            "icons", "sounds"]): Choose the asset metadata you want to retrieve

        Returns:
            list|None: List of the metadata
        """
        endpoint = f"{self.assets_url}/v2/{option}"
        return self._retrieve_url(endpoint)

    # Gameplay API
    # Matches TODO

    def get_match_metadata(self, match_id: int) -> dict:
        return self._retrieve_url(
            f"{self.gameplay_url}/v1/matches/{match_id}/metadata",
            params={"is_custom": None},
        )

    # Custom Matches TODO

    # Players

    def get_hero_stats(
        self,
        account_ids: int | list[int],
        min_unix_timestamp: int | None = None,
        max_unix_timestamp: int | None = None,
        min_duration_s: int | None = None,
        max_duration_s: int | None = None,
        min_networth: int | None = None,
        max_networth: int | None = None,
        min_average_badge: int | None = None,
        max_average_badge: int | None = None,
        min_match_id: int | None = None,
        max_match_id: int | None = None,
    ) -> list | None:
        """
        Returns statistics for each hero played by a given player account

        Args:
            account_ids (int, list[int]): Required. 1–100 account IDs in SteamID3 format. Will be converted to a comma-separated list.
            min_unix_timestamp (int | None): Optional. Minimum match start time (Unix timestamp).
            max_unix_timestamp (int | None): Optional. Maximum match start time (Unix timestamp).
            min_duration_s (int | None): Optional. Minimum match duration in seconds (0–7000).
            max_duration_s (int | None): Optional. Maximum match duration in seconds (0–7000).
            min_networth (int | None): Optional. Minimum player net worth.
            max_networth (int | None): Optional. Maximum player net worth.
            min_average_badge (int | None): Optional. Minimum average badge level (0–116).
            max_average_badge (int | None): Optional. Maximum average badge level (0–116).
            min_match_id (int | None): Optional. Minimum match ID.
            max_match_id (int | None): Optional. Maximum match ID.

        Returns:
            list|None: List of hero stats.
        """

        if isinstance(account_ids, int):
            account_ids = [account_ids]
        params = {
            k: v for k, v in locals().items() if not k in ["self"] and v is not None
        }
        return self._retrieve_url(f"{self.gameplay_url}/v1/players/hero-stats", params)

    def get_batch_steam_profile(self, account_ids: int | list[int]) -> list | None:
        """Returns Steam profiles of players.

        Args:
            account_ids (int | list[int]): List of account ids for steam profiles

        Returns:
            list|None: Metadata of steam profiles
        """
        if isinstance(account_ids, int):
            account_ids = [account_ids]
        params = {
            k: v for k, v in locals().items() if not k in ["self"] and v is not None
        }
        return self._retrieve_url(f"{self.gameplay_url}/v1/players/steam", params)

    def get_steam_profile_search(self, search_query: str | int) -> list | None:
        """Lets you search for Steam profiles by account_id or personaname.

        Args:
            search_query (str): Can be string for account_id or personaname

        Returns:
            list|None: List of steam players similar to search query
        """
        params = {
            k: v for k, v in locals().items() if not k in ["self"] and v is not None
        }
        return self._retrieve_url(
            f"{self.gameplay_url}/v1/players/steam-search", params
        )

    def get_enemy_stats(
        self,
        account_id: int,
        min_unix_timestamp: int | None = None,
        max_unix_timestamp: int | None = None,
        min_duration_s: int | None = None,
        max_duration_s: int | None = None,
        min_average_badge: int | None = None,
        max_average_badge: int | None = None,
        min_match_id: int | None = None,
        max_match_id: int | None = None,
        min_matches_played: int | None = None,
        max_matches_played: int | None = None,
    ) -> list | None:
        """
        Returns the enemy stats

        Args:
            account_id (int, list[int]): Required. account ID in SteamID3 format.
            min_unix_timestamp (int | None): Optional. Minimum match start time (Unix timestamp).
            max_unix_timestamp (int | None): Optional. Maximum match start time (Unix timestamp).
            min_duration_s (int | None): Optional. Minimum match duration in seconds (0–7000).
            max_duration_s (int | None): Optional. Maximum match duration in seconds (0–7000).
            min_average_badge (int | None): Optional. Minimum average badge level (0–116).
            max_average_badge (int | None): Optional. Maximum average badge level (0–116).
            min_match_id (int | None): Optional. Minimum match ID.
            max_match_id (int | None): Optional. Maximum match ID.
            min_matches_played (int | None): Optional. Minimum matches played.
            max_matches_played (int | None): Optional. Maximum matches played.

        Returns:
            list|None: List of enemy stats.
        """
        params = {
            k: v
            for k, v in locals().items()
            if not k in ["self", "account_id"] and v is not None
        }
        return self._retrieve_url(
            f"{self.gameplay_url}/v1/players/{account_id}/enemy-stats", params
        )

    def get_match_stats(
        self,
        account_id: int,
        force_refetch: bool = False,
        only_stored_history: bool = False,
    ) -> list | None:
        """Returns the player match history for the given account_id

        Args:
            account_id (int): The players SteamID3
            force_refetch (bool | None): Refetch the match history from Steam, even if it is already cached in ClickHouse. Only use this if you are sure that the data in ClickHouse is outdated. Enabling this flag results in a strict rate limit.
            only_stored_history (bool | None): Return only the already stored match history from ClickHouse. There is no rate limit for this option, so if you need a lot of data, you can use this option. This option is not compatible with force_refetch.
            # TODO verify why force_refetch and only_stored_history don't work
        Returns:
            list|None: List of player match history data
        """
        params = {
            k: v for k, v in locals().items() if not k in ["self", "account_id"] and v
        }
        return self._retrieve_url(
            f"{self.gameplay_url}/v1/players/{account_id}/match-history", params=params
        )

    def get_mate_stats(
        self,
        account_id: int,
        min_unix_timestamp: int | None = None,
        max_unix_timestamp: int | None = None,
        min_duration_s: int | None = None,
        max_duration_s: int | None = None,
        min_average_badge: int | None = None,
        max_average_badge: int | None = None,
        min_match_id: int | None = None,
        max_match_id: int | None = None,
        min_matches_played: int | None = None,
        max_matches_played: int | None = None,
        same_party: bool | None = None,
    ) -> list | None:
        """
        Returns the mate stats

        Args:
            account_id (int, list[int]): Required. account ID in SteamID3 format.
            min_unix_timestamp (int | None): Optional. Minimum match start time (Unix timestamp).
            max_unix_timestamp (int | None): Optional. Maximum match start time (Unix timestamp).
            min_duration_s (int | None): Optional. Minimum match duration in seconds (0–7000).
            max_duration_s (int | None): Optional. Maximum match duration in seconds (0–7000).
            min_average_badge (int | None): Optional. Minimum average badge level (0–116).
            max_average_badge (int | None): Optional. Maximum average badge level (0–116).
            min_match_id (int | None): Optional. Minimum match ID.
            max_match_id (int | None): Optional. Maximum match ID.
            min_matches_played (int | None): Optional. Minimum matches played.
            max_matches_played (int | None): Optional. Maximum matches played.
            same_party (bool | None): Optional. Filter based on whether the mates were on the same party.

        Returns:
            list|None: List of mate stats.
        """
        params = {
            k: v
            for k, v in locals().items()
            if not k in ["self", "account_id"] and v is not None
        }
        print(params)
        return self._retrieve_url(
            f"{self.gameplay_url}/v1/players/{account_id}/mate-stats", params
        )

    def get_party_stats(
        self,
        account_id: int,
        min_unix_timestamp: int | None = None,
        max_unix_timestamp: int | None = None,
        min_duration_s: int | None = None,
        max_duration_s: int | None = None,
        min_average_badge: int | None = None,
        max_average_badge: int | None = None,
        min_match_id: int | None = None,
        max_match_id: int | None = None,
    ) -> list | None:
        """
        Returns the party stats

        Args:
            account_id (int, list[int]): Required. account ID in SteamID3 format.
            min_unix_timestamp (int | None): Optional. Minimum match start time (Unix timestamp).
            max_unix_timestamp (int | None): Optional. Maximum match start time (Unix timestamp).
            min_duration_s (int | None): Optional. Minimum match duration in seconds (0–7000).
            max_duration_s (int | None): Optional. Maximum match duration in seconds (0–7000).
            min_average_badge (int | None): Optional. Minimum average badge level (0–116).
            max_average_badge (int | None): Optional. Maximum average badge level (0–116).
            min_match_id (int | None): Optional. Minimum match ID.
            max_match_id (int | None): Optional. Maximum match ID.

        Returns:
            list|None: List of party stats.
        """
        params = {
            k: v
            for k, v in locals().items()
            if not k in ["self", "account_id"] and v is not None
        }
        return self._retrieve_url(
            f"{self.gameplay_url}/v1/players/{account_id}/party-stats", params
        )

    # MMR TODO

    def get_batch_mmr(
        self, account_ids: int | list[int], max_match_id: int | None = None
    ) -> list | None:
        """Batch Player MMR

        Args:
            account_ids (int | list[int]): list of account ids, Account IDs are in SteamID3 format.
            max_match_id (int | None, optional): Filter matches based on their ID. Defaults to None.

        Returns:
            list|None: List of MMR data for account_ids
        """
        if isinstance(account_ids, int):
            account_ids = [account_ids]
        params = {
            k: v for k, v in locals().items() if not k in ["self"] and v is not None
        }
        return self._retrieve_url(f"{self.gameplay_url}/v1/players/mmr", params)

    def get_batch_hero_mmr(
        self,
        hero_id: int,
        account_ids: int | list[int],
        max_match_id: int | None = None,
    ) -> list | None:
        """Batch Player Hero MMR

        Args:
            hero_id (int): The hero ID to fetch the MMR history for.
            account_ids (int | list[int]): list of account ids, Account IDs are in SteamID3 format.
            max_match_id (int | None, optional): Filter matches based on their ID. Defaults to None.

        Returns:
            list|None: Hero MMR data for account_ids
        """
        if isinstance(account_ids, int):
            account_ids = [account_ids]
        params = {
            k: v
            for k, v in locals().items()
            if not k in ["self", "hero_id"] and v is not None
        }
        return self._retrieve_url(
            f"{self.gameplay_url}/v1/players/mmr/{hero_id}", params
        )

    def get_mmr_history(self, account_id: int) -> list | None:
        """Gets the Player's MMR History

        Args:
            account_id (int): account id of player. Account IDs are in SteamID3 format.

        Returns:
            list|None: Data of Player's MMR History
        """
        return self._retrieve_url(
            f"{self.gameplay_url}/v1/players/{account_id}/mmr-history"
        )

    def get_hero_mmr_history(self, account_id: int, hero_id: int) -> list | None:
        """Gets the Player Hero MMR History

        Args:
            account_id (int): account id of player. Account IDs are in SteamID3 format.
            hero_id (int): The hero ID to fetch the MMR history for.

        Returns:
            list|None: Data of Player Hero MMR History
        """
        return self._retrieve_url(
            f"{self.gameplay_url}/v1/players/{account_id}/mmr-history/{hero_id}"
        )

    # Leaderboard TODO
    # Analytics TODO
    # Builds TODO
    # Patches TODO


if __name__ == "__main__":
    deadlockapi = DeadlockAPI()
    response = deadlockapi.get_steam_profile_search("Deathy")[0]
    account_id = response["account_id"]
    mmr_hist = deadlockapi.get_mmr_history(account_id)
    print(json.dumps(response, indent=2))
    print(json.dumps(mmr_hist[-1], indent=2))
    """with open("Randomshit", "w") as f: 
        json.dump(deadlockapi.get_match_metadata(41986546), f,  indent = 2)
    """
    with open("items", "w") as f: 
        json.dump(deadlockapi.get_item(365620721) , f,  indent = 2)




