# ----------------------------------------------------
# Hamming(7,4) PROJECT
#  May 2021

# We will use the random library to generate random messages
# and introduce errors at random locations.
import random


##################### CHANNEL-ADDED ERROR (1 bit) ######################
def flip_bit(message, location):
    # This will flip the bit at position e-1 (0->1 and 1->0)
    message[location] = 1 - message[location]

    return message


def flip_random_bit(message):
    e = random.randint(1, len(message))
    print("Flipping bit (=introducing error) at location: " + str(e))

    # This will flip the bit at position e-1 (0->1 and 1->0)
    message = flip_bit(message, e - 1)

    return message


# Correct any error in the hamming encoded message
# This function will CHANGE the hamming variable as well
def hamming_correct(hamming):
    error_location = get_all_xor(hamming)
    print('Where did we find an error? ' + str(error_location))

    # If there was an error, correct it by swapping the corresponding bit
    if error_location > 0:
        flip_bit(hamming, error_location - 1)

    return hamming


def hamming_encode(in_str, dl, nb_parity_bits):
    out_str = [0] * (dl + nb_parity_bits)  # initial all zero
    parity_position = {}
    ipower = 0
    idata = 0
    for i in range(dl + nb_parity_bits):
        if (i+1) == (1 << ipower):
            parity_position[ipower] = i  # remember parity position
            ipower += 1
        else:
            out_str[i] = in_str[idata]
            idata += 1
    print('parity_position:', parity_position)

    weight = get_all_xor(out_str)
    need_fix_position = get_bin_factor(weight, nb_parity_bits)
    print(weight, need_fix_position)
    for i, x in enumerate(need_fix_position):
        out_str[parity_position[i]] = x
    return out_str, parity_position


def get_all_xor(in_data):
    answer = 0
    member = []
    for i, x in enumerate(in_data):
        if x:
            answer = answer ^ (i+1)
            member.append(i+1)
    print('in_data:', in_data)
    print('none zero position is:', member)
    return answer


def hamming_decode(in_str, posi):
    answer = []
    for i, x in enumerate(in_str):
        if i not in posi.values():  # skip the parity position
            answer.append(x)
    # answer = [x for i, x in enumerate(in_str) if i not in posi.values()]
    return answer


def get_bin_factor(num, bits):  # get the bin factors, lower is first
    answer = []
    for step in range(bits):
        answer.append(num % 2)
        num = num >> 1
    return answer


# Get parity bits
def find_pb(digits):
    answer = 1
    for iposi in range(1, digits+5):
        x = 1 << iposi
        if x >= (digits + iposi + 1):
            answer = iposi
            break
    return answer


##################### MAIN PROGRAM #####################
# Generate a random string of "0" and "1"

# Change data length here!
data_len = 4
# Change data length here!

para_r = find_pb(data_len)
print('Data length is:', data_len, 'nb_parity_bits is:', para_r)

message = [random.getrandbits(1) for x in range(data_len)]

print("Message: " + str(message))

hamming, parity_posi = hamming_encode(message, data_len, para_r)
print("Encoded hamming message: " + str(hamming))

hamming_with_error = flip_random_bit(hamming)
print("Received hamming message: " + str(hamming_with_error))

corrected_message = hamming_correct(hamming_with_error)
print('Corrected hamming message: ' + str(corrected_message))

decoded_message = hamming_decode(corrected_message, parity_posi)
print('Corrected message: ' + str(decoded_message))
