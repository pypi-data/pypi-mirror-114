# -*- coding:utf-8 -*-
""" Library for NEXTW ECM-XF Module. """
# !/usr/bin/python
# Python:   3.6.5+
# Platform: Windows/Linux/Raspberry
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Library for NEXTW ECM-XF Module.
# History:  2021-04-21 Wheel Ver:1.0 [Heyn] Initialize
#           2021-04-28 Wheel Ver:1.0 [Heyn] New class ecmxf_pdo_mapping
#           2021-05-13 Wheel Ver:1.1 [Heyn] optimized code.
#           2021-05-31 Wheel Ver:1.1 [Heyn] New add user_init_offset and user_init_rtxpdo, rename init to init_ecmxf.

import time
import struct
import logging

from .ecm_xf import open as open_ecmxf
from .ecm_xf import sdo_read, sdo_write, wkc_error
from .ecm_xf import get_rxpdo_size, get_txpdo_size, rxpdo_clear, txpdo_clear
from .ecm_xf import fifo_init, fifo_enable, fifo_clear
from .ecm_xf import get_rxfifo_size, set_rxfifo_size, get_txfifo_size, set_txfifo_size
from .ecm_xf import user_init_offset, user_init_rtxpdo, init_ecmxf
from .ecm_xf import firmware, slavecount, config_dc, set_mode, get_state, set_state
from .ecm_xf import align_position, cia402_servo_on, sm420_adv_config, dc_stable, show_pdo
from .ecm_xf import reconfig_rxpdo, reconfig_txpdo, reconfig
from .ecm_xf import servo, servo_on, servo_off, mixing, feedback, reset, reboot, close
from .ecm_xf import STATE_NONE, STATE_INIT, STATE_PRE_OP, STATE_SAFE_OP, STATE_OP, STATE_ACK
from .ecm_xf import DATA_DEFAULT_SIZE, ASSIGN_ACTIVATE, FIFO_WR, FIFO_RD
from .ecm_xf import MODE_CSP, MODE_CSV, MODE_CST

class fifo( object ):
    """
        Usage:
        fifo().rx_size = 1     # Set RX FIFO size
        fifo().tx_size = 1     # Set TX FIFO size

        fifo().rx_size         # Get RX FIFO size
        fifo().tx_size         # Get TX FIFO size
    """
    def __init__( self ) -> None:
        super().__init__()

    @property
    def rx_size( self ):
        return get_rxfifo_size()

    @rx_size.setter
    def rx_size( self, value ):
        set_rxfifo_size( value )

    @property
    def tx_size( self ):
        return get_txfifo_size()

    @tx_size.setter
    def tx_size( self, value ):
        set_txfifo_size( value )

    @staticmethod
    def disabled():
        if not fifo_init():
            return False
        return fifo_enable( False )

    @staticmethod
    def enabled( ):
        if not fifo_clear():
            return False
        return fifo_enable( True )

class rx_fifo( object ):
    """
        Usage:
        rx_fifo().size = 1      # Set RX FIFO size
        rx_fifo().size          # Get RX FIFO size
    """ 
    @property
    def size( self ):
        return get_rxfifo_size()
    
    @size.setter
    def size( self, value ):
        set_rxfifo_size( value )

    def __len__( self ):
        return get_rxfifo_size()

class tx_fifo( object ):
    """
        Usage:
        tx_fifo().size = 1      # Set TX FIFO size
        tx_fifo().size          # Get TX FIFO size
    """   
    @property
    def size( self ):
        return get_txfifo_size()
    
    @size.setter
    def size( self, value ):
        set_txfifo_size( value )

    def __len__( self ):
        return get_txfifo_size()

class rx_pdo( object ):
    """
        Usage:
        Get RX FIFO size
        1. len( rx_pdo() )
        2. rx_pdo().size
        Clear RX FIFO buffer
        1. rx_pdo().clear()
    """
    def __init__( self ) -> None:
        super().__init__()

    def __len__( self ):
        return get_rxpdo_size()

    @property
    def size( self ):
        return get_rxpdo_size()

    @staticmethod
    def clear( ):
        return rxpdo_clear()

class tx_pdo( object ):
    """
        Usage:
        Get TX FIFO size
        1. len( tx_pdo() )
        2. tx_pdo().size
        Clear TX FIFO buffer
        1. tx_pdo().clear()
    """
    def __init__( self ) -> None:
        super().__init__()

    def __len__( self ):
        return get_txpdo_size()

    @property
    def size( self ):
        return get_txpdo_size()
    
    @staticmethod
    def clear( ):
        return txpdo_clear()

class sdo( object ):
    """ SDO related operations.
        Usage:
        Write SDO -> sdo( 1, 0x2106, alias='Speed P Gain 1', size=2 ).value = 50
        Read  SDO -> sdo( 1, 0x2106, alias='Speed P Gain 1', size=2 ).value
    """
    def __init__( self, slave=1, index=0, subindex=0, size=1, alias='' ) -> None:
        super().__init__()
        self.alias = alias
        self.slave, self.index, self.subindex, self.size = slave, index, subindex, size

    @property
    def value( self ):
        return sdo_read( slave=self.slave, index=self.index, subindex=self.subindex, size=self.size, timeout=7000000 )

    @value.setter
    def value( self, data:bytes ) -> None:
        sdo_write( slave=self.slave, index=self.index, subindex=self.subindex, size=self.size, data=data, timeout=7000000 )

class ecmxf_pdo_mapping( object ):
    def __init__( self ) -> None:
        super().__init__( )
        self.axis_pdo  = dict( )
        self.__fmt     = { 1 : 'B', 2 : 'H', 4 : 'i' }
        self.map_index = 0x1600
        self.rx_pdo_assign_object = 0x1C12
        self.tx_pdo_assign_object = 0x1C13

    def __len__( self ):
        size = 0
        for item in self.axis_pdo.keys():
            size += self.axis_pdo[item].get( 'size', 0 )
        return size

    def __str__( self ) -> str:
        string = ''
        for item in self.axis_pdo.keys():
            string += '{} = {}\r\n'.format( item, self.axis_pdo[item] )
        return string
    
    def get( self, key:str, name:str, default:int=0 ) -> int:
        assert isinstance( self.axis_pdo, dict ), 'axis_pdo type is not dict!'
        return self.axis_pdo[key].get( name, default )

    def set( self, key:str, value:int ):
        self.axis_pdo[key]['value'] = value

    def keys( self ):
        items = []
        for key in self.axis_pdo.keys():
            if self.axis_pdo[key].get( 'ro', True ):
                items.append( key )
        return items

    def unpack( self, offset:int=0, data:bytes=b'' ) -> bool:
        buffer = data[ offset: ]
        for item in self.axis_pdo.keys():
            offset = self.axis_pdo[item].get( 'offset', 0 )
            size   = self.axis_pdo[item].get( 'size',   0 )
            self.axis_pdo[item]['value'] = struct.unpack( '<{}'.format( self.__fmt[size] ), buffer[offset:offset+size] )[0]
        return True

    def pack( self, slave:int=0, data:list=[] ) -> bytes:
        buffer   = data[:]
        pdo_size = self.__len__()*slave
    
        for item in self.axis_pdo.keys():
            offset = self.axis_pdo[item].get( 'offset', 0 )
            size   = self.axis_pdo[item].get( 'size',   0 )
            value  = self.axis_pdo[item].get( 'value',  0 )
            buffer[ pdo_size+offset : pdo_size+offset+size ] = list( struct.pack( '<{}'.format( self.__fmt[size] ), value ) )
        return buffer

    def reconfig( self ) -> list:
        items = []
        for key in self.axis_pdo.keys():
            items.append( dict( map_index = self.map_index,
                                index     = self.get( key, name='index' ),
                                sub_index = 0,
                                bit_size  = self.get( key, name='size' )*8 ) )
        return items

class ecmxf_library( object ):

    def ecmxf_catch_exception( func ):
        def wrapper( self, *args, **kwargs ):
            try:
                return func( self, *args, **kwargs )
            except BaseException as err:
                logging.error( 'ECMXF EXCEPTION -> FUNCTION({}) ERROR={}'.format( func.__name__, err ) )
                return False
        return wrapper

    def __init__( self, slaves:list, rx_pdo_mapping:list, tx_pdo_mapping:list ) -> None:
        """ Initialization
            COUNT  = 2
            MODES  = [ MODE_CSV, MODE_CSP ]
            
            parameters:
            slaves = [ i for i in range( 0, COUNT ) ]
            rx_pdo_mapping = get_rx_pdo_mapping( MODES )
            tx_pdo_mapping = get_tx_pdo_mapping( MODES )
        """
        super( ecmxf_library, self ).__init__()
        self.__position = []
        self.rx_fifo_size, self.tx_fifo_size = 32, 1
        self.slaves, self.slave_size = slaves, len( slaves )
        self.rx_pdo_mapping, self.tx_pdo_mapping = rx_pdo_mapping, tx_pdo_mapping

    def open( self, dev='/dev/spidev0.0', size=DATA_DEFAULT_SIZE ) -> bool:
        """ Turn on the SPI device and initialize global variables.
            dev  : device name
            size : spi packet size
            
            return : The actual size of the spi packet
        """
        if not open_ecmxf( dev ):
            return False

        self.__rx_pdo_size = [ len( i ) for i in self.rx_pdo_mapping ]
        self.__tx_pdo_size = [ len( i ) for i in self.tx_pdo_mapping ]

        self.__rx_pdo_size_offset = [ sum(self.__rx_pdo_size[:index]) for index in range( len( self.__rx_pdo_size ) ) ]
        self.__tx_pdo_size_offset = [ sum(self.__tx_pdo_size[:index]) for index in range( len( self.__tx_pdo_size ) ) ]

        if not user_init_rtxpdo( slave_size = self.slave_size,
                                 sum_rx_pdo = sum( self.__rx_pdo_size ),
                                 sum_tx_pdo = sum( self.__tx_pdo_size ),
                                 rxpdo_size = self.__rx_pdo_size_offset,
                                 txpdo_size = self.__tx_pdo_size_offset ):
            return False

        if not user_init_offset( slave_size = self.slave_size,
                                 cw_offset  = [ rx.get( key='cw', name='offset', default=0 ) for rx in self.rx_pdo_mapping  ],
                                 tp_offset  = [ rx.get( key='tp', name='offset', default=2 ) for rx in self.rx_pdo_mapping  ],
                                 sw_offset  = [ tx.get( key='sw', name='offset', default=0 ) for tx in self.tx_pdo_mapping  ],
                                 pv_offset  = [ tx.get( key='pv', name='offset', default=2 ) for tx in self.tx_pdo_mapping  ] ):
            return False

        spi_size = init_ecmxf( slave_size=self.slave_size, spi_size=size )
        logging.debug( 'SPI SIZE = {}'.format( spi_size ) )

        return spi_size == size

    def firmware( self ):
        """ Get ECMXF firmware version. """
        return firmware()

    def axis( self ):
        """ Get slave count. """
        return slavecount()

    @ecmxf_catch_exception
    def set_dc( self, ns:int=1000000 ) -> bool:
        """ Set synchronization cycle time ( Unit : Nanosecond )
        """
        return config_dc( dc         = ASSIGN_ACTIVATE,
                          sync0      = ns,
                          sync1      = 0,
                          shift_time = int(ns/2) )

    def set_mode( self, slaves:list, modes:list ) -> bool:
        """ Set servo working mode ( CSP CSV CST )
        """
        return set_mode( slaves=slaves, modes=modes, index=0x6060 )

    def align_position( self, slave:int, homing:bool=False, position:int=0 ) -> list:
        """ Align position
            homeing : True  -> Go homing( zero )
                      False -> Align current servo encoder position
            position: Align position
        """
        self.__position.append( align_position( slave=slave, homing=homing, position=position ) )
        return self.__position
    
    def cia402_servo_on( self, slaves:list, homing:list=[False], position:list=[0] ) -> bool:
        for index, slave in enumerate(slaves):
            self.__position.append( cia402_servo_on( slave=slave, homing=homing[index], position=position[index] ) )
        
        assert tx_pdo().clear(),  'CLEAR TX PDO IS ERROR'
        assert rx_pdo().clear(),  'CLEAR RX PDO IS ERROR'
        assert fifo().enabled( ), 'ENABLED FIFO IS ERROR'
        return self.__position

    def get_state( self, slave:int=0 ):
        """ Get current servo status
            return ( STATE_NONE     = 0x00,
                     STATE_INIT     = 0x01,
                     STATE_PRE_OP   = 0x02,
                     STATE_SAFE_OP  = 0x04,
                     STATE_OP       = 0x08,
                     STATE_ACK      = 0x10 )
        """
        return get_state( slave )

    def set_state( self, state=STATE_PRE_OP, rx_fifo_size=32, tx_fifo_size=1 ) -> bool:
        """ Set current servo status
        """
        if not set_state( state, 5000 ):
            logging.error( 'ECMXF set_state is ERROR.' )
            return False

        if state == STATE_PRE_OP:
            logging.debug( '============' )
            logging.debug( 'PRE-OP STATE' )
            logging.debug( '============' )

            self.rx_fifo_size = rx_fifo_size
            self.tx_fifo_size = tx_fifo_size

            rx_fifo().size = rx_fifo_size       # Set rx fifo size
            tx_fifo().size = tx_fifo_size       # Set tx fifo size

            logging.debug( 'RX FIFO SIZE = {}'.format( rx_fifo().size ) )   # Get rx fifo size
            logging.debug( 'TX FIFO SIZE = {}'.format( tx_fifo().size ) )   # Get tx fifo size

            # Check ECM queue size first
            # TODO

            fifo().disabled()                   # Disabled fifo

            # Get RX and TX PDO size.
            self.show_pdo_size()

            assert wkc_error( 20 ), 'ECMXF SET wkc_error failed'

        if state == STATE_SAFE_OP:
            logging.debug( '=============' )
            logging.debug( 'SAFE-OP STATE' )
            logging.debug( '=============' )
            sm420_adv_config( slaves    = self.slaves,
                              cw_offset = [ rx.get( key='cw', name='offset', default=0 ) for rx in self.rx_pdo_mapping  ],
                              sw_offset = [ tx.get( key='sw', name='offset', default=0 ) for tx in self.tx_pdo_mapping  ] )
        
        if state == STATE_OP:
            logging.debug( '=============' )
            logging.debug( 'OP STATE'      )
            logging.debug( '=============' )
            while True:
                if dc_stable():
                    break
                time.sleep( 1 )
        
        return True

    def show_pdo( self, slaves:list, index=0x1C12 ) -> bool:
        for slave in slaves:
            show_pdo( slave, index )

    def show_pdo_size( self ) -> tuple:
        rx_pdo_size = rx_pdo().size
        tx_pdo_size = tx_pdo().size
        logging.debug( 'RxPDO size = {}'.format( rx_pdo_size ) )  
        logging.debug( 'TxPDO size = {}'.format( tx_pdo_size ) )
        return ( rx_pdo_size, tx_pdo_size )

    @ecmxf_catch_exception
    def reconfig_rx( self, slaves:list, rx_mapping:list ) -> bool:
        for slave in slaves:
            assert reconfig_rxpdo( slaves = [ slave ],
                                   param  = rx_mapping[slave].reconfig() ), 'SLAVE({}) reconfig RX failed'.format( slave )
        
        assert rx_pdo().size == sum( self.__rx_pdo_size ), 'RECONFIG RX_PDO SIZE FAILED'
        return True

    @ecmxf_catch_exception
    def reconfig_tx( self, slaves:list, tx_mapping:list ) -> bool:
        for slave in slaves:
            assert reconfig_txpdo( slaves = [ slave ],
                                   param  = tx_mapping[slave].reconfig() ), 'SLAVE({}) reconfig TX failed'.format( slave )
        assert tx_pdo().size == sum( self.__tx_pdo_size ), 'RECONFIG TX_PDO SIZE FAILED'
        return True

    @ecmxf_catch_exception
    def reconfig( self, slaves:list, rx_mapping:list, tx_mapping:list ) -> bool:
        """ Reconfig rx or tx mapping.
        """
        if ( rx_pdo().size == sum( self.__rx_pdo_size ) ) and ( tx_pdo().size == sum( self.__tx_pdo_size ) ):
            logging.warning( 'SLAVE({}) Already configured, no need to reconfig.'.format( slaves ) )
            return True
        
        for slave in slaves:
            reconfig( slaves = [ slave ],
                      rx     = rx_mapping[slave].reconfig(),
                      tx     = tx_mapping[slave].reconfig() )
        
        assert rx_pdo().size == sum( self.__rx_pdo_size ), 'RECONFIG RX_PDO SIZE FAILED'
        assert tx_pdo().size == sum( self.__tx_pdo_size ), 'RECONFIG TX_PDO SIZE FAILED'

        return True

    def servo( self, slave:int=0, enabled:bool=True ) -> bool:
        """ Servo enable one by one
            
            slave   : Servo index
            enabled : True  = SERVO ON
                      False = SERVO OFF
        """
        return servo( slave=slave, state=enabled )

    @ecmxf_catch_exception
    def servo_ready( self ) -> bool:
        assert tx_pdo().clear(),  'CLEAR TX PDO IS ERROR'
        assert rx_pdo().clear(),  'CLEAR RX PDO IS ERROR'
        assert fifo().enabled( ), 'ENABLED FIFO IS ERROR'
        return True

    def servo_on( self, slaves:list ) -> list:
        assert servo_on( slaves=slaves ), 'SERVO ON ERROR'
        self.servo_ready()
        return self.__position

    def servo_off( self, slaves:list ) -> bool:
        return servo_off( slaves=slaves )

    def __syntax_tx_pdo( self, slaves:list, data:bytes=b'' ) -> list:
        """
            See: /servo/*.py
            return : [ {0: {'vd': 0, 'tv': 17}},
                       {1: {'pv': 0}},
                       {2: {'pv': 0}},
                       {3: {'vd': 0, 'tv': 17}},
                       {4: {'vd': 0, 'tv': 18}},
                       {5: {'pv': 0}},
                       {6: {'pv': -1}},
                       {7: {'vd': 0, 'tv': 5}} ]
        """
        items = []
        if len( data ):
            for slave in slaves:
                self.tx_pdo_mapping[slave].unpack( self.__tx_pdo_size_offset[slave], data )
                value = dict()
                for key in self.tx_pdo_mapping[slave].keys():
                    value[key] = self.tx_pdo_mapping[slave].get( key, 'value' )
                items.append( { slave:value } )
        return items

    def mixing( self, slaves:list, values:list, syntax=True, op=FIFO_WR ) -> dict:
        """
            param : { values      : 0,  # Bytes
                      rx_fifo_cnt : 0,
                      crc_err_cnt : 0,
                      wkc_err_cnt : 0,
                      is_alive    : 1   # 0 ro 1
                    }
        """
        param = mixing( slaves=slaves, values=values, op=op, fifo_max=self.rx_fifo_size )
        
        param.pop( 'rx_fifo_cnt' )
        param.pop( 'crc_err_cnt' )
        param.pop( 'wkc_err_cnt' )

        data = param.pop( 'values', b'' )

        return dict( data=self.__syntax_tx_pdo( slaves=slaves, data=data ), param=param ) if syntax else dict( data=data, param=param )

    def feedback( self, slaves:list ) -> list:
        """ Get SERVO feedback values.
        """
        return self.__syntax_tx_pdo( slaves=slaves, data=feedback( slaves=slaves ) )

    @staticmethod
    def reset( ) -> bool:
        """ Hardware reset """
        return reset()

    @staticmethod
    def reboot( ) -> bool:
        """ Software reset """
        return reboot()

    @staticmethod
    def close( ) -> None:
        """ CLOSE ECMXF """
        result = set_state( STATE_PRE_OP, 2000 )
        logging.debug( 'ECMXF STATE -> STATE_PRE_OP ({})'.format( result ) )
        result = reset()
        logging.debug( 'ECMXF RESET : {}'.format( result ) )
        result = close()
        logging.debug( 'ECMXF CLOSE : {}'.format( result ) )
