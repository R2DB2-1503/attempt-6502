data = input("Input raw bytes: ")
formatted = ", ".join([f"0x{byte}" for byte in data.split()])
print(formatted)
