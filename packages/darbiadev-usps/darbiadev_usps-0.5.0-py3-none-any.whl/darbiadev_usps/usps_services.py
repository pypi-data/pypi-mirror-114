#!/usr/bin/env python

import requests
import xmltodict


class USPSServices:
    """A class wrapping USPS' API.

    This class wraps USPS' API.
    """

    def __init__(
            self,
            base_url: str,
            user_id: str,
            password: str,
    ):
        self.base_url = base_url
        self.__user_id: str = user_id
        self.__password: str = password

    def _make_request(
            self,
            params: dict[str, str],
            method: str = 'post'
    ) -> str:
        args = {
            'method': method,
            'url': self.base_url,
            'params': params
        }

        response = requests.request(**args)
        response.raise_for_status()
        return response.content.decode()

    def track(
            self,
            tracking_number: str
    ) -> dict:
        """Get tracking details for a tracking number"""
        if not isinstance(tracking_number, str):
            raise ValueError('tracking_number must be a string')

        track_xml = f"""
            <?xml version="1.0" encoding="UTF-8" ?>
            <TrackRequest USERID="{self.__user_id}">
                <TrackID ID="{tracking_number}"></TrackID>
            </TrackRequest>
            """

        content = self._make_request(params={'API': 'TrackV2', 'xml': track_xml})
        data = xmltodict.parse(content, dict_constructor=dict)

        return data
