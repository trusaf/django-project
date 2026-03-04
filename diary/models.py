from django.db import models
from django.conf import settings

# 가족/그룹 관리를 위한 모델 (가족 일기 권한 제어용)
class FamilyGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="가족/그룹명")
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='family_groups', 
        verbose_name="소속 멤버"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "가족 그룹"
        verbose_name_plural = "가족 그룹 목록"

    def __str__(self):
        return self.name

# 통합 일기장 모델
class Diary(models.Model):
    DIARY_TYPE_CHOICES = [
        ('100Y', '100년 일기 (개인)'),
        ('COLLAB', '함께 쓰는 일기 (특정 사용자 공유)'),
        ('FAMILY', '가족 일기 (가족 그룹 공유)'),
    ]

    # 기본 정보
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='my_diaries',
        verbose_name="작성자"
    )
    diary_type = models.CharField(
        max_length=10, 
        choices=DIARY_TYPE_CHOICES, 
        default='100Y',
        verbose_name="일기 유형"
    )

    # 내용 및 날짜
    target_date = models.DateField(verbose_name="일기 대상 날짜", help_text="실제 일기에 해당하는 날짜 (100년 일기 기준점)")
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="본문 내용")

    # 권한 제어 및 공유 필드
    shared_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        blank=True, 
        related_name='shared_diaries', 
        verbose_name="공유 대상 사용자",
        help_text="함께 쓰는 일기 선택 시 지정"
    )
    family_group = models.ForeignKey(
        FamilyGroup, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='family_diaries',
        verbose_name="지정 가족 그룹",
        help_text="가족 일기 선택 시 지정"
    )

    # 메타 정보
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        # 날짜 내림차순 정렬을 기본값으로 설정
        ordering = ['-target_date', '-created_at']
        # 검색 성능 향상을 위한 데이터베이스 인덱스 추가
        indexes = [
            models.Index(fields=['target_date']),
            models.Index(fields=['diary_type']),
            models.Index(fields=['author']),
        ]
        verbose_name = "일기"
        verbose_name_plural = "일기 목록"

    def __str__(self):
        return f"[{self.get_diary_type_display()}] {self.target_date} - {self.title}"