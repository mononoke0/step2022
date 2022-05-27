#! /usr/bin/python3
# -*- coding: utf-8 -*-
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


def read_mult(line, index):
    token = {'type': 'MULT'}
    return token, index + 1

def read_division(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1

def read_open_parenthesis(line, index):
  token = {'type': 'OPEN PARENTHESIS'}
  return token, index + 1

def read_close_parenthesis(line, index):
  token = {'type': 'CLOSE PARENTHESIS'}
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
    elif line[index] == '*':
        (token, index) = read_mult(line, index)
    elif line[index] == '/':
        (token, index) = read_division(line, index)
    elif line[index] == '(':
      (token, index) = read_open_parenthesis(line, index)
    elif line[index] == ')':
      (token, index) = read_close_parenthesis(line, index)

    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
    
  return tokens


#'+', '-' を処理したtokensを返す
def plus_minus_evaluate(tokens):
  answer = 0
  index = 0
  #数字を表すtokenの要素の前の符号を確認：flg == 1 -> '+', flg == 0 -> '-'
  flg = 1
  #'-2+1', '-3+1'のように最初の数が負の値('-'から始まる)場合
  if(tokens[index]['type'] == 'MINUS'):
      flg = 0

  while index < len(tokens)-1:
    if tokens[index]['type'] == 'NUMBER':
      #後ろに'+', '-'のついている数字を読む(`*`, '/'の処理時に、計算結果aがaの計算に使用したtokensの要素数の分だけ、aa...と重複してtokensに存在するため)
      if tokens[index + 1]['type'] == 'PLUS':
          #'+', '-'のどちらを行うかはflgで確認
          if(flg == 1):
              answer += tokens[index]['number']
          else:
              answer -= tokens[index]['number']
          flg = 1
      elif tokens[index + 1]['type'] == 'MINUS':
          if(flg == 1):
              answer += tokens[index]['number']
          else:
              answer -= tokens[index]['number']
          flg = 0

      else:
        print('Invalid syntax')
        exit(1)
    index += 1

  return answer

#'(', ')'をスタックを使用して対応させる
class Stack:
  def __init__(self):
    self.stack = []
    self.top = 0 
    self.bottom  = 0
  
  def push(self, index):
    self.top += 1 
    self.stack.append(index)

  def pop(self):
    if len(self.stack)>0:
      self.stack.pop()
      self.top -= 1
    else:
      #')'に対応する'('が足りない場合
      print("pop Error: ')' doesn't correspond to '(' ")

  def check(self):
    #スタックの中身が空になっているか
    if self.top == self.bottom:
      #flag : 1-> ok, 0->failed
      return 1 
    else:
      print("Error: ')' doesn't correspond to '(' ")
      return 0
      


#'()'に対応したevaluate
def evaluate_polling(tokens):
  #数式の先頭に'(', 末尾に')'を追加
  tokens.insert(0, {'type': 'OPEN PARENTHESIS', 'index': 0})
  tokens.append({'type': 'CLOSE PARENTHESIS', 'index': len(tokens)})
  #スタックの作成
  parentheses_stack = Stack()
  index = 0
  while index < len(tokens):
    if(tokens[index]['type'] == 'OPEN PARENTHESIS'):
      #スタックに'('のindexを追加
      parentheses_stack.push(index)
    if (tokens[index]['type'] == 'CLOSE PARENTHESIS'):
      #tokens_inside_parentheses：()の内側のtokenのリスト
      tokens_inside_parentheses = []
      for i in range(parentheses_stack.stack[-1]+1, index):
        tokens_inside_parentheses.append(tokens[i])
      #()の内側のtokenのリストを計算
      answer = evaluate(tokens_inside_parentheses)
      print("answer: ", answer)
      #()を処理済みのtokens(new_tokens)を新たに作成
      new_tokens = []
      for i in range(0, parentheses_stack.stack[-1]):
        new_tokens.append(tokens[i])
      new_tokens.append({'type': 'NUMBER', 'number': answer})
      for i in range(index+1, len(tokens)):
        new_tokens.append(tokens[i])
      #新しいtokensに対応したindexに更新
      index = parentheses_stack.stack[-1]
      #tokensを新しいものに更新
      tokens = new_tokens
      #処理した')'に対応するスタックの要素をpop
      parentheses_stack.pop()
    index += 1
  #'(', ')'が対応しているか、スタックの中身で確認
  flg = parentheses_stack.check()
  if flg == 0:
    answer = None

  return answer



#'*', '/' を処理したtokensを返す
def mult_division_evaluate(tokens):
    #'*', '/' はindex-2にアクセスするのでindexは2からスタート
    index = 2
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if(tokens[index-1]['type']) == 'MULT':
                tokens[index]['number'] *= tokens[index-2]['number']
                #計算し終わったtokensの要素は{'type': 'dummy'}にかえる
                tokens[index-2] = {'type': 'dummy'}
                tokens[index-1] = {'type': 'dummy'}
            elif(tokens[index-1]['type'] == 'DIVISION'):
                tokens[index]['number'] = tokens[index-2]['number']/tokens[index]['number']
                #計算し終わったtokensの要素は{'type': 'dummy'}にかえる
                tokens[index-2] = {'type': 'dummy'}
                tokens[index-1] = {'type': 'dummy'}
        index += 1

    return tokens

#'+', '-', '*', '/' を処理した結果を返す
def evaluate(tokens):
    answer = 0
    #'*', '/' を計算
    tokens = mult_division_evaluate(tokens)
    #tokensの末尾に'+'を追加
    tokens.append({'type': 'PLUS'})
    #'+', '-' を計算
    answer = plus_minus_evaluate(tokens)

    return answer


#正しい数式か確認(2++2, 2+-2など、符号が連続していないか)
def check_true_numerical_formula(tokens):
  if tokens[-1]['type'] != 'NUMBER' :
    print(" must be a number at the end position of the numerical formula.")
    return 0
  index = 0
  check = 0
  while index<len(tokens):
    if (tokens[index]['type'] == 'PLUS') or (tokens[index]['type'] == 'MINUS') or (tokens[index]['type'] == 'MULT') or (tokens[index]['type'] == 'DIVISION'):
      check += 1
    if (tokens[index]['type'] == 'NUMBER'):
      check = 0

    if check > 1:
      print (" this numerical formula is wrong.  plus or minus signs are connected. ")
      return 0
    
    if (tokens[index]['type'] == 'DIVISION') and (tokens[index+1]['type'] == 'NUMBER') and (tokens[index+1]['number'] == 0):
      print (" cannot divide the numerical formula by 0.")
      return 0
    index += 1

  return 1


def test(line):
  tokens = tokenize(line)

  check = check_true_numerical_formula(tokens)
  if check == 1:
    actual_answer = evaluate_polling(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
      print("PASS! (%s = %f)" % (line, expected_answer))
    else:
      print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))
  else:
    return 


# Add more tests to this function :)
def run_test():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("1")
  test("-1")
  test("1*2+1")
  test("1*2.0+1")
  test("1+2*1")
  test("1+2/3")
  test("1+2.0/3")
  test("9/3/2")
  test("-1+1")
  test("-1.0*2")
  test("-3/2+1")
  test("-3.0/2+1")


  print("==== Test finished! ====\n")

run_test()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  check = check_true_numerical_formula(tokens)
  if check  == 1:
    answer = evaluate_polling(tokens)
    if answer != None:
      print("answer = %f\n" % answer)
    else:
      print("cannot return answer")
  else:
    pass
