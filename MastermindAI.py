## This is a program that implements Kunth's Mastermind Algorithm
## to deduce a standard 4-digit code with 6 possibilites.

##----------------------------------------------------------------------------##

## Returns a set of all 4-digit codes
## Digits can have 6 possible values: (0,1,2,3,4,5)
def generate_all_codes():
    all_codes = set()

    ## TODO: Use some sort of loop to generate all possible codes
    
    for one in range(0,6):
        for two in range(0,6):
            for three in range(0,6):
                for four in range(0,6):
                    all_codes.add((one,two,three,four))
            
    ## This line will check if you are returning the correct number of codes.
    assert(len(all_codes) == 1296)
    return all_codes

## Convert a tuple guess to a string
def guess_to_string(guess):
    y = list()

    ## TODO: Convert a tuple guess to a string
    ## Ex, (0, 1, 2, 3)  ->  0123

    for item in guess:
        y.append(str(item))
    str_guess = ''.join(y)
    
    return str_guess

## Returns the correctness of a guess and code.
## Done for you, no need to modify
def is_valid_guess(string_guess):

    ## TODO: Check guess to make sure it doesn't break your program
    ## HINT: https://www.w3schools.com/python/python_ref_string.asp
    ## HINT: Guess is a string, how do we know it only has numbers?
    if not string_guess.isnumeric():
        return False
    if len(string_guess) != 4:
        return False
    for num in string_guess:
        if int(num) > int(6-1):
            return False
    return True

def simulate_response(guess, code):
    ## Make sure that guess and code are the same length
    assert(len(guess) == len(code))

    ## Create two empty lists [0,0,0,0,0,0]
    guess_count = [0] * 6
    code_count  = [0] * 6

    ## Count how many times each digit shows up
    for digit in guess:
        guess_count[digit] += 1

    for digit in code:
        code_count[digit] += 1

    ## Compute how many numbers were guessed correct numbers
    correct_nums = 0

    for g, c in zip(guess_count, code_count):
        correct_nums += min(g, c)

    ## Count how many positions were correct
    correct_position = 0
    
    for g, c in zip(guess, code):
        if g == c:
            correct_position += 1

    return (correct_nums, correct_position)

##----------------------------------------------------------------------------##

## Class that will help you breaks Mastermind game codes.
class MastermindAI:
    def __init__(self):
        
        self.all_codes = generate_all_codes()
        self.possible_codes = self.all_codes.copy()
        self.previous_guesses = list()
        self.previous_responses = list()
        
    ## Based on possible_codes, calculate the best next guess
    ## TODO: Fill in the blanks and 
    def make_a_guess(self):
        ## If this is the first guess, guess 0011
        if len(self.previous_guesses) <= 0:
            self.previous_guesses.append((0,0,1,1))
            return (0,0,1,1)

        ## If there is only 1 possible code, return it
        ## self.possible_codes is a set
        ## https://www.w3schools.com/python/python_ref_set.asp

        ## TODO: Code Here
        if len(self.possible_codes) == 1:
            return self.possible_codes.pop()
        
        ## Initialize some variables
        empty_response_count = dict()
        best_guess = (0,0,1,1)
        best_worst_response = len(self.possible_codes)

        ## Set all possible responses to zero in empty_response_count
        ## Think about what responses are possible.
        ## Is it possible to have more correct_positions than correct_nums?
        ## empty_response_count[(0,0)] = 0
        ## empty_response_count[(1,0)] = 0
        ## ...
        ## And so on

        ## TODO: Code Here        
        
        for i in range(0,6):
            for j in range(0,i+1):
                empty_response_count[(i,j)] = 0
        
        for guess in self.all_codes:
            ## make a copy of empty_response_count
            ## https://www.w3schools.com/python/python_ref_dictionary.asp
            ## TODO: Blanks Here
            response_count = empty_response_count.copy()

            for code in self.possible_codes:
                ## Simulate the response between guess and code
                ## Increment (add 1) to the response count
                ## TODO: Code Here
                response_count[simulate_response(guess, code)] += 1
            ## Apply minmax
            ## If the worst count in response_count (the largest count) is less than (better) our best_worst_response
            ## then it should be the new best_worst_response
            ## best_guess should be equal to the guess that generated this response count
            ## https://www.w3schools.com/python/python_ref_dictionary.asp
            ## https://www.w3schools.com/python/ref_func_max.asp
            ## TODO: Blanks Here
            if max(response_count.values()) < best_worst_response:
                best_worst_response = max(response_count.values())
                best_guess = guess
                
        return best_guess

    ## Updates the set of possible codes by checking the response the code gives
    ## if it had been the actual code. If it does not match the response from the
    ## actual code, it cannot possible be the code, so it is removed.
    def update(self, guess, response):
        ## Add guess and response to previous_guesses and previous_responses
        self.previous_guesses.append(guess)
        self.previous_responses.append(response)

        ## Create a set for all of the items you want to remove
        remove_set = set()

        ## Loop through all possible codes and simulate their response with the guess
        ## If the simulated response does not equal the actual response, then it cannot
        ## be a possible code. So we add it to the remove_set.
        ## https://www.w3schools.com/python/python_ref_set.asp
        ## TODO: Code Here
        for code in self.possible_codes:
            if simulate_response(guess, code) != response:
                remove_set.add(code)

        ## Remove all codes in remove_set from self.possible_codes
        ## https://www.w3schools.com/python/python_ref_set.asp

        ## TODO: One Line of Code Here
        self.possible_codes.difference_update(remove_set)
    ## Reset MastermindAI object to start a new game
    def reset(self):
        self.possible_codes = self.all_codes.copy()
        self.previous_guesses = list()
        self.previous_responses = list()

##----------------------------------------------------------------------------##

if __name__ == "__main__":
    ## TODO: Make an interactive bot
    ## Do what ever you want, be creative

    ## Create an MastermindAI object
    ai = MastermindAI()

    ## Print Introduction and Instructions
    print('━━(￣ー￣*|||━━\n(´･･)ﾉ is an AI that will take your input code, and will determine it in under 5 guesses using an algorithm.')
    

    #_`Wait for human to think of code and press Enter
    result = list()
    code = input('Enter a code with 4 digits and digits from 0-5 \nEx:\'1234\'\n')
    while not is_valid_guess(code):
        print('Enter a valid guess: Ex \'0123\'')
        code = input()
    for item in code:
        item = int(item)
        result.append(item)
    code = tuple(result)
    
    while True:
        guessed = ai.make_a_guess()
        ## Print out a guess
        print('(´･･)ﾉ Guess: {0}\tActual Code: {1}\n'.format(guess_to_string(guessed),guess_to_string(code)))
        if guessed == code:
            break
        response = simulate_response(guessed, code)
        ai.update(guessed,response)
    print('(´･･)ﾉ figured out the code\nThanks for typing a code and pressing enter!')    

    ## Ask how many numbers are correct. Read user input.
    #input('How many numbers are correct?\nYour Code: {0}   Returned Code: {1}\nAnswer: '.format(code,guessed))
    ## Ask how many positions are correct. Read user input.
    #input('How many numbers are in the correct position?\nYour Code: {0}   Returned Code: {1}\nAnswer: '.format(code, guessed))

    ## Repeat!
