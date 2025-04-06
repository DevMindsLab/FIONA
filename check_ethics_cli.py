from core_interface.ethics_link import check_ethics_validity

def main():
    valid, message = check_ethics_validity()
    if valid:
        print(f"✅ Ethics core is valid: {message}")
    else:
        print(f"❌ Ethics core failed: {message}")

if __name__ == "__main__":
    main()
