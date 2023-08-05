from .base import APIEndpoint
import datetime

from mydhl.models.shipmentrequests import *
from mydhl.constants.constants import *

class ShipmentRequestMethods(APIEndpoint):

    def __init__(self, api):
        super(ShipmentRequestMethods, self).__init__(api, "ShipmentRequest")
    

    def shipPackage(self,
        serviceType,
        shipper, 
        recipient,
        packages,
        internationalDetail,
        shipTimestamp=None,
        dropOffType=DropOffType.REGULAR_PICKUP, 
        unitOfMeasurement=Measurement.MEASUREMENT_METRIC,
        paymentInfo=PaymentInfo.PAYMENT_DAP,
        currency='EUR'
    ):

        if not shipTimestamp: 
            shipTime = datetime.datetime.now() + datetime.timedelta(hours=2)
            shipTimestamp = shipTime.strftime('%Y-%m-%dT%H:%M:%S')
        

        data = {
            "ShipmentRequest": {
                "RequestedShipment": {
                    "ShipmentInfo": {
                        "LabelType": "PDF",
                        "DropOffType": dropOffType,
                        "ServiceType": serviceType,
                        "Account": self.api.account,
                        "Currency": currency,
                        "UnitOfMeasurement": unitOfMeasurement,
                    },
                    "ShipTimestamp": "{shipTimestamp} GMT+02:00".format(shipTimestamp=shipTimestamp),
                    "PaymentInfo": paymentInfo,
                    "InternationalDetail" : internationalDetail.getJSON(),
                    "Ship": {
                        "Shipper": shipper.getJSON(),
                        "Recipient": recipient.getJSON()
                    },
                    "Packages": packages.getJSON()
                }
            }
        }

        print(data)

        url = self.endpoint

        status, headers, respJson = self.api.post(url, data)

        print(respJson)
        return ShipmentResponse().parse(respJson['ShipmentResponse'])