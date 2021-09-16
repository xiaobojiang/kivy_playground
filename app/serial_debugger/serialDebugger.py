from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

import os
import enum

class SerialEncoding(enum.Enum):
    ASCII = 1
    HEX   = 2

class Indicator(Widget):
    color = ListProperty([1,0,0,1])
    pass

class SerialSetting():
    port_opened = False
    stop_bits = 1
    data_bits = 8
    checksum_bits = 0
    baud_rate = 9600
    recv_encoding = SerialEncoding.ASCII
    send_encoding = SerialEncoding.ASCII
    append_linend_send = False

    def __init__(self):
        pass

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

class Root(FloatLayout):
    console_text = ObjectProperty(None)
    send_text = ObjectProperty(None)
    id_baudrate = ObjectProperty(None)
    id_switch_serial = ObjectProperty(None)
    id_indicator = ObjectProperty(None)
    id_recv_encode = ObjectProperty(None)
    id_append_linend_send = ObjectProperty(None)

    serial_setting = SerialSetting()

    def on_recvencode_change(self, value):
        self.console_text.text += 'receive encoding: {}\n'.format(value)
        if value == 'ASCII':
            self.serial_setting.recv_encoding = SerialEncoding.ASCII
        else:
            self.serial_setting.recv_encoding = SerialEncoding.HEX
        #self.console_text.text += '{}\n'.format(self.id_recv_encode.state == 'down')

    def on_sendencode_change(self, value):
        self.console_text.text += 'send encoding: {}\n'.format(value)
        if value == 'ASCII':
            self.serial_setting.send_encoding = SerialEncoding.ASCII
            try:
                self.send_text.text = HexToByte(self.send_text.text)
            except ValueError:
                self.console_text.text += 'Wrong hex data format in send area, cannot transfer to ASCII\n'
                self.send_text.text = ''
        else:
            self.serial_setting.send_encoding = SerialEncoding.HEX
            #make send area into hex string
            self.send_text.text = ByteToHex(self.send_text.text)


        

    def on_commport_change(self, value):
        self.console_text.text += 'comm port: {} \n'.format(value)

    def on_baudrate_change(self, value):
        self.console_text.text += 'baudrate: {} \n'.format(value)

    def on_databit_change(self, value):
        self.console_text.text += 'data bit: {} \n'.format(value)

    def on_stopbit_change(self, value):
        self.console_text.text += 'stop bit: {} \n'.format(value)

    def on_checksum_change(self, value):
        self.console_text.text += 'check sum: {} \n'.format(value)

    def switch_serial(self, value):
        if value == 'Open':
            self.id_switch_serial.text = 'Close'
            self.id_indicator.color = [0,1,0,1]
        else:
            self.id_switch_serial.text = 'Open'
            self.id_indicator.color = [1,0,0,1]

    def clear_recvdata(self):
        self.console_text.text = ''

    def clear_senddata(self):
        self.send_text.text = ''

    def send_data(self):
        if not self.serial_setting.port_opened:
            self.console_text.text += 'Port not opened yet, please select and click Open.\n'
        
    def on_append_linend_send_change(self, value):
        self.console_text.text += 'checkbox: {}\n'.format(value)
        self.serial_setting.append_linend_send = value



class SerialDebuggerApp(App):
    def build(self):
        self.icon = 'icon.png'


Factory.register('Root', cls=Root)

if __name__ == '__main__':
    SerialDebuggerApp().run()