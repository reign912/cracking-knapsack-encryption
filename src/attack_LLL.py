import sys
import constants
import liblll
import utility
import ciphering
import deciphering
import attacking
import logger
import time
import ast 
import time
time.sleep(10)

print("Decryption/attacking of encrypted text is about to start.")
time.sleep(2)


def _get_selection(prompt, options):
    choice = input(prompt).upper()
    while not choice or choice[0] not in options:
        choice = input("Please enter one of {}. {}".format('/'.join(options), prompt)).upper()
    return choice[0]


def get_filename():
    """Ask the user for a filename, reprompting for nonempty input.

    Doesn't check that the file exists.
    """
    filename = input("Filename? ")
    while not filename:
        filename = input("Filename? ")
    return filename

def get_input(binary=False):
    """Prompt the user for input data, optionally read as bytes."""
    print("* Input *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        text = input("Enter a string: ").strip().upper()
        while not text:
            text = input("Enter a string: ").strip().upper()
        if binary:
            return bytes(text, encoding='utf8')
        return text
    else:
        filename = get_filename()
        flags = 'r'
        if binary:
            flags += 'b'
        with open(filename, flags) as infile:
            return infile.read()


def set_output(output, binary=False):
    """Write output to a user-specified location."""
    print("* Output *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        print(output)
    else:
        filename = get_filename()
        flags = 'w'
        if binary:
            flags += 'b'
        with open(filename, flags) as outfile:
            print("Writing data to {}...".format(filename))
            outfile.write(output)

    
def read_in_file(file):
     f = open(file,"r")
     return f.read()



def write_in_file(file,input):
     f = open(file, "w")
     f.write(str(input))
     f.close()




def attack_by_lll(msg_cipher, public_key_vector):

    text_clear = ""
    for i in range(0, len(msg_cipher)):
        element_message_cipher = msg_cipher[i]
        base_vector_list = attacking.create_base_vector_list(public_key_vector,element_message_cipher)  
        matrix_to_lll_reduction = liblll.create_matrix(base_vector_list)   
        reduced_matrix = liblll.lll_reduction(matrix_to_lll_reduction)
        deciphered_bit_sequence = attacking.get_first_column_as_bit_sequence(reduced_matrix)       
        bit_to_text = utility.convert_bit_to_text(deciphered_bit_sequence, len(public_key_vector))
        text_clear += bit_to_text
    print("clear-text/cracked-text : => " +str(text_clear))
    write_in_file("text_clear.txt",text_clear)
    return True


print("Encrypted text cipher:")
print(str(ast.literal_eval(read_in_file("result/output_msg_crypt.txt")))+"  \n")
print("Public Key:")
print(str(ast.literal_eval(read_in_file("keys/public_key/public_key.txt")))+"  \n")
begin = time.time() 

attack_by_lll(ast.literal_eval(read_in_file("result/output_msg_crypt.txt")),ast.literal_eval(read_in_file("keys/public_key/public_key.txt")))
end = time.time()
print("Time taken to attack:",end-begin)
print("\nEND OF ATTACKING PROGRAM")

