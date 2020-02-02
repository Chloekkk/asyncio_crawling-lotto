from django.shortcuts import render
import random
from collections import Counter

# Create your views here.

def home(request):
    return render(request, 'home.html')

def result(request):
    numberlist = []
    # lottolist = list(range(1,46))
    lottolist = random.sample(list(range(1, 46)), 6)
    # 왜 sort 안됨?

    # get input data
    try:
        for i in range(1,7):
            numberlist.append(int(request.GET[str(i)]))
    except(ValueError):
        return render(request, 'home.html', {'empty':1})
  
    # check overlap num
    checknum = Counter(numberlist)
    wrongnum = []
    for key in checknum:
        if checknum[key] != 1:
            wrongnum.append(checknum)

    if wrongnum:
        print("exist wrong num")
        return render(request, 'home.html', {'wrong':wrongnum})

    # calculate right number
    sum = 0
    for num in numberlist:
        if num in lottolist:
            sum += 1

    percentage = (sum/6)*100
    return render(request, 'result.html', {'numlist':numberlist, 'lotto':lottolist, 'sum':sum, 'percent':percentage})