from django.shortcuts import render, get_object_or_404

from pybo.models import Question, Answer

# Paginator 불러오기
# 페이징 기능을 담당하는 클래스
# Paginator는 쿼리셋(혹은 리스트)를 받아서 페이지 단위로 나누는 역할
from django.core.paginator import Paginator

from django.db.models import Q, Count

def index(request):
    # request.GET: URL의 쿼리스트링(?뒤에 값)을 가져오는 부분
    # http://127.0.0.1/pybo/?page=1
    # page=3 이라는 요청이 들어오면 page에 3이 저장됨
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            # Q함수를 이용하여 검색
            # __icontains: 대소문자 구별 없이 부분문자열 검색(LIKE "%kw%")
            Q(subject__icontains = kw) |
            Q(content__icontains = kw) |
            # question_list에서 filter 함수를 적용
            # Question -> author -> username
            Q(author__username__icontains = kw) |
            # Question -> reserse FK(Answer) -> author -> username
            Q(answer__author__username__icontains = kw)
        ).distinct() # 중복 제거
        """
        select distinct q.*
        from pybo_question q
        left join pybo_answer a on a.question_id = q.id
        right join customuser c on c.id = a.author_id
        where q.subject ilike "%kw%"
           or q.content ilike "%kw%"
           or c.username ilike "%kw%"
        """

    # Question.objects.all()로 확인할 결과는 page63 참조
    # 쿼리셋으로 조회됨
    paginator = Paginator(question_list, 10)
    # 데이터 묶음을 전달해주기 위한 가공
    # get_page() 메서드는 유효하지 않은 번호를 넣어도 자동으로 처리(999를 넣으면 마지막 페이지 처리)

    page_obj = paginator.get_page(page)

    current_page = page_obj.number
    start_index = max(current_page - 5, 1)
    end_index = min(current_page + 5, paginator.num_pages)
    page_range = range(start_index, end_index + 1)

    context = {
        'question_list': page_obj,
        'page_range': page_range,
        'page': page,
        'kw': kw,
        'so': so,
    }

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')
    page = request.GET.get('page', '1')

    if so == 'recommend':
        answer_list = question.answer_set.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'old':
        answer_list = question.answer_set.order_by('create_date')
    else:
        answer_list = question.answer_set.order_by('-create_date')

    if kw:
        answer_list = answer_list.filter(
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw)
        ).distinct()


    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)

    current_page = page_obj.number
    start_index = max(current_page - 5, 1)
    end_index = min(current_page + 5, paginator.num_pages)
    page_range = range(start_index, end_index + 1)

    context = {
        'question': question,
        'answer_list': page_obj,
        'page_range': page_range,
        'page': page,
        'kw': kw,
        'so': so,
    }

    return render(request, 'pybo/question_detail.html', context)
