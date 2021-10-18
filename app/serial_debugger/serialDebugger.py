from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.popup import Popup

import os
import enum
import serial
import datetime
from pathlib import Path

from kivy.core.window import Window
Window.size = (1080, 600)
class SerialEncoding(enum.Enum):
    ASCII = 1
    HEX   = 2

class SerialChecksum(enum.Enum):
    Non = 1
    Odd  = 2
    Even = 3

def ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """

    # Uses list comprehension which is a fractionally faster implementation than
    # the alternative, more readable, implementation below
    #
    #    hex = []
    #    for aChar in byteStr:
    #        hex.append( "%02X " % ord( aChar ) )
    #
    #    return ''.join( hex ).strip()

    return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

def HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    # The list comprehension implementation is fractionally slower in this case
    #
    #    hexStr = ''.join( hexStr.split(" ") )
    #    return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
    #                                   for i in range(0, len( hexStr ), 2) ] )

    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )

class Indicator(Widget):
    color = ListProperty([1,0,0,1])
    pass

class SerialPort():
    port_opened = False
    stop_bits = 1
    data_bits = 8
    checksum_bits = SerialChecksum.Non
    baud_rate = 9600
    recv_encoding = SerialEncoding.ASCII
    send_encoding = SerialEncoding.ASCII
    append_linend_send = False
    add_timestamp = False
    select_port = ''
    console_buffer = None
    time_counter = 0
    last_read_counter = 0
    inbuff_number = 0

    def __init__(self, console_buffer, read_timeout=100*60/1000): #default read timeout 100ms
        self._ser = serial.Serial()
        self.console_buffer = console_buffer
        self.read_timeout = read_timeout

    def __repr__(self) -> str:
        return 'port: {port}, stop bit: {stopbit}, data bit: {databit}, \
        checksum: {checksum}, baud rate: {baudrate}, recv encode: {recvencode}, \
        send encode: {sendencode}, append line end: {appendlinend}, opened: {opened}'.format(
            port = self.select_port,
            stopbit = self.stop_bits,
            databit = self.data_bits,
            checksum = self.checksum_bits,
            baudrate = self.baud_rate,
            recvencode = self.recv_encoding,
            sendencode = self.send_encoding,
            appendlinend = self.append_linend_send,
            opened = self.port_opened
        )

    def __str__(self) -> str:
        return self.__repr__()

    def open_port(self):
        self._ser.baudrate = self.baud_rate
        self._ser.port     = self.select_port
        self._ser.bytesize = self.transfer_bytesize(self.data_bits)
        self._ser.stopbits = self.transfer_stopbits(self.stop_bits)
        self._ser.parity   = self.transfer_parity(self.checksum_bits)
        try:
            self._ser.open()
        except serial.serialutil.SerialException:
            self.port_opened = False
            self._ser.close()
            return False
        self.time_counter = 0
        self.last_read_counter = 0
        self.port_opened = self._ser.is_open
        return self._ser.is_open

    def close_port(self):
        self._ser.close()
        self.port_opened = False
        return True

    def transfer_bytesize(self, bytesize):
        if bytesize == 5:
            return serial.FIVEBITS
        elif bytesize == 6:
            return serial.SIXBITS
        elif bytesize == 7:
            return serial.SEVENBITS
        else:
            return serial.EIGHTBITS

    def transfer_stopbits(self, stopbits):
        if stopbits == 1:
            return serial.STOPBITS_ONE
        else:
            return serial.STOPBITS_TWO

    def transfer_parity(self, checksum):
        if checksum == SerialChecksum.Non:
            return serial.PARITY_NONE
        elif checksum == SerialChecksum.Odd:
            return serial.PARITY_ODD
        elif checksum == SerialChecksum.Even:
            return serial.PARITY_EVEN
        else:
            return serial.PARITY_NONE

    def print_read_task(self):
        if self.port_opened:
            #increment at 1ms interval
            self.time_counter += 1
            read_waiting_num = self._ser.in_waiting
            if read_waiting_num > 0:
                if self.inbuff_number != read_waiting_num:
                    #keep counters updated and same
                    self.last_read_counter = self.time_counter
                    self.inbuff_number = read_waiting_num
                else:
                    #counters are same, check timeout condition
                    if self.time_counter - self.last_read_counter >= self.read_timeout:
                        #print all the data in the buff, output is bytes, need decode
                        self.print_encoded_data(self._ser.read(read_waiting_num))
                        #keep counters updated and same
                        self.last_read_counter = self.time_counter
                        #reset the counter
                        self.inbuff_number = 0

    def print_encoded_data(self, data):
        if self.add_timestamp:
            now = datetime.datetime.now()
            self.console_buffer.text += now.strftime("%H:%M:%S.%f")[:-3] + '    ' 
        if self.recv_encoding == SerialEncoding.HEX:
            try:
                encoded_data = ''.join( [ "%02X " % x for x in data ] ).strip()
                self.console_buffer.text += encoded_data 
                self.console_buffer.text += '\n'
            except Exception as e:
                print(e)
                pass
        else: # self.recv_encoding == SerialEncoding.ASCII:            
            if len(data)>0:
                encoded_data = data.decode('utf-8')
                self.console_buffer.text += encoded_data
                if encoded_data[-1] != '\n' and encoded_data[-1] != '\r':
                    self.console_buffer.text += '\n'
    

                        

    def send(self, data):
        if self.port_opened:
            try:
                if self.send_encoding == SerialEncoding.HEX:
                    self._ser.write(HexToByte(data).encode('utf-8'))
                else: #self.send_encoding == SerialEncoding.ASCII:
                    self._ser.write(data.encode('utf-8'))
            except serial.serialutil.SerialTimeoutException:
                self.console_buffer.text += 'write timeout\n'
            except ValueError:
                self.console_buffer.text += 'Wrong hex data format in send area, cannot transfer to ASCII\n'


    
class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    homepath = str(Path.home())


class Root(FloatLayout):
    console_text    = ObjectProperty(None)
    send_text       = ObjectProperty(None)
    id_commport     = ObjectProperty(None)
    id_baudrate     = ObjectProperty(None)
    id_checksum     = ObjectProperty(None)
    id_stopbit      = ObjectProperty(None)
    id_databit      = ObjectProperty(None)
    id_indicator    = ObjectProperty(None)
    id_switch_serial = ObjectProperty(None)
    id_recv_encode  = ObjectProperty(None)
    id_send_encode  = ObjectProperty(None)
    id_append_linend_send = ObjectProperty(None)
    id_add_timestamp = ObjectProperty(None)
    serial_port = None

    serial_port_list = []

    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        self.serial_port = SerialPort(self.console_text)
        self.update_comm_ports()
        self.id_commport.values = self.serial_port_list
        self.id_commport.text = '-' if not self.serial_port_list else  self.serial_port_list[0]
        
    
    def update_comm_ports(self):
        self.serial_port_list = []
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            return None
        if comports:
            com_ports_list = list(comports())
            for port in com_ports_list:
                self.serial_port_list.append(port[0])

    def update_port(self, dt): #dt is the delta time
        #update commport options
        self.update_comm_ports()
        self.id_commport.values = self.serial_port_list

    def update_serialread(self, dt):
        self.serial_port.print_read_task()
        



    def on_recvencode_change(self, value):
        self.console_text.text += 'receive encoding: {}\n'.format(value)
        if value == 'ASCII':
            self.serial_port.recv_encoding = SerialEncoding.ASCII
        else:
            self.serial_port.recv_encoding = SerialEncoding.HEX
        #self.console_text.text += '{}\n'.format(self.id_recv_encode.state == 'down')

    def on_sendencode_change(self, value):
        self.console_text.text += 'send encoding: {}\n'.format(value)
        if value == 'ASCII':
            self.serial_port.send_encoding = SerialEncoding.ASCII
            try:
                self.send_text.text = HexToByte(self.send_text.text)
            except ValueError:
                self.console_text.text += 'Wrong hex data format in send area, cannot transfer to ASCII\n'
                self.send_text.text = ''
        else:
            self.serial_port.send_encoding = SerialEncoding.HEX
            #make send area into hex string
            self.send_text.text = ByteToHex(self.send_text.text)
        

    def on_commport_change(self, value):
        self.console_text.text += 'comm port: {} \n'.format(value)
        self.serial_port.select_port = value

    def on_baudrate_change(self, value):
        self.console_text.text += 'baudrate: {} \n'.format(value)
        self.serial_port.baud_rate = int(value)

    def on_databit_change(self, value):
        self.console_text.text += 'data bit: {} \n'.format(value)
        self.serial_port.data_bits = int(value)

    def on_stopbit_change(self, value):
        self.console_text.text += 'stop bit: {} \n'.format(value)
        self.serial_port.stop_bits = int(value)

    def on_checksum_change(self, value):
        self.console_text.text += 'check sum: {} \n'.format(value)
        if value == 'None':
            self.serial_port.checksum_bits = SerialChecksum.Non
        elif value == 'Odd':
            self.serial_port.checksum_bits = SerialChecksum.Odd
        elif value == 'Even':
            self.serial_port.checksum_bits = SerialChecksum.Even

    def switch_serial(self, value):
        #self.console_text.text += str(self.serial_port)
        if value == 'Open':
            if self.serial_port.open_port():
                self.id_switch_serial.text = 'Close'
                self.id_indicator.color = [0,1,0,1]
                self.id_commport.disabled = True
                self.id_baudrate.disabled = True
                self.id_checksum.disabled = True
                self.id_stopbit.disabled = True
                self.id_databit.disabled = True
            else:
                self.console_text.text += 'Port {} open failed, please check\n'.format(self.serial_port.select_port)

        else:
            self.id_switch_serial.text = 'Open'
            self.id_indicator.color = [1,0,0,1]
            self.id_commport.disabled = False
            self.id_baudrate.disabled = False
            self.id_checksum.disabled = False
            self.id_stopbit.disabled = False
            self.id_databit.disabled = False
            self.serial_port.close_port()


    def clear_recvdata(self):
        self.console_text.text = ''

    def clear_senddata(self):
        self.send_text.text = ''

    def send_data(self):
        if not self.serial_port.port_opened:
            self.console_text.text += 'Port not opened yet, please select and click Open.\n'
        else:
            self.serial_port.send(self.send_text.text)
            

        
    def on_append_linend_send_change(self, value):
        #self.console_text.text += 'apped line end: {}\n'.format(value)
        self.serial_port.append_linend_send = value

    def on_add_timestamp_change(self, value):
        #self.console_text.text += 'add timestamp: {}\n'.format(value)
        self.serial_port.add_timestamp = value

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):        
        self.dismiss_popup()
        with open(os.path.join(path, filename), 'wb') as filewriter:
            filewriter.write(self.console_text.text.encode('utf-8'))
        self.console_text.text += ' - - - - - -  - - - - - - \n'
        self.console_text.text += 'File saved at {}\n'.format(os.path.join(path, filename))
        self.console_text.text += ' - - - - - -  - - - - - - \n'


class SerialDebuggerApp(App):
    def build(self):
        self.icon = 'icon.png'
        root = Root()
        Clock.schedule_interval(root.update_port, 1.0)
        Clock.schedule_interval(root.update_serialread, 1.0/60)
        return root


#Factory.register('Root', cls=Root)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':
    SerialDebuggerApp().run()

    #know issue: does not support chinese