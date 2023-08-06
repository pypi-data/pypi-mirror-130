def parse_rekognition_response_receipt_text(rekognitionResponse, vendorNameList):
    
    receiptText = dict()

    isVendorName = False
    numTotal = 0
    isAmountTotal = False

    for text in rekognitionResponse['TextDetections']:
        #print( text['Type'] + ' ' + text['DetectedText'].lower() + ' : ' + str(text['Confidence']))

        if numTotal == 1:
            numTotal = 2
        
        if not isVendorName:
            for vendorName in vendorNameList:
                if text['DetectedText'].lower() == vendorName.lower():
                    receiptText['vendorName'] = vendorName
                    isVendorName = True

        if numTotal == 0:
            if text['DetectedText'].lower() == 'total':
                numTotal = 1
        
        if numTotal == 2:
            numTotal = 0
            amountTotal = text['DetectedText'].lower().replace('eur', '')
            if amountTotal.replace('.', '').isnumeric():
                receiptText['amountTotal'] = float(amountTotal)
                isAmountTotal = True
        
        if isVendorName and isAmountTotal:
            break

    return receiptText
