#Домашнее задание: декораторы

import requests
import time
import re
import functools
from functools import wraps
from random import randint

BOOK_PATH = 'https://www.gutenberg.org/files/2638/2638-0.txt'

def benchmark(func):
    """
    Декоратор, выводящий время, которое заняло выполнение декорируемой функции
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
 
     start = time.perf_counter() 
      result = func(*args, **kwargs)
      end = time.perf_counter() 
      print(f'Время выполнения функции {func.__name__} составило {end - start:.6f} секунд')
      return result
    return wrapper

def logging(func):
    """
    Декоратор, который выводит параметры с которыми была вызвана функция
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print(f'Функция вызвана с параметрами: {func.__name__} {args} {kwargs}')
        return res
    return wrapper


def counter(func):
    """
    Декоратор, считающий и выводящий количество вызовов декорируемой функции
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        res = func(*args, **kwargs)
        print(f'{func.__name__} была вызвана {wrapper.count} раз')
        return res
    wrapper.count = 0
    return wrapper

def memo(func):
  """
  Декоратор, запоминающий результаты исполнения функции func, чьи аргументы args должны быть хешируемыми
  """
  cache = {}
  @wraps(func)
  def fmemo(*args):
    if args in cache:
      return cache[args]
    else:
      cache[args] = func(*args)
      return cache[args]
  fmemo.cache = cache
  return fmemo


@counter
@logging
@benchmark
def word_count(word, url=BOOK_PATH):
    """
    Функция для посчета указанного слова на html-странице
    """

    # отправляем запрос в библиотеку Gutenberg и забираем текст
    raw = requests.get(url).text

    # заменяем в тексте все небуквенные символы на пробелы
    processed_book = re.sub('[\W]+' , ' ', raw).lower()

    # считаем
    cnt = len(re.findall(word.lower(), processed_book))

    return f"Cлово {word} встречается {cnt} раз"

print(word_count('whole'))



def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)


# измеряем время выполнения
@benchmark
def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)
fib(5) 


@memo
def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)


# измеряем время выполнения
@benchmark
@memo
def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)

fib(5)


# Время выполнения рекурсивной реализации расчета чисел Фибоначчи без декоратора больше чем с ним

