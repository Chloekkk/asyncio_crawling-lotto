from django.shortcuts import render
import random
from collections import Counter
# import lotto.asyncio_crawling

# Create your views here.

def home(request):
    return render(request, 'home.html')

def result(request): 
    numberlist = []
    # lottolist = list(range(1,46))
    lottolist = random.sample(list(range(1, 46)), 7)
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
    
    # print("hello")
    # print(asyncio_crawling.results)
    results = lotto.asyncio_crawling.results
    final_last_lotto_num = []
    final_last_lotto_num.append(results.get(1))
    final_count = 0
    check_2nd = False

    if (len(set(numberlist) & set(final_last_lotto_num[0][:-1])) == 5) and (final_last_lotto_num[0][-1] in numberlist) :
        check_2nd = True

    for i in range(1, len(results.keys())+1):
        count = len(set(numberlist) & set(results.get(i)[:-1]))
        final_count = len(set(numberlist) & set(final_last_lotto_num[0][:-1]))
        # 첫번째 예외 셋팅
        if i == 1 :
            final_count = 0
        if count > final_count:
            final_last_lotto_num.clear()
            final_last_lotto_num.append(results.get(i))
        elif count == final_count:
            if count == 5:
                if (results.get(i)[-1] in numberlist) and (final_last_lotto_num[0][-1] in numberlist):
                    final_last_lotto_num.append(results.get(i))
                    check_2nd = True
                elif (results.get(i)[-1] in numberlist) and (final_last_lotto_num[0][-1] not in numberlist):
                    final_last_lotto_num.clear()
                    final_last_lotto_num.append(results.get(i))
                    check_2nd = True
                elif (results.get(i)[-1] not in numberlist) and (final_last_lotto_num[0][-1] in numberlist):
                    check_2nd = True
                elif (results.get(i)[-1] not in numberlist) and (final_last_lotto_num[0][-1] not in numberlist):
                    final_last_lotto_num.append(results.get(i))
            else :  
                final_last_lotto_num.append(results.get(i))
        elif count < final_count:
            pass 

    if final_count == 0 :
        final_last_lotto_num.clear()

    print(final_count, final_last_lotto_num)
    percentage = (sum/6)*100
    # 원래는 all_winning_numbers 에 results  넣었음 
    return render(request, 'result.html', {'numlist':numberlist, 'lotto':lottolist, 'sum':sum, 'percent':percentage, 'all_winning_numbers': final_last_lotto_num})