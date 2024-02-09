from typing import List

from django.db.models import QuerySet

from .serializer import BreakfastSerializer


class BreakfastReportProvider:
    """Класс формирования данных по коуч-завтраку для отчета."""

    serializer_class = BreakfastSerializer

    def __init__(self, queryset: QuerySet):
        self._qs = queryset
        self._data = None

    @property
    def data(self) -> List[dict]:
        """Данные провайдера."""
        if self._data is None:
            self._data = self.collect()

        return self._data

    def get_queryset(self) -> QuerySet:
        """Метод формирования кверисета."""
        qs = self._qs.prefetch_related('users')

        return qs

    def collect(self) -> List[dict]:
        """Метод сборки данных для отчета."""
        return self.serializer_class(
            self.get_queryset(),
            many=True,
        ).data
