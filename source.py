#! /usr/bin/python3

def read_number(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    decimal = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * decimal
      decimal /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def read_plus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def read_minus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1

def read_open_parenthesis(line, index):
  token = {'type': 'OPEN PARENTHESIS', 'NUMBER': index}
  return token, index + 1

def read_close_parenthesis(line, index):
  token = {'type': 'CLOSE PARENTHESIS', 'NUMBER': index}
  return token, index + 1



def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = read_number(line, index)
    elif line[index] == '+':
      (token, index) = read_plus(line, index)
    elif line[index] == '-':
      (token, index) = read_minus(line, index)
    elif line[index] == '(':
      (token, index) = read_open_parenthesis(line, index)
    elif line[index] == ')':
      (token, index) = read_close_parenthesis(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


def evaluate(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer

class Stack:
  def __init__(self):
    self.stack = []
    self.top = 0
    self.bottom  = 0
  
  def push(self, index):
    self.top += 1 #リストのindex+1
    self.stack.append(index)

  def pop(self):
    if self.stack.len()>0:
      self.stack.pop()
      self.top -= 1
    else:
      print("Error: ')' doesn't correspond to '(' ")

  def check(self):
    if self.stack.top == self.stack.bottom:
      print("OK")
    else:
      print("Error: ')' doesn't correspond to '(' ")




#'()'に対応したevaluate
def evaluate_polling(tokens):
  tokens.insert({'type': 'OPEN PARENTHESIS', 'index': 0})
  tokens.append({'type': 'CLOSE PARENTHESIS', 'index': tokens.len()})
  parentheses_stack = Stack()
  index = 0
  while index < len(tokens):
    if(tokens[index][type] == 'OPEN PARENTHESIS'):
      parentheses_stack.push(index)
    if (tokens[index][type] == 'CLOSE PARENTHESIS'):
      tokens_inside_parentheses = []
      for i in range(tokens[index]['index'], index):
        tokens_inside_parentheses.append(tokens[i])
      answer = evaluate(tokens_inside_parentheses)
      new_tokens = []
      for i in range(0, tokens[index]['index']):
        new_tokens.append(tokens[i])
      new_tokens.append({'type': 'NUMBER', 'number': answer})
      for i in range(index+1, tokens.len()):
        new_tokens.append(tokens[i])
      index = tokens[index]['index']
      tokens = new_tokens
    index += 1
  parentheses_stack.check()

  return answer





def test(line):
  tokens = tokenize(line)
  actual_answer = evaluate(tokens)
  expected_answer = eval(line)
  if abs(actual_answer - expected_answer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expected_answer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  print("==== Test finished! ====\n")

run_test()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)
