
#1) Path in which you wish to store all BRENDA queries:
from zeep import Client
import time
import hashlib
import string
import os

END_POINT = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl"


def extract_field(field, last):

    #Construct list of EC numbers, based on the enzymes for which there is
    #data on BRENDA:

    if field == 'METALSIONS':
        ECstring = client.service.getEcNumbersFromMetalsIons(*credentials)

    elif field == 'COFACTOR':
        ECstring = client.service.getEcNumbersFromCofactor(*credentials)

    #Loop that retrieves data from BRENDA and saves it in txt files. Starts
    #from the last EC number queried:
    start = 0
    for ECnumber in ECstring:

        #Detects the starting point (the last EC number queried):
        if not start and (ECnumber == last or last == ''):
            start = 1

        if start:
            #The code will retrieve data for Saccharomyces cerevisiae:
            query = credentials + ('ecNumber*'+ECnumber + '#organism*Saccharomyces cerevisiae',)
            success = 0

            #The try/except block inside the while is to avoid timeout PROXY
            #and encoding errors:
            while success < 10:
                try:
                    file_name = 'EC' + ECnumber + '_' + field
                    print(file_name)

                    if field == 'METALSIONS':
                        data = client.service.getMetalsIons(*query)

                    elif field == 'COFACTOR':
                        data = client.service.getCofactor(*query)

                    print(data)

                    #Once the querie was performed succesfully, the data is
                    #copied in txt files:
                    if data:
                        fid = open(file_name + '.txt', 'w')
                        fid.write(data.decode('ascii', 'ignore'))
                        fid.close()

                    success = 10

                except:
                    #Let the server cool of for a bit. If after 10 times it
                    #still fails, the query is discarded:
                    time.sleep(1)
                    success += 1


def brenda(email, password, last_field='', last_EC='', output_path=''):

    prev_path = os.getcwd()
    os.chdir(output_path)
    endpointURL = END_POINT
    client = Client(endpointURL)
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    credentials = (email, password)
    #Information to retrieve.
    fields = ['METALSIONS', 'COFACTOR']

    #Loop that retrieves all fields. Starts by the last one queried:
    start = 0
    for field in fields:
        if not start and (field == last_field or last_field == ''):
            start = 1
        if start:
            extract_field(field, last_EC)

    os.chdir(prev_path)
