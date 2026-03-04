from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.DiaryListView.as_view(), name='diary_list'), # 목록 및 검색
    path('100y/', views.HundredYearDiaryView.as_view(), name='100y_diary'), # 100년 일기
    path('create/', views.DiaryCreateView.as_view(), name='diary_create'), # 신규 작성
    path('<int:pk>/', views.DiaryDetailView.as_view(), name='diary_detail'), # 상세 보기
    path('<int:pk>/edit/', views.DiaryUpdateView.as_view(), name='diary_edit'), # 수정 (이전 단계 작성분)
    path('<int:pk>/delete/', views.DiaryDeleteView.as_view(), name='diary_delete'), # 삭제
]