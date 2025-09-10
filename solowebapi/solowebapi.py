import logging
from typing import Optional, Union
from dataclasses import dataclass

import aiohttp

logger = logging.getLogger(__name__)

BASE_URL = "https://pocomacho.ru/solonetbot/api/v1/modules"


@dataclass
class BaseLicenseResponse:
    """
    Base class for license API responses.

    :param action: The performed action (check, grant, revoke)
    :param module: Module name the license relates to
    :param ok: Whether the request was successful
    :param user_id: ID of the user for whom the action was performed
    :param is_active: Whether the license is active
    :param expiry_date: Expiration date of the license, if available
    :param updated_at: Timestamp when license was last updated
    """
    action: str
    module: str
    ok: bool
    user_id: int
    is_active: Optional[bool] = None
    expiry_date: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class CheckLicenseResponse(BaseLicenseResponse):
    """Response for a license check action."""
    pass


@dataclass
class GrantLicenseResponse(BaseLicenseResponse):
    """Response for granting a license."""
    created: Optional[bool] = None


@dataclass
class RevokeLicenseResponse(BaseLicenseResponse):
    """Response for revoking a license."""
    message: Optional[str] = None


LicenseResponse = Union[CheckLicenseResponse, GrantLicenseResponse, RevokeLicenseResponse]


def _parse_license_response(data: dict) -> Optional[LicenseResponse]:
    """
    Parse a license response JSON dictionary into the corresponding dataclass.

    :param data: JSON dictionary returned by the license API
    :return: Parsed license response object, or None if action is unknown
    """
    action = data.get("action")
    if action == "check":
        return CheckLicenseResponse(**data)
    elif action == "grant":
        return GrantLicenseResponse(**data)
    elif action == "revoke":
        return RevokeLicenseResponse(**data)
    else:
        logger.error("Unknown action in response: %s", action)
        return None


class SoloWebAPI:
    """
    Async API client for SoloBot license management endpoints.

    :param username: API username
    :param password: API password
    :param verify_ssl: Whether to verify SSL certificates (default True)
    :param timeout: Request timeout in seconds (default 60)
    :param base_url: Base API URL (default BASE_URL)
    """

    def __init__(
            self,
            username: str,
            password: str,
            verify_ssl: bool = True,
            timeout: int = 60,
            base_url: str = BASE_URL,
    ):
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.base_url = base_url.rstrip("/")
        self._session: Optional[aiohttp.ClientSession] = None

    async def _ensure_session(self):
        """
        Ensure the aiohttp ClientSession is created and ready.
        """
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(
                auth=aiohttp.BasicAuth(self.username, self.password),
                timeout=timeout,
            )

    async def close(self):
        """
        Close the aiohttp ClientSession.
        """
        if self._session and not self._session.closed:
            await self._session.close()

    def _build_url(self, module: str, path: str) -> str:
        """
        Construct a full API URL for a given module and endpoint.

        :param module: Module name
        :param path: API path
        :return: Full API URL
        """
        return f"{self.base_url}/{module}/{path}"

    async def _post_json(self, url: str, payload: dict) -> Optional[dict]:
        """
        Send a POST request with JSON payload and parse the JSON response.

        :param url: Full API URL
        :param payload: JSON payload
        :return: JSON response dictionary, or None on error
        """
        await self._ensure_session()
        try:
            async with self._session.post(url, json=payload, ssl=self.verify_ssl) as resp:
                if resp.status in (200, 201):
                    try:
                        return await resp.json()
                    except Exception:
                        logger.error("Response is not JSON for %s", url, exc_info=True)
                        return None

                if resp.status == 400:
                    logger.warning("Validation error (400) on %s payload=%s", url, payload)
                elif resp.status == 401:
                    logger.error("Authentication failed (401): invalid username/password")
                elif resp.status == 403:
                    logger.error("Forbidden (403): not an author/admin")
                elif resp.status == 404:
                    logger.error("Not found (404): module or user does not exist")
                elif resp.status == 422:
                    details = await resp.json(content_type=None)
                    logger.error("Unprocessable Entity (422): %s", details)
                else:
                    logger.error("Unexpected HTTP %s on %s", resp.status, url)

                return None

        except aiohttp.ClientError:
            logger.error("Network/client error while POST %s", url, exc_info=True)
            return None
        except Exception:
            logger.error("Unexpected error while POST %s", url, exc_info=True)
            return None

    async def _license_action(self, module_name: str, user_id: int, action: str) -> Optional[LicenseResponse]:
        """
        Perform a license action (check, grant, revoke) on a module for a user.

        :param module_name: Module name
        :param user_id: User ID
        :param action: Action type ('check', 'grant', 'revoke')
        :return: Parsed license response object or None on failure
        """
        url = self._build_url(module_name, "license")
        payload = {"user_id": user_id, "action": action}
        data = await self._post_json(url, payload)
        if not data:
            return None

        return _parse_license_response(data)

    async def grant_license(self, module: str, user_id: int) -> bool:
        """
        Grant a license to a user for a module.

        :param module: Module name
        :param user_id: User ID
        :return: True if license is active after grant, False otherwise
        """
        status = await self._license_action(module, user_id, "grant")
        return bool(status and status.is_active)

    async def revoke_license(self, module: str, user_id: int) -> bool:
        """
        Revoke a user's license for a module.

        :param module: Module name
        :param user_id: User ID
        :return: True if license is inactive after revoke, False otherwise
        """
        status = await self._license_action(module, user_id, "revoke")
        return bool(status and status.is_active is False)

    async def check_license(self, module: str, user_id: int) -> bool:
        """
        Check if a user's license for a module is active.

        :param module: Module name
        :param user_id: User ID
        :return: True if license is active, False otherwise
        """
        status = await self._license_action(module, user_id, "check")
        return bool(status and status.is_active)

    async def get_license_status(self, module: str, user_id: int) -> Optional[LicenseResponse]:
        """
        Get full license status object for a user and module.

        :param module: Module name
        :param user_id: User ID
        :return: Full license response object or None on error
        """
        return await self._license_action(module, user_id, "check")
