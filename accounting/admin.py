from django.contrib import admin
from .models import Partner, Account, JournalEntry, JournalItem

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'business_number', 'contact_info', 'created_at')
    search_fields = ('name', 'business_number')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'account_type', 'is_active')
    list_filter = ('account_type', 'is_active')
    search_fields = ('code', 'name')
    ordering = ('code',)

# 전표 입력 시 하단에 분개 상세(Item)를 여러 줄 입력할 수 있는 인라인 설정
class JournalItemInline(admin.TabularInline):
    model = JournalItem
    extra = 2  # 기본으로 표시할 빈 입력 칸 수 (차변, 대변 최소 2줄 필요)
    raw_id_fields = ('account', 'partner') # 데이터가 많아질 경우를 대비한 팝업 검색 위젯

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'created_by', 'created_at')
    list_filter = ('date', 'created_by')
    search_fields = ('title',)
    date_hierarchy = 'date'
    inlines = [JournalItemInline]
    raw_id_fields = ('created_by',)