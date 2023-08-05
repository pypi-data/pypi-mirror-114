# -*- coding:utf-8 -*-
""" ECMXF FOR ELMO """
# !/usr/bin/python
# Python:   3.6.5+
# Platform: Windows/Raspberry
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  ECMXF FOR ELMO.
# Package:  pip install libecm
# History:  2021-05-05 Ver:1.0 [Heyn] Initialization
#           2021-05-24 Ver:1.1 [Heyn] Optimized code

import time
import logging

from libecm import ecmxf
from libecm.ecmxf import ecmxf_library
from libecm.ecmxf import DATA_DEFAULT_SIZE
from libecm.ecmxf import MODE_CSP, MODE_CSV, MODE_CST
from libecm.ecmxf import STATE_INIT, STATE_PRE_OP, STATE_SAFE_OP, STATE_OP

from libecm.plugins.hexinSigmoid        import hexinSigmoid

from libecm.servo.elmo_gold_pdo_mapping import get_rx_pdo_mapping
from libecm.servo.elmo_gold_pdo_mapping import get_tx_pdo_mapping


COUNT  = 8
SLAVES = [ i for i in range( 0, COUNT ) ]
MODES  = [ MODE_CSV, MODE_CSP, MODE_CSP, MODE_CSV, MODE_CSV, MODE_CSP, MODE_CSP, MODE_CSV ]
ENCODER_ACCURACY = 2**17

RX_PDO_MAPPING = get_rx_pdo_mapping( MODES )
TX_PDO_MAPPING = get_tx_pdo_mapping( MODES )

logging.basicConfig( level=logging.INFO )

def main():
    ethercat = ecmxf_library( SLAVES, RX_PDO_MAPPING, TX_PDO_MAPPING )
    ethercat.open( dev='/dev/spidev0.0' )

    if not ethercat.set_dc( 5000000 ):
        logging.error( 'Is servo power on?' )
        return False
    
    print( 'FIRMWARE   = 0x{:02X}'.format( ethercat.firmware() ) )
    print( 'SLAVECOUNT = {}'.format( ethercat.axis( ) ) )

    ethercat.set_state( STATE_PRE_OP )


    print( 'RECONFIG = {}'.format( ethercat.reconfig( slaves     = SLAVES,
                                                      rx_mapping = RX_PDO_MAPPING,
                                                      tx_mapping = TX_PDO_MAPPING ) ) )
    
    # ethercat.show_pdo_size()

    # ethercat.show_pdo( slaves=SLAVES, index=0x1C12 )
    # ethercat.show_pdo( slaves=SLAVES, index=0x1C13 )

    ethercat.set_mode( slaves=SLAVES, modes=MODES )
    
    ethercat.set_state( STATE_SAFE_OP )
    ethercat.servo_off( slaves=SLAVES )

    # ethercat.show_pdo_size()

    for slave in SLAVES:
        print( ethercat.align_position( slave=slave, homing=True, position=0 ) )

    ethercat.set_state( STATE_OP )

    try:
        if not ethercat.servo_on( slaves=SLAVES ):
            ethercat.close()
            return True

        velocity, degree = 0, 0
        
        sigmoid = hexinSigmoid( dsitclock=5 )
        _pos = 0

        while True:
            velocity = input( 'Please input velocity(rps) = ' )
            degree   = input( 'Please input degree = ' )

            velocity = float( velocity ) if velocity != '' else 0
            degree   = float(  degree  ) if  degree  != '' else 0

            # position = 5600*velocity
            # for v in sigmoid.values( cpos = _pos,
            #                          tpos = position,
            #                          ms   = int(abs(_pos-position)/5600*1000),
            #                          flexible = 4,
            #                          inflection=1/2 ):
            #     ethercat.mixing( slaves=SLAVES, values=[ int( v ),
            #                                              int( 0 ),
            #                                              int( 0 ),
            #                                              int( v ),
            #                                              int( v ),
            #                                              int( 0 ),
            #                                              int( 0 ),
            #                                              int( v ) ] )
            #     time.sleep( 0.003 )
            # else:
            #     _pos = sigmoid.actual_position()
            #     print( sigmoid )

            position = int( ENCODER_ACCURACY*450*degree // 360 )
            for pos in sigmoid.values( cpos       = _pos,
                                       tpos       = int(position),
                                       ms         = int(abs(_pos-position)/163840*40),
                                       flexible   = 6,
                                       inflection = 1/2 ):
                ethercat.mixing( slaves=SLAVES, values=[ int( 5600*float(velocity) ),
                                                         int( 0 ),
                                                         int( 0 ),
                                                         int( 5600*float(velocity) ),
                                                         int( 5600*float(velocity) ),
                                                         int( 0 ),
                                                         int( pos ),
                                                         int( 5600*float(velocity) ) ] )
                time.sleep( 0.003 )
            else:
                _pos = sigmoid.actual_position()
                print( sigmoid )

    except KeyboardInterrupt:
        pass
    except BaseException as err:
        logging.error( err )
    
    ethercat.servo_off( slaves=SLAVES )
    ethercat.close( )
    
if __name__ == "__main__":
    main()
