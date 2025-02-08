import subprocess
import sys

# Function to calculate the bit range between two hexadecimal values
def calculate_bit_range(start_hex, end_hex):
    # Convert hexadecimal values to decimal numbers
    start_dec = int(start_hex, 16)
    end_dec = int(end_hex, 16)

    # Check if end is less than or equal to start
    if end_dec <= start_dec:
        raise ValueError("END value must be greater than START value")
    
    # Calculate the difference between the two numbers
    diff = end_dec - start_dec
    
    # Calculate the number of bits needed to represent the difference
    bit_range = diff.bit_length()
    
    return bit_range

# Main function to execute the command
def main():
    if len(sys.argv) < 5:
        print("Usage: python3 run_RCKangaroo.py -dp DP [-gpu GPU] [-pubkey PUBKEY -start START -end END]")
        sys.exit(1)

    # Parse parameters
    args = {sys.argv[i]: sys.argv[i + 1] for i in range(1, len(sys.argv), 2) if i + 1 < len(sys.argv)}

    dp = args.get("-dp")
    gpu = args.get("-gpu", None)
    pubkey = args.get("-pubkey", None)
    start_hex = args.get("-start", None)
    end_hex = args.get("-end", None)
    tames = args.get("-tames", None)
    max = args.get("-max", None)
    

    # Validate mandatory parameters
    if not dp or not (14 <= int(dp) <= 60):
        print("Error: -dp parameter is mandatory and must be between 14 and 60.")
        sys.exit(1)

    if pubkey:
        if not start_hex or not end_hex:
            print("Error: -start and -end parameters are mandatory if -pubkey is specified.")
            sys.exit(1)

        # Calculate the bit range
        try:
            bit_range = calculate_bit_range(start_hex, end_hex)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

        if not (32 <= bit_range <= 170):
            print("Error: The calculated -range must be between 32 and 170.")
            sys.exit(1)
    else:
        # Benchmark mode
        bit_range = None

    # Command to execute
    command = ["./rckangaroo", "-dp", dp]

    if gpu:
        command.extend(["-gpu", gpu])
    
    if tames:
        command.extend(["-tames", tames])
        
    if max:
        command.extend(["-max", max])

    if pubkey:
        command.extend([
            "-range", str(bit_range),
            "-start", start_hex,
            "-pubkey", pubkey
        ])

    # Execute the command
    subprocess.run(command)

if __name__ == "__main__":
    main()