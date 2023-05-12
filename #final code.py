

import time
import board
import RPi.GPIO as GPIO
import time
from adafruit_apds9960.apds9960 import APDS9960
import digitalio

## Airtable stuff

import requests

# # step to index
Smoothie1Dict = {
    1: 0,
    2: 5,
    3: 1,
    4: 6,
    5: 9,
    6: 3,
    7: 10,
    8: 2,
    9: 4,
    10: 7
}

Smoothie2Dict = {
    1: 9,
    2: 3,
    3: 1,
    4: 7,
    5: 6,
    6: 8,
    7: 5,
    8: 0,
    9: 2,
    10: 4
}

# this is information for pushing data to the airtable
AIRTABLE_API_KEY = 'keyKf7fEzdNw4S7qi'
AIRTABLE_BASE_ID = 'appxFSx1vodDWljqe'
SMOOTHIE1 = 'Smoothie1Tasks'
SMOOTHIE2 = 'Smoothie2Tasks'

# pulling info for Smoothie 1
URLSmoothie1 = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{SMOOTHIE1}?api_key={AIRTABLE_API_KEY}'
response1 = requests.get(url=URLSmoothie1, params={})
data1 = response1.json()

# pulling info for Smoothie 2 
URLSmoothie2 = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{SMOOTHIE2}?api_key={AIRTABLE_API_KEY}'
response2 = requests.get(url=URLSmoothie2, params={})
data2 = response2.json()

# updating current order info 
currID = 'recBNdKxX9ccyOdSf'
currEndpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Current_Order/{currID}'

# pull current order info 
currURL = 'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Current_Order?api_key={AIRTABLE_API_KEY}'
response2 = requests.get(url = currURL, params = {})
dataCurr = response2.json()


# python request headers
headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}
##

## Comms id code

# smoothie 1 and 2
dropOffProcessingS1ID = 'recK4TPYcr89XiKRJ'
dropOffProcessingS1Endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{SMOOTHIE1}/{dropOffProcessingS1ID}'
dropOffProcessingS2ID = 'reckso7rzDIYQFz3W'
dropOffProcessingS2Endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{SMOOTHIE2}/{dropOffProcessingS2ID}'

##### PROCESSING ######

# smoothie 1 and 2 
pickUpProcessingS1ID = 'recm0NkjJTLlbpVyx'
pickUpProcessingS1Endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{SMOOTHIE1}/{pickUpProcessingS1ID}'
pickUpProcessingS2ID = 'recPsmAcRHjjwYbZq'
pickUpProcessingS2Endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{SMOOTHIE2}/{dropOffProcessingS2ID}'

# smoothie 1 and 2 
strawberryS1ID = 'recrQSMlTC3rVhQVM'
strawberryS1Endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{SMOOTHIE1}/{strawberryS1ID}' 
strawberryS2ID = 'recgPvp8ooDJ7hIHR'
strawberryS2Endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{SMOOTHIE2}/{strawberryS2ID}'

# smoothie 2 
bananaID = 'recg6PhVTnypcWleC'
bananaEndpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{SMOOTHIE2}/{bananaID}'

## Comm functionss

def smoothieType():
    return dataCurr['records'][0]['fields']['Smoothie Type']

def taskFinished1(index):
    return data1['records'][index]['fields']['Task Finished']

def docked1(index):
    return data1['records'][index]['fields']['Robot Docked']

def ready1(index):
    return data1['records'][index]['fields']['Ready for Robot']

def taskFinished2(index):
    return data2['records'][index]['fields']['Task Finished']

def docked2(index):
    return data2['records'][index]['fields']['Robot Docked']

def ready2(index):
    return data2['records'][index]['fields']['Ready for Robot']

## My processing code

def StrawberrySlicer():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    apds = APDS9960(i2c)
    apds.enable_proximity = True
    GPIO.setmode(GPIO.BCM)

    IN1 = 21    #23
    IN2 = 20    #24

    INslicer1 = 17
    INslicer2 = 27

    INsweeper1 = 24     #21
    INsweeper2 = 23     #20


    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(INslicer1, GPIO.OUT)
    GPIO.setup(INslicer2, GPIO.OUT)
    GPIO.setup(INsweeper1, GPIO.OUT)
    GPIO.setup(INsweeper2, GPIO.OUT)  

    #print(apds.proximity)
        
    start_time = time.time()
    if apds.proximity > 5:  # if distance sensor detects berry
        print("Strawberry detected!")
        end_time = time.time()
        print(end_time)
        time.sleep(.18) #delay to move strawberry into position #.33
        print("moving berry into position")
        
        GPIO.output(IN1, GPIO.LOW)  #stops belt
        GPIO.output(IN2, GPIO.LOW)
        time.sleep(1)

        GPIO.output(INslicer1, GPIO.HIGH)  #slices in
        GPIO.output(INslicer2, GPIO.LOW)
        time.sleep(.31)
        GPIO.output(INslicer1, GPIO.LOW) #slices out
        GPIO.output(INslicer2, GPIO.HIGH)
        time.sleep(.31)
        GPIO.output(INslicer1, GPIO.HIGH)  #slices in
        GPIO.output(INslicer2, GPIO.LOW)
        time.sleep(.31)
        GPIO.output(INslicer1, GPIO.LOW) #slices out
        GPIO.output(INslicer2, GPIO.HIGH)
        time.sleep(.31)
        GPIO.output(INslicer1, GPIO.HIGH)  #slices in
        GPIO.output(INslicer2, GPIO.LOW)
        time.sleep(.31)

        GPIO.output(INslicer1, GPIO.HIGH)  #slices in
        GPIO.output(INslicer2, GPIO.LOW)
        time.sleep(.31)
        GPIO.output(INslicer1, GPIO.LOW) #slices out
        GPIO.output(INslicer2, GPIO.HIGH)
        time.sleep(.31)
        GPIO.output(INslicer1, GPIO.HIGH)  #slices in
        GPIO.output(INslicer2, GPIO.LOW)
        time.sleep(.31)
        GPIO.output(INslicer1, GPIO.LOW) #slices out
        GPIO.output(INslicer2, GPIO.HIGH)
        time.sleep(.31)
        GPIO.output(INslicer1, GPIO.HIGH)  #slices in
        GPIO.output(INslicer2, GPIO.LOW)
        time.sleep(.31)


        GPIO.output(INslicer1, GPIO.LOW)  #stops slicing
        GPIO.output(INslicer2, GPIO.LOW)

        # move Left
        GPIO.output(INsweeper1, GPIO.LOW)
        GPIO.output(INsweeper2, GPIO.HIGH)
        time.sleep(1.6)

        # move stop
        GPIO.output(INsweeper1, GPIO.LOW)
        GPIO.output(INsweeper2, GPIO.LOW)
        time.sleep(1)
        GPIO.output(INsweeper1, GPIO.HIGH)
        GPIO.output(INsweeper2, GPIO.LOW)
        time.sleep(2)
        GPIO.output(INsweeper1, GPIO.LOW)
        GPIO.output(INsweeper2, GPIO.LOW)
        time.sleep(1)
        
        GPIO.output(INslicer1, GPIO.LOW) #slices out
        GPIO.output(INslicer2, GPIO.HIGH)
        time.sleep(.51)
        GPIO.output(INslicer1, GPIO.LOW)  #stops slicing
        GPIO.output(INslicer2, GPIO.LOW)

        GPIO.output(IN1, GPIO.HIGH)
        #print("high")
        GPIO.output(IN2, GPIO.LOW)
        #print("low")
        time.sleep(1) #move conveyor for berry to move out of the way 
        print("moving berry out of the way")
        elapsed_time = end_time - start_time
        elapsed_time += 1.6
        GPIO.output(IN1, GPIO.LOW)   #reverse belt
        GPIO.output(IN2, GPIO.HIGH)
        print(elapsed_time)
        time.sleep(elapsed_time)
        GPIO.output(IN1, GPIO.LOW)  #stops belt
        GPIO.output(IN2, GPIO.LOW)
    else:
        print("No Berry")
        GPIO.output(IN1, GPIO.HIGH)
        #print("high")
        GPIO.output(IN2, GPIO.LOW)
        #print("low")



## strawberry function

def strawbBanana():
    # clearing up some misleading terms, strawberry is meant to be used by 
    # strawberry processing, same for banana. the drop off is for the fork team

    # get smoothie information
    smoothie = smoothieType()
    # strawberry no banana 
    # STAWBERRY AND BANANA 
    if smoothie == 1:
        # docked and ready for drop off  
        if (ready1(6) == 1) and (docked1(6) == 1):
            data = {
                "fields": {
                    "Ready for Robot": 0
                }
            }
            # briefly update airtable for Ready for Robot to be False so two robots are not in the same place 
            r = requests.patch(dropOffProcessingS1Endpoint, json=data, headers=headers)
            # INSERT function for dropping off (strawberries only for this one)
            
            # set Strawberry docked to True as they are being dropped off 
            data = {
                "fields": {
                    "Robot Docked": 1
                }
            }
            r = requests.patch(strawberryS1Endpoint, json=data, headers=headers)

            time.sleep(5)
            # once finished 
            data = {
                "fields": {
                    "Ready for Robot": 1,
                    "Task Finished": 1
                }
            }

            r = requests.patch(dropOffProcessingS1Endpoint, json=data, headers=headers)
        # For processing teams 
        # only strawberries
    
        # if strawberries is docked (incoming strawberries) and pick up is ready 
        if (docked1(9) == 1) and (docked1(8) == 1):
            data = {
                "fields": {
                    "Ready for Robot": 0
                }
            }
            # briefly update airtable for Ready for Robot to be False so two robots are not in the same place 
            r = requests.patch(strawberryS1Endpoint, json=data, headers=headers)
            # INSERT function for strawberry processing
            time.sleep(10)
            data = {
                "fields": {
                    "Ready for Robot": 1,
                    "Task Finished": 1
                }
            }

        r = requests.patch(strawberryS1Endpoint, json=data, headers=headers)
    # if smoothie 2, need both fruits
    if smoothie == 2:
        # docked and ready for robot to start picking up both strawberries and bananas 
        if (ready2(5) == 1) and (docked2(5) == 1):
            data = {
                "fields": {
                    "Ready for Robot": 0
                }
            }
            # briefly update airtable for Ready for Robot to be False so two robots are not in the same place 
            r = requests.patch(pickUpProcessingS2Endpoint, json=data, headers=headers)
            # INSERT function for strawberry and banana pick up 
            

            # set Drop Off Processing to True as strawberries and bananas are dropped off  
            data = {
                "fields": {
                    "Robot Docked": 1
                }
            }
            r = requests.patch(strawberryS2Endpoint, json=data, headers=headers)
            r = requests.patch(bananaEndpoint, json=data, headers=headers)

            time.sleep(5)
            # once finished 
            data = {
                "fields": {
                    "Ready for Robot": 1,
                    "Task Finished": 1
                }
            }

            r = requests.patch(strawberryS2Endpoint, json=data, headers=headers)
            r = requests.patch(bananaEndpoint, json=data, headers=headers)
        # if strawberries is docked (incoming strawberries) and pick up is ready 
        if (docked2(7) == 1) and (docked2(5) == 1):
            data = {
                "fields": {
                    "Ready for Robot": 0
                }
            }
            # briefly update airtable for Ready for Robot to be False so two robots are not in the same place 
            r = requests.patch(strawberryS2Endpoint, json=data, headers=headers)
            # INSERT function for strawberry processing
            StrawberrySlicer()

            time.sleep(10)
            data = {
                "fields": {
                    "Ready for Robot": 1,
                    "Task Finished": 1
                }
            }

            r = requests.patch(strawberryS2Endpoint, json=data, headers=headers)
        # same idea for bananas
        if (docked2(5) == 1 and docked2(6) == 1):
            data = {
                "fields": {
                    "Ready for Robot": 0
                }
            }
            
            r = requests.patch(bananaEndpoint, json=data, headers=headers)
            # INSERT function for banana processing
            time.sleep(10)
            data = {
                "fields": {
                    "Ready for Robot": 1,
                    "Task Finished": 1
                }
            }

            r = requests.patch(bananaEndpoint, json=data, headers=headers)


def main(): 
    for i in range(10):
        print(i)
        print(data2['records'][i]['fields']['Step'])
    return


 
if __name__ == '__main__':
    main()


