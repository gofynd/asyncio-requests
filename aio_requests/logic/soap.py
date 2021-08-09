from requests import Session
from zeep import AsyncClient
from zeep.transports import AsyncTransport
import httpx


async def soap_request(url, data, auth, response, timeout):
    """send_soap_request."""
    return ""
    # session = Session()
    # auth = (auth["username"], auth["password"]) if auth else ()
    # httpx_client = httpx.AsyncClient(auth=auth)
    # try:
    #     client = AsyncClient(url, transport=AsyncTransport(client=httpx_client, timeout=timeout))
    #     soap_response = client.service.CreateTransHdr(
    #         storeNo=data.get("storeNo"),
    #         staffID=data.get("staffID"),
    #         receiptNo=data.get("receiptNo"),
    #         itemNo=data.get("itemNo"),
    #         date_=data.get("date_"),
    #         qty_=data.get("qty_"),
    #         netAmt=data.get("netAmt"),
    #         taxAmt=data.get("taxAmt"),
    #         discountAmt=data.get("discountAmt"),
    #         taxGroupCode=data.get("taxGroupCode"),
    #         saleIsReturnSale=data.get("saleIsReturnSale"),
    #         refundReceiptNo=data.get("refundReceiptNo"),
    #         grossAmt=data.get("grossAmt"),
    #         payment_=data.get("payment_"),
    #         webOrderNo=data.get("webOrderNo"),
    #         channelNew=data.get("channelNew"),
    #         bagID=data.get("bagID"),
    #         brand=data.get("brand"),
    #         iGST=data.get("iGST"),
    #         customerMobileNo=data.get("customerMobileNo"),
    #         stateCode=data.get("stateCode"),
    #         customerName=data.get("customerName"),
    #         gender=data.get("gender"),
    #         dateofBirth=data.get("dateofBirth"),
    #         address=data.get("address"),
    #         city=data.get("city"),
    #         pincode=data.get("pincode"),
    #         stateName=data.get("stateName"),
    #         emailId=data.get("emailId"),
    #         shipmentNumber=data.get("shipmentNumber"),
    #         creditNoteNumber=data.get("creditNoteNumber"),
    #         buyerGSTNumber=data.get("buyerGSTNumber"),
    #         tCSAmount=data.get("tCSAmount"),
    #         creditNoteInvoiceURL=data.get("creditNoteInvoiceURL"),
    #         comments=data.get("comments"),
    #         pOPDF=data.get("pOPDF"),
    #         iRNNumber=data.get("iRNNumber"),
    #         qRCode=data.get("qRCode"),
    #     )
    #     response["status_code"], response["text"] = 200, soap_response
    # except Exception as e:
    #     response["status_code"], response["text"] = 500, str(e)
    # response["json"] = parse_data(response["text"])
    # return response
