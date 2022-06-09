import json
import time
import zipfile

SOLUTIONS_FILE = './data/solutions.json'
WORDS_FILE = './data/words.json'
EVALUATION_MAP_FILE = './data/evaluations.zip'
STARTING_GUESS = 'STARE'
WORD_LENGTH = 5

archive = zipfile.ZipFile(EVALUATION_MAP_FILE, 'r')
all_evaluations_serialized = archive.read(archive.namelist()[0])
all_evaluations = json.loads(all_evaluations_serialized)

with open(SOLUTIONS_FILE, 'r') as f:
    all_solutions = json.load(f)

with open(WORDS_FILE, 'r') as f:
    all_words = json.load(f)

def precompute():
    dict = {}
 
    for word1 in all_solutions:
        
        for word2 in all_solutions:

            key = getKey(word1, word2)
            altKey = getKey(word2, word1)

            if not key in dict.keys() and not altKey in dict.keys():
                dict[key if key < altKey else altKey] = evaluateGuess(word1, word2)         

    with open(EVALUATION_MAP_FILE, 'w') as f:
        json.dump(dict, f)

def getMatchesInSolution(letter, solution):

    matchesInSolution = 0
    
    for i in range(0, WORD_LENGTH):
        if solution[i] == letter:
            matchesInSolution += 1

    return matchesInSolution

def getMatchesSoFar(letter, guess, result, i):

    matchesSoFar = 0
    
    for j in range(0, i - 1): 
        if letter == guess[j] and result[i] != '-':
            matchesSoFar += 1

    return matchesSoFar

def evaluateGuessUsingMap(guess, solution):

    key = getKey(guess, solution) if guess < solution else getKey(solution, guess)
    return all_evaluations[key]

def evaluateGuess(guess, solution):

    result = ['','','','','']
   
    for i in range(0, WORD_LENGTH):

        if guess[i] == solution[i]:
            result[i] = 'X'

    for i in range(0, WORD_LENGTH):

        if result[i] == 'X':
            continue

        letter = guess[i]
        matchesSoFar = getMatchesSoFar(letter, guess, result, i)
        matchesInSolution = getMatchesInSolution(letter, solution)

        result[i] = 'O' if matchesInSolution > matchesSoFar else '-'
       
    return ''.join(result)

def getKey(word1, word2):

    return f'{word1}|{word2}'

def findSolution(guess, solution, solutions):

    guess_count = 0
    
    while len(solutions) > 1:
        guess_count += 1
        #result = evaluateGuess(guess, solution)
        key = getKey(guess, solution)
        result = evaluateGuessUsingMap(guess, solution)
        filtered_solutions = []

        for possible_solution in solutions:
            #possible_solution_result = evaluateGuess(guess, possible_solution)
            possible_solution_result = evaluateGuessUsingMap(guess, possible_solution)
        
            if possible_solution_result == result:
                filtered_solutions.append(possible_solution)

        solutions = filtered_solutions
        guess = solutions[0]
    else:
        return guess_count

def run():
    start_time = time.time()

    for starting_guess in all_solutions[0:10]: 

        guess_counts = []

        for solution in all_solutions: 
            guess_count = findSolution(starting_guess, solution, all_solutions)
            guess_counts.append(guess_count)

        print(starting_guess, 'average:', sum(guess_counts) / len(guess_counts))

    end_time = time.time()
    print('Execution time: --- %s seconds ---' % (end_time - start_time))

