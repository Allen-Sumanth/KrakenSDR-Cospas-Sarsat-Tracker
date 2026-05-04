import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, cpi_size=8192):
        """
        Custom Smart Gate: Holds the previous MUSIC spectrum when squelch is closed.
        """
        gr.sync_block.__init__(
            self,
            name='Squelch-Triggered Vector Gate',
            # Hardcoded 8192 to prevent the GRC AST parser from crashing
            in_sig=[(np.float32, 360), (np.complex64, 8192)],
            out_sig=[(np.float32, 360)]
        )
        # Initialize the baseline floor at -140 dB
        self.held_vector = np.full(360, -140.0, dtype=np.float32)

    def work(self, input_items, output_items):
        doa_input = input_items[0]
        squelch_input = input_items[1]

        for i in range(len(doa_input)):
            current_doa = doa_input[i]
            current_squelch_frame = squelch_input[i]

            # 1. Did the squelch gate open at ALL during this 437ms frame?
            gate_open = np.max(np.abs(current_squelch_frame)) > 0.5

            # 2. Safety Check 1: Ignore frames where MUSIC exploded into NaNs
            if np.isnan(current_doa).any():
                gate_open = False

            # 3. Safety Check 2: The Flatline Trap
            # If the signal is squelched, the 1e-6 DC offset creates a perfectly flat 0.0dB spectrum.
            # A valid peak will have a noise floor below -3.0 dB.
            if np.min(current_doa) > -3.0:
                gate_open = False

            # Output Logic
            if gate_open:
                # Burst detected AND valid peak! Save it to memory.
                self.held_vector = np.copy(current_doa)
            
            # Safely write the held vector into the output buffer
            output_items[0][i][:] = self.held_vector

        return len(output_items[0])
