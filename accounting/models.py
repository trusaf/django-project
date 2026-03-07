from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# 1. 거래처 모델 (매출/매입처 관리)
class Partner(models.Model):
    name = models.CharField(max_length=100, verbose_name="거래처명")
    business_number = models.CharField(max_length=20, blank=True, verbose_name="사업자등록번호")
    contact_info = models.CharField(max_length=200, blank=True, verbose_name="연락처/이메일")
    memo = models.TextField(blank=True, verbose_name="메모")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "거래처"
        verbose_name_plural = "거래처 목록"

    def __str__(self):
        return self.name

# 2. 계정과목 모델
class Account(models.Model):
    ACCOUNT_TYPES = [
        ('ASSET', '자산'),
        ('LIABILITY', '부채'),
        ('EQUITY', '자본'),
        ('REVENUE', '수익'),
        ('EXPENSE', '비용'),
    ]

    code = models.CharField(max_length=10, unique=True, verbose_name="계정코드")
    name = models.CharField(max_length=50, verbose_name="계정과목명")
    account_type = models.CharField(max_length=15, choices=ACCOUNT_TYPES, verbose_name="분류")
    description = models.CharField(max_length=200, blank=True, verbose_name="설명")
    is_active = models.BooleanField(default=True, verbose_name="사용 여부")

    class Meta:
        ordering = ['code']
        verbose_name = "계정과목"
        verbose_name_plural = "계정과목 목록"

    def __str__(self):
        return f"[{self.code}] {self.name}"

# 3. 전표 메인 모델 (Header)
class JournalEntry(models.Model):
    date = models.DateField(verbose_name="거래 일자")
    title = models.CharField(max_length=200, verbose_name="거래 요약(적요)")
    evidence_file = models.FileField(upload_to='accounting/evidence/%Y/%m/', blank=True, null=True, verbose_name="증빙 파일")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="작성자")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="입력 일시")

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['date']),
        ]
        verbose_name = "전표"
        verbose_name_plural = "전표 목록"

    def __str__(self):
        return f"{self.date} - {self.title}"

# 4. 전표 상세/분개 모델 (Item)
class JournalItem(models.Model):
    entry = models.ForeignKey(JournalEntry, related_name='items', on_delete=models.CASCADE, verbose_name="소속 전표")
    account = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="계정과목")
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="거래처")
    description = models.CharField(max_length=200, blank=True, verbose_name="상세 적요")
    debit = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name="차변(입금/자산증가 등)")
    credit = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name="대변(출금/부채증가 등)")

    class Meta:
        verbose_name = "분개 상세"
        verbose_name_plural = "분개 상세 목록"

    def clean(self):
        # 차변과 대변 둘 다 입력되거나 둘 다 0인 경우 방지
        if self.debit > 0 and self.credit > 0:
            raise ValidationError("차변과 대변 중 하나만 금액을 입력해야 함.")
        if self.debit == 0 and self.credit == 0:
            raise ValidationError("차변 또는 대변에 금액을 입력해야 함.")

    def __str__(self):
        amount_type = "차변" if self.debit > 0 else "대변"
        amount = self.debit if self.debit > 0 else self.credit
        return f"[{amount_type}] {self.account.name}: {amount:,.0f}원"