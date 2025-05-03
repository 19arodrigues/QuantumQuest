import qiskit
from qiskit.quantum_info import Statevector
from math import pi, sin, cos, atan2, degrees

# from qiskit.providers.basic_provider import BasicProvider
# from qiskit_ibm_runtime import QiskitRuntimeService

class QuantumComputer():
    def __init__(self, stateMarkers, ciruitGrid):
        self.markers = stateMarkers.markers
        self.circuitGrid = ciruitGrid
        self.circuit = None
        self.statevector = None
        self.probabilities = []
        # Save an IBM Cloud account.
        # QiskitRuntimeService.save_account(channel="ibm_cloud", token="MY_IBM_CLOUD_API_KEY",
        #                                   instance="ibm-q/open/main")
        # Save an IBM Quantum account.
        # QiskitRuntimeService.save_account(channel="ibm_quantum", token="da9850724d9196d351fcfd209789160a48ab54141ff4d2f01bd107ac1af11735f219898b876cb0a9fd6130accb5bf3845acc4d20c998310446ddb2cf147475b6")
        # service = QiskitRuntimeService()

    def update(self):
        # backend = BasicProvider().get_backend('basic_provider')
        # backend = qiskit.BasicAer.get_backend("statevector_simulator")
        self.circuit = self.circuitGrid.circuit_grid_model.construct_circuit()
        # transpiled_circuit = qiskit.transpile(circuit, backend)
        # statevector = backend.run(transpiled_circuit, shots=100).result().get_statevector()
        self.statevector = Statevector.from_instruction(self.circuit) 

        self.probabilities = []
        for basis_state, amplitude in enumerate(self.statevector):
            # print(f"Re: {amplitude.real}, Im: {amplitude.imag}, Phase Angles: {degrees(atan2(amplitude.imag, amplitude.real))}, Probability: {amplitude.real**2}")
            self.markers[basis_state].image.set_alpha(max(amplitude.real**2*255,50))
            if amplitude <= 0.0001:
                self.markers[basis_state].updateColour((255, 0, 0))
            else:
                self.markers[basis_state].updateColour((255, 255, 255))
            self.probabilities.append(amplitude.real**2 + amplitude.imag**2)
            # print(self.markers[basis_state].image.get_alpha(), end=" ")
        # print()