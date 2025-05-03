# from qiskit import QuantumCircuit
# from qiskit.quantum_info import Statevector
# from os import walk, listdir
# import re
# from pathlib import Path


# circuit = QuantumCircuit(3)

# statevector = Statevector.from_instruction(circuit)
# print(circuit)
# print(statevector)

# for i, amplitude in enumerate(statevector):
#         print(amplitude.real)
# path = "assets/levels/level0/plant"
# surface_list = []
# for X,XX,images in listdir(path):
#         for image in images:
                
#             if '.png' in image:
#                 complete_path = path + '/' + image
#                 print(complete_path)
#                 # image_surf = pygame.image.load(complete_path).convert_alpha()



# folder_path = Path(path)
# file_names = [file.name for file in folder_path.iterdir() if file.is_file() and file.name.lower().endswith(".png")]

# # Utility method for sorting files by number
# def extract_number(filename):
#         match = re.search(r'\d+', filename)  # Get tile id
#         return int(match.group()) if match else float('inf')  # Use 'infinity' to deprioritise files with no number

# # Sort using the custom key
# sorted_files = sorted(file_names, key=lambda x: (extract_number(x), x))

# print(len(sorted_files))

for i in range(4):
#     print(f"{i}: {i%2 * (2-i)}")
    print(f"{i}: {((i+1)%2) * (1-i)}")

