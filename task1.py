import random

def check_pot_value(value, profile):
    
    # Define ranges based on profile
    if profile == 1:
        min_val, max_val = 123, 321
    elif profile == 2:
        min_val, max_val = 734, 801
    elif profile == 3:
        min_val, max_val = 402, 530
    else:
        print("Invalid profile!")
        return 0

    # Generate target inside selected range
    # target = random.randint(min_val, max_val)
    # gap = 5

    #print(f"Profile: {profile}, Target: 820-1020, Value: {value}")

    if min_val<= value <= max_val:
        return 1
    else:
        return 0