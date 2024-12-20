from cryptography.fernet import Fernet

def generate_key():
    """
    Generate a new Fernet key and save it to a file.
    """
    # Generate the key
    key = Fernet.generate_key()

    # Save the key to a file
    with open("key.key", "wb") as key_file:
        key_file.write(key)

    print("Key generated and saved to 'key.key'")

def load_key():
    """
    Load the Fernet key from the file.
    """
    try:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
        print("Key loaded successfully.")
        return key
    except FileNotFoundError:
        print("Key file not found. Please generate a key first.")
        return None

if __name__ == "__main__":
    print("1. Generate a new key")
    print("2. Load the existing key")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        generate_key()
    elif choice == "2":
        key = load_key()
        if key:
            print(f"Loaded Key: {key.decode()}")
    else:
        print("Invalid choice. Please run the script again.")
