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
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
    
  return tokens


#'+', '-' を処理したtokensを返す
def plus_minus_evaluate(tokens):
  answer = 0
  #tokensの末尾にdummyの'+'を追加
  #tokens.append({'type': 'PLUS'}) 
  index = 0
  #数字を表すtokenの要素の前の符号を確認：flg == 1 -> '+', flg == 0 -> '-'
  flg = 1
  #'-2+1', '-3+1'のように最初の数が負の値('-'から始まる)場合
  if(tokens[index]['type'] == 'MINUS'):
      flg = 0


  while index < len(tokens)-1:
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index + 1]['type'] == 'PLUS':
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
  #符号で式が終わる場合
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

    #0で割る場合
    if (tokens[index]['type'] == 'DIVISION') and (tokens[index+1]['type'] == 'NUMBER') and (tokens[index+1]['number'] == 0):
      print (" cannot divide the numerical formula by 0.")
      return 0
    index += 1

  return 1


                
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
  #1桁
  test("1")
  test("1.0")
  test("-1")
  test("-1.0")

  #2桁
  test("1+1")
  test("1.0+1")
  test("1+1.0")
  test("1.0+1.0")

  test("-1+1")
  test("-1.0+1")
  test("-1+1.0")
  test("-1.0+1.0")

  test("1-1")
  test("1.0-1")
  test("1-1.0")
  test("1.0-1.0")

  test("2*1")
  test("2.0*1")
  test("2*1.0")
  test("2.0*1.0")

  test("2/1")
  test("2.0/1")
  test("2/1.0")
  test("2.0/1.0")

  #3桁
  test("1+1+1")
  test("1+1+1.0")
  test("1+1.0+1")
  test("1.0+1+1")
  test("1+1.0+1.0")
  test("1.0+1+1.0")
  test("1.0+1.0+1")
  test("1.0+1.0+1.0")

  test("2+1-1")
  test("2+1-1.0")
  test("2+1.0-1")
  test("2.0+1-1")
  test("2+1.0-1.0")
  test("2.0+1-1.0")
  test("2.0+1.0-1")
  test("2.0+1.0-1.0")

  test("2+1*1")
  test("2+1*1.0")
  test("2+1.0*1")
  test("2.0+1*1")
  test("2+1.0*1.0")
  test("2.0+1*1.0")
  test("2.0+1.0*1")
  test("2.0+1.0*1.0")

  test("2+1/1")
  test("2+1/1.0")
  test("2+1.0/1")
  test("2.0+1/1")
  test("2+1.0/1.0")
  test("2.0+1/1.0")
  test("2.0+1.0/1")
  test("2.0+1.0/1.0")

  test("2-1-1")
  test("2-1-1.0")
  test("2-1.0-1")
  test("2.0-1-1")
  test("2-1.0-1.0")
  test("2.0-1-1.0")
  test("2.0-1.0-1")
  test("2.0-1.0-1.0")

  test("2-1+1")
  test("2-1+1.0")
  test("2-1.0+1")
  test("2.0-1+1")
  test("2-1.0+1.0")
  test("2.0-1+1.0")
  test("2.0-1.0+1")
  test("2.0-1.0+1.0")

  test("2-1*1")
  test("2-1*1.0")
  test("2-1.0*1")
  test("2.0-1*1")
  test("2-1.0*1.0")
  test("2.0-1*1.0")
  test("2.0-1.0*1")
  test("2.0-1.0*1.0")

  test("2-1/1")
  test("2-1/1.0")
  test("2-1.0/1")
  test("2.0-1/1")
  test("2-1.0/1.0")
  test("2.0-1/1.0")
  test("2.0-1.0/1")
  test("2.0-1.0/1.0")

  test("2*1*1")
  test("2*1*1.0")
  test("2*1.0*1")
  test("2.0*1*1")
  test("2*1.0*1.0")
  test("2.0*1*1.0")
  test("2.0*1.0*1")
  test("2.0*1.0*1.0")

  test("2*1+1")
  test("2*1+1.0")
  test("2*1.0+1")
  test("2.0*1+1")
  test("2*1.0+1.0")
  test("2.0*1+1.0")
  test("2.0*1.0+1")
  test("2.0*1.0+1.0")

  test("2*1-1")
  test("2*1-1.0")
  test("2*1.0-1")
  test("2.0*1-1")
  test("2*1.0-1.0")
  test("2.0*1-1.0")
  test("2.0*1.0-1")
  test("2.0*1.0-1.0")

  test("2*1/1")
  test("2*1/1.0")
  test("2*1.0/1")
  test("2.0*1/1")
  test("2*1.0/1.0")
  test("2.0*1/1.0")
  test("2.0*1.0/1")
  test("2.0*1.0/1.0")

  test("2/1/1")
  test("2/1/1.0")
  test("2/1.0/1")
  test("2.0/1/1")
  test("2/1.0/1.0")
  test("2.0/1/1.0")
  test("2.0/1.0/1")
  test("2.0/1.0/1.0")

  test("2/1+1")
  test("2/1+1.0")
  test("2/1.0+1")
  test("2.0/1+1")
  test("2/1.0+1.0")
  test("2.0/1+1.0")
  test("2.0/1.0+1")
  test("2.0/1.0+1.0")

  test("2/1-1")
  test("2/1-1.0")
  test("2/1.0-1")
  test("2.0/1-1")
  test("2/1.0-1.0")
  test("2.0/1-1.0")
  test("2.0/1.0-1")
  test("2.0/1.0-1.0")

  test("2/1*1")
  test("2/1*1.0")
  test("2/1.0*1")
  test("2.0/1*1")
  test("2/1.0*1.0")
  test("2.0/1*1.0")
  test("2.0/1.0*1")
  test("2.0/1.0*1.0")


  print("==== Test finished! ====\n")

run_test()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  check = check_true_numerical_formula(tokens)
  if check  == 1:
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
  else:
    pass

 