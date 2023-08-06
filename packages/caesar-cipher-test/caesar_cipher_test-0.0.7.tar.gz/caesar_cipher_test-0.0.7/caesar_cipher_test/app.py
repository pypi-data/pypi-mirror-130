alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def caesar(start_text, shift_amount, cipher_direction):
  end_text = ""
  if cipher_direction == "decode":
    shift_amount *= -1
  
  for char in start_text:
    if char in alphabet:
      position = alphabet.index(char)
      #position of cipher text 
      # % 26 for char more zan z in the alphabet 
      new_position = (position + shift_amount) % 26
      end_text += alphabet[new_position]
    else:
      end_text += char
  print(f"Here's the {cipher_direction}d result: {end_text}")

from .art import logo
print(logo)

should_end = False
while not should_end:

  direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
  #terminate when the user not write in the above format encode or decode
  if direction == 'encode' or direction == 'decode':
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))
    # %26 for shift value more than 26
    shift = shift % 26
    caesar(start_text=text, shift_amount=shift, cipher_direction=direction)
  else:
      print('Wrong option.\n')
  restart = input("Type 'y/Y' if you want to go again. Otherwise type 'n/N'.\n").lower()
  if restart == "n":
    should_end = True
    print("Goodbye")
    


