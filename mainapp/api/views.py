from rest_framework.response import Response
from ..models import Bot
from .serializers import BotSerializer
from rest_framework.decorators import api_view
import logging
from rest_framework import generics

logger = logging.getLogger(__name__)


class GetAllBotsList(generics.ListAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer


class GetBotDetail(generics.RetrieveAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
# @api_view(['GET'])
# def bot_detail(request, pk):
#     bot = Bot.objects.get(id=pk)
#     serializer = BotSerializer(bot, many=False)
#     logger.info('User viewed bot with id=%s', pk)
#     return Response(serializer.data)


@api_view(['POST'])
def bot_create(request):
    serializer = BotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    logger.info('User added a new bot')
    return Response(serializer.data)


@api_view(['POST'])
def bot_update(request, pk):
    bot = Bot.objects.get(id=pk)
    serializer = BotSerializer(instance=bot, data=request.data)
    if serializer.is_valid():
        serializer.save()
    logger.info('User updated bot with id=%s', pk)
    return Response(serializer.data)


@api_view(['DELETE'])
def bot_delete(request, pk):
    bot = Bot.objects.get(id=pk)
    bot.delete()
    logger.info('User deleted bot with id=%s', pk)
    return Response('Deleted')
