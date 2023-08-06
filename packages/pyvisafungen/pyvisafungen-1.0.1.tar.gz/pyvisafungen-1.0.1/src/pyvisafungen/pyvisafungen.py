import pyvisa

class Keysightfungen:
    
    def initialize(lan_ip):
        rm = pyvisa.ResourceManager('ktvisa32')
        inst=rm.open_resource(lan_ip)
        inst.timeout=25000
        inst.clear()
        inst.write('*RST;*CLS;*OPC?')
        inst.write('SOUR1:DATA:VOL:CLE')
        return inst
    
    def out_load(Instrument,channel,load):
        Instrument.write("OUTP{:d}:LOAD {:d}".format(channel,load)) 
        
    def out_load_HZ(Instrument,channel):
        Instrument.write("OUTP{:d}:LOAD INF".format(channel)) 
   
    def output(Instrument,channel,ONOFF):
        Instrument.write("OUTP{:d} {:s}".format(channel,str(ONOFF)))
    
    def set_sin(Instrument,channel,freq,amp,ampunit):
        Instrument.write("SOUR{:d}:FUNC {:s}".format(channel,"SIN"))
        Instrument.write("SOUR{:d}:FREQ {:f}".format(channel,freq))
        Instrument.write("SOUR{:d}:VOLT {:f} {:s}".format(channel,amp,ampunit))    
            
    def create_arb(Instrument,channel,ARBname,ARBdata):
        Instrument.write("FORM:BORD SWAP")
        
        strarg = ':SOUR{:d}:DATA:ARB {:s},'.format(channel,ARBname)
        
        Instrument.write_binary_values(strarg,ARBdata, datatype = 'f', is_big_endian = False )
         
    def set_arb(Instrument,channel,ARBname,samplerate,amp,offset,ampunit): 
        Instrument.write("SOUR{:d}:VOLT:UNIT VPP".format(channel)) 
        Instrument.write("SOUR{:d}:FREQ:MODE CW".format(channel))
        Instrument.write("SOUR{:d}:FUNC ARB".format(channel)) 
        Instrument.write("SOUR{:d}:FUNC:ARB {:s}".format(channel,ARBname))
        Instrument.write("SOUR{:d}:FUNC:ARB:SRAT {:f}".format(channel,samplerate))   ## :g 自动切换 e
        Instrument.write("SOUR{:d}:VOLT {:f} {:s}".format(channel,amp,ampunit))
        Instrument.write("SOUR{:d}:VOLT:OFFS {:f}".format(channel,offset))
    
    def set_burst_trig(Instrument,channel,NCycle,TrigSlope,BurstOn):
        Instrument.write("SOUR{:d}:BURS:MODE TRIG".format(channel))  ## TRIG | GAT
        Instrument.write("SOUR{:d}:BURS:NCYC {:d}".format(channel,NCycle)) 
        Instrument.write("TRIG{:d}:SOUR {:s}".format(channel,"EXT")) 
        Instrument.write("TRIG{:d}:SLOP {:s}".format(channel,TrigSlope)) ##POS | NEG
        Instrument.write("SOUR{:d}:BURS:STAT {:s}".format(channel,BurstOn))
 
    def set_burst_gate(Instrument,channel,BurstGatePol,BurstOn):
        Instrument.write("SOUR{:d}:BURS:MODE GAT".format(channel,BurstMode))  ## TRIG | GAT
        Instrument.write("SOUR{:d}:BURS:GATE:POL {:s}".format(channel,BurstGatePol)) ## NORM | INV
        Instrument.write("SOUR{:d}:BURS:STAT {:s}".format(channel,BurstOn))
    
    def set_burst_phase(Instrument,channel,BurstPhase):
        Instrument.write("UNIT:ANGLE DEG")
        Instrument.write("SOUR{:d}:BURS:PHAS {:d}".format(channel,BurstPhase))
    
    def set_mod_amp(Instrument,channel,AMDepth,ModOn):
        Instrument.write("SOUR{:d}:AM:DSSC {:s}".format(channel,"OFF")) # Double Sideband Suppressed Carrier (ON) or AM modulated carrier with sidebands (OFF).
        Instrument.write("SOUR{:d}:AM:SOUR {:s}".format(channel,"EXT"))
        Instrument.write("SOUR{:d}:AM:DEPT {:d}".format(channel,AMDepth))
        Instrument.write("SOUR{:d}:AM:STAT {:s}".format(channel,ModOn))
    
    def set_mod_fm(Instrument,channel,FMDev,ModOn):
        Instrument.write("SOUR{:d}:FM:SOUR {:s}".format(channel,"EXT"))
        Instrument.write("SOUR{:d}:FM:DEV {:d}".format(channel,FMDev))
        Instrument.write("SOUR{:d}:FM:STAT {:s}".format(channel,ModOn))
    
    def set_fsk(Instrument,channel,FSKFreq,ModOn):
        Instrument.write("SOUR{:d}:FSK:SOUR {:s}".format(channel,"EXT"))
        Instrument.write("SOUR{:d}:FSK:FREQ {:d}".format(channel,FSKFreq)) ## in unit of Hz
        Instrument.write("SOUR{:d}:FSK:STAT {:s}".format(channel,ModOn))   


class RIGOLfungen:
    def initialize(lan_ip):
        rmrigol = pyvisa.ResourceManager('ktvisa32')
        inst=rmrigol.open_resource(lan_ip)
        inst.timeout=25000
        inst.clear()
        inst.write('*RST')
        return inst
    
    def out_load(Instrument,channel,load):
        Instrument.write("OUTP{:d}:LOAD {:d}".format(channel,load)) 
        
    def out_load_HZ(Instrument,channel):
        Instrument.write("OUTP{:d}:LOAD INF".format(channel)) 
        
        
    def set_sin(Instrument,channel,freq,amp,ampunit):
        Instrument.write("SOUR{:d}:FUNC {:s}".format(channel,"SIN"))  ##SIN | DC | SQUare | RAMP | USER
        Instrument.write("SOUR{:d}:FREQ {:f}".format(channel,freq)) ## in unit of Hz
        
        Instrument.write("SOUR{:d}:VOLT {:f}".format(channel,amp)) 
        Instrument.write("SOUR{:d}:VOLT:UNIT {:s}".format(channel,ampunit)) # VPP|VRMS|DBM
            
    def set_mod_amp(Instrument,channel,AMDepth,ModOn):
        Instrument.write("SOUR{:d}:MOD:TYP {:s}".format(channel,"AM"))
        Instrument.write("SOUR{:d}:MOD:AM:DEPT {:d}".format(channel,AMDepth))
        Instrument.write("SOUR{:d}:MOD:AM:SOUR {:s}".format(channel,"EXT"))
        Instrument.write("SOUR{:d}:MOD:STAT {:s}".format(channel,ModOn))

    def set_mod_fm(Instrument,channel,FMDev,ModOn):
        Instrument.write("SOUR{:d}:MOD:TYP {:s}".format(channel,"FM"))
        Instrument.write("SOUR{:d}:MOD:FM:DEV {:d}".format(channel,FMDev)) ## in unit of Hz
        Instrument.write("SOUR{:d}:MOD:FM:SOUR {:s}".format(channel,"EXT"))
        Instrument.write("SOUR{:d}:MOD:STAT {:s}".format(channel,ModOn))

    def set_fsk(Instrument,channel,FSKFreq,FSKPOLarity,ModOn):
        Instrument.write("SOUR{:d}:MOD:TYP {:s}".format(channel,"FSK"))
        Instrument.write("SOUR{:d}:MOD:FSK:FREQ {:d}".format(channel,FSKFreq)) ## in unit of Hz
        Instrument.write("SOUR{:d}:MOD:FSK:POL {:s}".format(channel,FSKPOLarity)) ## POS | NEG
        Instrument.write("SOUR{:d}:MOD:FSK:SOUR {:s}".format(channel,"EXT"))
        Instrument.write("SOUR{:d}:MOD:STAT {:s}".format(channel,ModOn))
        
    def set_burst_trig(Instrument,channel,NCycle,TrigSlope,BurstOn):
        Instrument.write("SOUR{:d}:BURS:MODE TRIG".format(channel))  ## TRIG | GAT
        Instrument.write("SOUR{:d}:BURS:NCYC {:d}".format(channel,NCycle)) 
        Instrument.write("SOUR{:d}:BURS:TRIG:SOUR {:s}".format(channel,"EXT")) ##INT | EXT| MAN
        Instrument.write("SOUR{:d}:BURS:TRIG:SLOP {:s}".format(channel,TrigSlope)) ## POS | NEG
        Instrument.write("SOUR{:d}:BURS:STAT {:s}".format(channel,BurstOn)) 
    
    def set_burst_phase(Instrument,channel,BurstPhase):
        Instrument.write("SOUR{:d}:BURS:PHAS {:d}".format(channel,BurstPhase))
    
    def set_burst_gate(Instrument,channel,BurstGatePol,BurstOn):
        Instrument.write("SOUR{:d}:BURS:MODE GAT".format(channel))  ## TRIG | GAT
        Instrument.write("SOUR{:d}:BURS:GATE:POL {:s}".format(channel,BurstGatePol)) ## NORM | INV
        Instrument.write("SOUR{:d}:BURS:STAT {:s}".format(channel,BurstOn)) 
        
    def output(Instrument,channel,ONOFF):
        Instrument.write("OUTP{:d} {:s}".format(channel,str(ONOFF)))        