import sys
import re

#Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
def parse_input(data):
    ingredients = {}
    # Split the data into lines
    lines = data.strip().split('\n')
    for line in lines:
        ingredient, others = line.split(': ')
        ingredients[ingredient]={}
        for other in others.split(', '):
            prop, value = other.split(' ')
            ingredients[ingredient][prop] = int(value)
    return ingredients

scores = set()
scores2 = set()

def score_recipe(properties,ingredients,qty):
    retval = 1
    props = set()
    Values= {}
    for ingredient in properties:
        for prop in properties[ingredient]:
            props.add(prop)
    for prop in props:
        if prop == 'calories':
            continue
        #print(f'Calculating: {prop}')
        Values[prop] = 0
        for i in range(len(ingredients)):
            Values[prop]+=properties[ingredients[i]][prop]*qty[i]
        #print(f'Prop: {prop}, Value: {Values[prop]}')
        #print(Values)
    for val in Values.values():
        if val < 0:
            val = 0
        retval *= val
    calories = 0
    for i in range(len(ingredients)):
        calories+=properties[ingredients[i]]['calories']*qty[i]
    if calories == 500:
        global scores2
        scores2.add(retval)
    return retval

def find_recipe(properties,ingredients=(),qty=()):
    #print(f'find_recipe(properties,{ingredients},{qty})')
    if not ingredients:
        tmpList = []
        for ingredient in properties:
            tmpList.append(ingredient) 
        ingredients = tuple(tmpList)
    q=sum(qty)
    if len(qty) < len(ingredients):
        #print(f'Not all ingredients are accounted for {q}')
        #print(f'100-{len(ingredients)}+2-{q} = {100-len(ingredients)+2-q}')
        #for i in range(99-len(ingredients)+2-q,0,-1):
        for i in range(100 - q, 0, -1):
        #for i in range(99,0,-1):
            tmpList = list(qty)
            tmpList.append(i)
            find_recipe(properties,ingredients,tuple(tmpList))
    elif q < 100 or q > 100:
        return -1
    else:
        score = score_recipe(properties,ingredients,qty)
        #print(f'Score: {ingredients} {qty}: {score}')
        global scores
        scores.add(score)
        return score
    return 0

def part1(parsed_data):
    retval = 0;
    retval = find_recipe(parsed_data)
    global scores
    retval = max(scores)
    return retval

def part2(parsed_data):
    retval = 0;
    global scores2
    retval = max(scores2)
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    print(parsed_data)

    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    