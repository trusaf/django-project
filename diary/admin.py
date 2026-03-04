from django.contrib import admin
from .models import FamilyGroup, Diary

@admin.register(FamilyGroup)
class FamilyGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    # 다대다 필드(M2M)의 양방향 선택 위젯 적용 (멤버 추가/제거 용이)
    filter_horizontal = ('members',)

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'diary_type', 'target_date', 'author', 'created_at')
    list_filter = ('diary_type', 'target_date', 'author')
    search_fields = ('title', 'content', 'author__username')
    # 날짜 기반 계층형 네비게이션 적용 (100년 일기 탐색 최적화)
    date_hierarchy = 'target_date'
    # 공유 사용자 M2M 필드 선택 위젯 적용
    filter_horizontal = ('shared_users',)
    # 외래키 데이터가 많을 경우를 대비한 검색 팝업 위젯 적용
    raw_id_fields = ('author', 'family_group')