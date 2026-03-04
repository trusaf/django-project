import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Diary
from .forms import DiaryForm

# 01. 목록 및 검색 뷰
class DiaryListView(LoginRequiredMixin, ListView):
    model = Diary
    template_name = 'diary/diary_list.html'
    context_object_name = 'diaries'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        # 본인 작성, 직접 공유받음, 소속 가족 그룹의 일기만 필터링
        qs = Diary.objects.filter(
            Q(author=user) | 
            Q(shared_users=user) | 
            Q(family_group__members=user)
        ).distinct()
        
        # 검색어 처리
        query = self.request.GET.get('q', '')
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query))
        
        # (추가) 드롭다운 메뉴를 통한 일기 유형(type) 필터링 처리
        diary_type = self.request.GET.get('type')
        if diary_type in ['100Y', 'COLLAB', 'FAMILY']:
            qs = qs.filter(diary_type=diary_type)
        
        return qs

# 02. 상세 조회 뷰
class DiaryDetailView(LoginRequiredMixin, DetailView):
    model = Diary
    template_name = 'diary/diary_detail.html'

# 03. 작성 뷰
class DiaryCreateView(LoginRequiredMixin, CreateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# 04. 수정 뷰
class DiaryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary_form.html'
    
    # 수정 성공 시 이동할 URL 지정 (예: 해당 일기 상세 페이지)
    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.object.pk})

    # 요청 사용자가 일기 작성자와 일치하는지 확인하는 권한 검증 메서드
    def test_func(self):
        diary = self.get_object()
        return self.request.user == diary.author

# 05. 삭제 뷰
class DiaryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Diary
    template_name = 'diary/diary_confirm_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    def test_func(self):
        diary = self.get_object()
        return self.request.user == diary.author


# 11. '100년 일기 서브메뉴'
class HundredYearDiaryView(LoginRequiredMixin, ListView):
    model = Diary
    template_name = 'diary/100y_diary.html'
    context_object_name = 'diaries'

    def get_queryset(self):
        # 1. 기준일 설정 (파라미터가 없거나 오류 시 오늘 날짜 지정)
        date_str = self.request.GET.get('date')
        if date_str:
            try:
                target_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                target_date = datetime.date.today()
        else:
            target_date = datetime.date.today()

        self.target_date = target_date # 템플릿 전달용 저장

        # 2. 본인 작성 및 100년 일기 유형 필터링
        current_year = target_date.year
        queryset = Diary.objects.filter(
            author=self.request.user,
            diary_type='100Y',
            target_date__month=target_date.month,
            target_date__day=target_date.day,
            target_date__year__gte=current_year - 5, # 최근 5년 범위 시작
            target_date__year__lte=current_year      # 최근 5년 범위 끝
        ).order_by('-target_date')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 선택된 기준일을 화면에 유지하기 위해 컨텍스트 추가
        context['target_date'] = self.target_date
        return context