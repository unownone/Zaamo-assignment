from functools import reduce
from django.shortcuts import render
from rest_framework import generics, pagination
from django_filters.rest_framework import DjangoFilterBackend
import operator
from rest_framework.response import Response
from django.http import Http404
from videoapi.serializers import VideoSerializer
from videoapi.models import Video
from django.db.models import Q
# Create your views here.


class GetVideos(generics.ListAPIView):
    pagination_class = pagination.PageNumberPagination
    serializer_class = VideoSerializer


    def get_queryset(self):
        query = self.request.query_params.get("query", None)
        queryset = Video.objects.all()
        if query is not None or query!="":
            queryset2 = queryset.filter(id=query)
            if queryset2.exists():
                queryset = queryset2
            else:
                qrs = reduce(operator.or_,
                            (Q(title__contains=x)|
                            Q(description__contains=x) for x in query.split()))
                queryset = queryset.filter(qrs)
        
        return queryset
