#!/usr/bin/env python

import json

import requests
import xmltodict


class FedExServices:
    """This class wraps FedEx's API, using HTTP POST requests to send SOAP envelopes."""

    def __init__(
            self,
            web_service_url: str,
            key: str,
            password: str,
            account_number: str,
            meter_number: str
    ):
        self.web_service_url = web_service_url
        self.__key: str = key
        self.__password: str = password
        self.__account_number: str = account_number
        self.__meter_number: str = meter_number

    def _make_request(
            self,
            soap_envelope: str,
            method: str = 'post'
    ) -> str:
        args = {
            'method': method,
            'url': self.web_service_url,
            'data': soap_envelope,
            'headers': {'Content-Type': 'text/xml;charset=utf-8'}
        }

        response = requests.request(**args)
        response.raise_for_status()
        return response.content.decode()

    def track(
            self,
            tracking_number: str
    ):
        """Get tracking details for a tracking number"""

        soap_envelope = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v19="http://fedex.com/ws/track/v19">
            <soapenv:Header/>
            <soapenv:Body>
                <v19:TrackRequest>
                    <v19:WebAuthenticationDetail>
                        <v19:ParentCredential>
                            <v19:Key>{self.__key}</v19:Key>
                            <v19:Password>{self.__password}</v19:Password>
                        </v19:ParentCredential>
                        <v19:UserCredential>
                            <v19:Key>{self.__key}</v19:Key>
                            <v19:Password>{self.__password}</v19:Password>
                        </v19:UserCredential>
                    </v19:WebAuthenticationDetail>
                    <v19:ClientDetail>
                        <v19:AccountNumber>{self.__account_number}</v19:AccountNumber>
                        <v19:MeterNumber>{self.__meter_number}</v19:MeterNumber>
                    </v19:ClientDetail>
                    <v19:TransactionDetail>
                        <v19:CustomerTransactionId>Track By Number_v19</v19:CustomerTransactionId>
                        <v19:Localization>
                            <v19:LanguageCode>EN</v19:LanguageCode>
                            <v19:LocaleCode>US</v19:LocaleCode>
                        </v19:Localization>
                    </v19:TransactionDetail>
                    <v19:Version>
                        <v19:ServiceId>trck</v19:ServiceId>
                        <v19:Major>19</v19:Major>
                        <v19:Intermediate>0</v19:Intermediate>
                        <v19:Minor>0</v19:Minor>
                    </v19:Version>
                    <v19:SelectionDetails>
                        <v19:CarrierCode>FDXE</v19:CarrierCode>
                        <v19:PackageIdentifier>
                            <v19:Type>TRACKING_NUMBER_OR_DOORTAG</v19:Type>
                            <v19:Value>{tracking_number}</v19:Value>
                        </v19:PackageIdentifier>
                        <v19:ShipmentAccountNumber/>
                        <v19:SecureSpodAccount/>
                        <v19:Destination>
                            <v19:GeographicCoordinates>rates evertitque aequora</v19:GeographicCoordinates>
                        </v19:Destination>
                    </v19:SelectionDetails>
                </v19:TrackRequest>
            </soapenv:Body>
        </soapenv:Envelope>
        """

        content = self._make_request(soap_envelope=soap_envelope)
        data = xmltodict.parse(content, dict_constructor=dict)

        headless_data = data['SOAP-ENV:Envelope']['SOAP-ENV:Body']['TrackReply']
        headless_data['_original'] = content

        return headless_data


def _web_track(tracking_number):
    """Finicky ripoff of JSON tracking method used on FedEx.com"""
    data = {
        'data': json.dumps({
            'TrackPackagesRequest': {
                'appType': 'wtrk',
                'uniqueKey': '',
                'processingParameters': {
                    'anonymousTransaction': True,
                    'clientId': 'WTRK',
                    'returnDetailedErrors': True,
                    'returnLocalizedDateTime': False
                },
                'trackingInfoList': [{
                    'trackNumberInfo': {
                        'trackingNumber': tracking_number,
                        'trackingQualifier': '',
                        'trackingCarrier': ''
                    }
                }]
            }
        }),
        'action': 'trackpackages',
        'locale': 'en_US',
        'format': 'json',
        'version': 99
    }

    response = requests.post('https://www.fedex.com/trackingCal/track', data=data)

    return response.json()
