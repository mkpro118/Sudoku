from django.http.response import JsonResponse
from django.shortcuts import render
from .sudoku import *

generator = sudokuGenerator()

# Create your views here.
def getPuzzle(request, level):
    solution = next(generator)
    problem = maskSudoku(solution, level)
    return JsonResponse({
        'problem': problem,
        'solution': solution,
    })

def home(request):
    return render(request, 'sudoku.html')
