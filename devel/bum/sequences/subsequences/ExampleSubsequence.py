from common.devel.bum.sequences.pulse_sequence import pulse_sequence
from labrad.units import WithUnit as U

class example(pulse_sequence):
    
    required_parameters = [
                           ]
    
    def sequence(self):
        print self.parameters['DopplerCooling.duration']
        self.end = self.start + U(5, 'us')
