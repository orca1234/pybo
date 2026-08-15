from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..models import Question


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준
    category = request.GET.get('category', '')  # 카테고리

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # 카테고리 필터
    if category:
        question_list = question_list.filter(category=category)

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    # 카테고리 목록 (필터 드롭다운용, 중복 제거)
    category_list = Question.objects.exclude(category='').values_list('category', flat=True).distinct()

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so, 'category': category, 'category_list': category_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)

    # 조회수 (세션당 1회)
    session_key = 'viewed_question_%s' % question_id
    if not request.session.get(session_key, False):
        question.hit = question.hit + 1
        question.save()
        request.session[session_key] = True

    # 답변 정렬
    answer_so = request.GET.get('answer_so', 'recent')
    if answer_so == 'recommend':
        answer_list = question.answer_set.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif answer_so == 'oldest':
        answer_list = question.answer_set.order_by('create_date')
    else:  # recent
        answer_list = question.answer_set.order_by('-create_date')

    # 답변 페이징
    answer_page = request.GET.get('answer_page', '1')
    paginator = Paginator(answer_list, 5)  # 답변 5개씩
    answer_page_obj = paginator.get_page(answer_page)

    context = {
        'question': question,
        'answer_list': answer_page_obj,
        'answer_so': answer_so,
        'answer_page': answer_page,
    }
    return render(request, 'pybo/question_detail.html', context)