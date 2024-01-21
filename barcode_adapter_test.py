from pycomm3 import CIPDriver, Services
from pycomm3.cip.data_types import UINT, STRING, Struct
from pycomm3.custom_types import FixedSizeString
from pycomm3.logger import configure_default_logger as data_logger
from pycomm3.logger import LOG_VERBOSE
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
                
                
                
    This can be used to do a hard reset - [barcode_scanner.generic_message(sr_1000_service_dict.get("device_reset"), barcode_instance_id, barcode_instance_id, data_type=None, 
                                    name='device reset', connected=True, unconnected_send=False )]
                                    
    TODO: Limit logger file size!!!!
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
#data_logger(level=LOG_VERBOSE, filename=filepath)

sr_1000_service_dict = {
                            "get_attribute_single": b'\x0E',
                            "get_attribute_all": b'\x01',
                            "set_attribute": b'\x10',
                            "start_read": b'\x4B',
                            "stop_read" : b'\x4C',
                            "acquire_read": b'\x55',
                            "reset_error": b'\x53',
                            "clear_reset_and_error_bits": b'\x5A',
                            "get_member": b'\x18',
                            "device_reset" : b'\x05',
                            "read_complete_clear": b'\x5A'
                            
                        }

service = Services()
barcode_scanner = CIPDriver('192.168.1.10')

read_status_attribute_id = b'\x64'
barcode_instance_id = b'\x01'
barcode_assembly_instance_id = b'\x64'
barcode_class_id = b'\x69'
barcode_io_status_attribute = b'\x6C'

barcode_bank_number = bytearray(b'\xFF')

service_data_start = b'\xFF\xFF'
service_data_result = UINT[2].encode([200,0])
data_size = UINT
rest_result=UINT[None]
read_result = STRING
message = FixedSizeString(100, UINT)
barcode_struct = Struct(UINT[None]('FirstWord'), UINT('ReadPass'), UINT('Matching'), UINT('Read_'))
#barcode_struct = Struct(UINT('data size'), UINT('rest data'), UINT('Result Data'))


read_input_count = b'\x74'
result_data_ready_count = b'\x81'

with barcode_scanner:
    #stop_reading = barcode_scanner.generic_message(sr_1000_service_dict.get("stop_read"), barcode_class_id, barcode_instance_id, data_type=None, 
                                    #name='Stop read', connected=True, unconnected_send=False )
    #hard_reset = barcode_scanner.generic_message(sr_1000_service_dict.get("device_reset"), barcode_instance_id, barcode_instance_id, data_type=None, 
                                    #name='device reset', connected=True, unconnected_send=False )
    #sleep(40)
    no_response = barcode_scanner.generic_message(sr_1000_service_dict.get("start_read"), barcode_class_id, barcode_instance_id, request_data=service_data_start, data_type=None, 
                                    name='Start read', connected=True, unconnected_send=False )
    sleep(5)
    

try:
    #while True:
    with barcode_scanner:
        #sleep(0)
        #read_result = barcode_scanner.generic_message(sr_1000_service_dict.get("acquire_read"), barcode_class_id, barcode_instance_id, attribute=service_data_result, data_type=UINT, 
                                        #name='Read Result Code', connected=True, unconnected_send=False )
        #read_input_count_output = barcode_scanner.generic_message(sr_1000_service_dict.get("get_attribute_single"), barcode_class_id, barcode_instance_id, attribute=read_input_count, data_type=rest_result, 
                                        #name='Read input count', connected=True, unconnected_send=False )
        #result_data_ready_count_output = barcode_scanner.generic_message(sr_1000_service_dict.get("get_attribute_single"), barcode_class_id, barcode_instance_id, attribute=result_data_ready_count, data_type=rest_result, 
                                        #name='Result data ready count', connected=True, unconnected_send=False )
        print(f'Sending data request \n\n')
        
        data = barcode_scanner.generic_message(sr_1000_service_dict.get("get_attribute_single"), barcode_class_id, barcode_instance_id, attribute=read_status_attribute_id, data_type=rest_result, 
                                        name='Read results', connected=True, unconnected_send=False )
        
        reset_read = barcode_scanner.generic_message(sr_1000_service_dict.get("read_complete_clear"), barcode_class_id, barcode_instance_id, data_type=None, 
                                                   name='Clear read Data', connected=True, unconnected_send=False)
        
        
        get_data = barcode_scanner.generic_message(sr_1000_service_dict.get("acquire_read"), barcode_class_id, barcode_instance_id, request_data=service_data_result, data_type=STRING, 
                                                   name='Result data', connected=True, unconnected_send=False)
        
        data2 = barcode_scanner.generic_message(sr_1000_service_dict.get("get_attribute_single"), barcode_class_id, barcode_instance_id, attribute=read_status_attribute_id, data_type=rest_result, 
                                        name='Read results', connected=True, unconnected_send=False )
        
        
        #data_two = barcode_scanner.generic_message(sr_1000_service_dict.get("get_attribute_single"), barcode_class_id, barcode_instance_id, attribute=read_status_attribute_id, data_type=UINT, 
                                        #name='Read results', connected=True, unconnected_send=False )
        #result_array = list(data[1])
        #print(f'Barcode Trigger {type(no_response)}\n{no_response}\n')
        
        #print(f'Barcode/start read {type(data)}\n{data}DATA Too {data_two}\nRead input count, counting how many it actually read = {read_input_count_output}\nResult data ready count = {result_data_ready_count_output}')
        read_stat = data2[1][1]
        test = data[1][0]
        get_data = list(get_data)
        barcode = get_data[1]
        
        trimmed_barcode = barcode[3:-4]
        
        print(f'Barcode/start read {type(data)}\nBefore read complete{data} After read complete {data2} {read_stat} type of read stat{type(read_stat)}\n')
        print(f'\n just reading {read_stat} {test}')
        print(f'Service code result attempt = {get_data}\n barcode = {barcode} {type(barcode)} {trimmed_barcode}')
        stop_reading = barcode_scanner.generic_message(sr_1000_service_dict.get("stop_read"), barcode_class_id, barcode_instance_id, data_type=None, 
                                name='Stop read', connected=True, unconnected_send=False )

        #TODO: Convert data from byte string, ensure the lenth is thirteen and starts with a 9
        #TODO: Ensure we get a good read. look at the 1 or zero value

except KeyboardInterrupt:
    
    
    barcode_scanner.close()
    print('Closing communication with SR-1000')
