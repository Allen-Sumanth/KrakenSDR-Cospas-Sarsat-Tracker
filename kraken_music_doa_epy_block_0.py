"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, mode='map_squelch', threshold=0.1):
        """
        mode: 'map_squelch' outputs zeros between bursts so the heatmap doesn't track false movement.
              'compass_hold' persists the last burst indefinitely for visual UI dials.
        """
        gr.sync_block.__init__(
            self,
            name='Smart Vector Gate',
            in_sig=[(np.float32, 360)],
            out_sig=[(np.float32, 360)]
        )
        self.mode = mode 
        self.threshold = threshold
        self.held_vector = np.zeros(360, dtype=np.float32)

    def work(self, input_items, output_items):
        for i in range(len(input_items[0])):
            current_vector = input_items[0][i]

            # 1. Catch the MUSIC algorithm Divide-by-Zero (NaN) explosion
            if np.isnan(current_vector).any():
                is_valid = False
            # 2. Check if the vector contains a strong, valid MUSIC peak
            elif np.max(current_vector) > self.threshold:
                is_valid = True
                self.held_vector = np.copy(current_vector) # Save it to memory
            else:
                is_valid = False

            # Output Logic
            if self.mode == 'compass_hold':
                # Continously push the last known heading (Dangerous if driving!)
                output_items[0][i] = self.held_vector
            else:
                # 'map_squelch' - Push valid burst, otherwise output strict zeros
                if is_valid:
                    output_items[0][i] = current_vector
                else:
                    output_items[0][i] = np.zeros(360, dtype=np.float32)

        return len(output_items[0])
