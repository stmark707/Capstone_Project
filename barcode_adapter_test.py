from pycomm3 import CIPDriver, Services
from pycomm3.cip.data_types import WORD, UINT, INT, DWORD, BYTE, LWORD
from pycomm3.custom_types import FixedSizeString
from pycomm3.logger import configure_default_logger as data_logger
from datetime import datetime
from time import sleep

'''
 -Primer topics to look up: EtherNet/IP, EtherNet/IP Adaptor, EtherNet/IP Scanner
        -cyclic communication vs explicit messaging
        -CIP defined UCMM(unconnected) and Class 3(connected) message communication
    -pycomm3 is the communication library used to communicating specifications to and from the keyence network module and amplifiers.
        -pycomm3 docs: https://docs.pycomm3.dev/en/latest/usage/cipdriver.html
        -pycomm3 creates a template for sending CIP (common industrial protocol) explicit messages.
        -pycomm3 does not implement cyclic communication at this time. Only explicit messaging.
    
        -The construction of a generic message is as follows:
            generic_message(Service, Class ID, Instance ID, Attribute ID)
                -Service - The nature of the request action the device needs to complete (Most devices follow CIP specifications)
                    - The nature of a request can be seen as Setting a value or Reading a Value
                -Class ID - Refers to the type of object within the SR-1000 (Provided by Manufacturer: Keyence)
                -Instance ID - Specifies which object the service request is refering to (In this case: 00 = NU-EP1 Module, 01 = Amplifier 1, etc )
                    - (Provided by Manufacturer: Keyence)
                -Attribute ID - Specifies the action to be completed (Provided by Manufacturer: Keyence)
                
                Class ID = b'\x69' [SR AUTOID Reader Object]
'''

time_string = datetime.now()
the_month = time_string.month
the_day = time_string.day
the_year = time_string.year

utc_object = datetime.utcnow()
utc_time = utc_object.time()

title = str(the_month) + '_' + str(the_day) + '_' + str(the_year) + '_' + 'Barcode_logger'
filepath = ('barcode_logger' + '/' + title)


data_logger(filename=filepath)

sr_1000_service_dict = {
                            "get_attribute": b'\x0E',
                            "set_attribute": b'\x10',
                            "start_read": b'\x4B',
                            "stop_read" : b'\x4C',
                            "acquire_read": b'\x55',
                            "reset_error": b'\x53',
                            "clear_reset_and_error_bits": b'\x5A'
    
                        }

service = Services()
barcode_scanner = CIPDriver('192.168.1.10')

read_status_attribute_id = b'\x64'
barcode_instance_id = b'\x01'
barcode_class_id = b'\x69'
service_data_start = bytearray(b'\xFF\x01')
service_data_result = bytearray(b'\xFF\x05')
data_size = UINT
rest_result=UINT
read_result = WORD
message = FixedSizeString(128, LWORD)

try:
    #while True:
    with barcode_scanner:
        data = barcode_scanner.generic_message(sr_1000_service_dict.get("start_read"), barcode_class_id, barcode_instance_id, attribute=None, request_data=service_data_start, data_type=UINT, 
                                        name='Start read', connected=True, unconnected_send=False )
        read_result = barcode_scanner.generic_message(sr_1000_service_dict.get("acquire_read"), barcode_class_id, barcode_instance_id, attribute=read_status_attribute_id, data_type=message, 
                                        name='read result', connected=True, unconnected_send=False )
        #data = barcode_scanner.generic_message(sr_1000_service_dict.get("get_attribute"), barcode_class_id, barcode_instance_id, attribute=read_status_attribute_id, data_type=UINT, 
                                        #name='Read Status', connected=True, unconnected_send=False )
        #result_array = list(data[1])
        print(f'Barcode/start read {type(data)}\n{data}\n{read_result}')
    
except KeyboardInterrupt:
    barcode_scanner.close()
    print('Closing communication with SR-1000')