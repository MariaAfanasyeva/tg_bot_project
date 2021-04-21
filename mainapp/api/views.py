from rest_framework.response import Response
from ..models import Bot
from .serializers import BotSerializer
from rest_framework.decorators import api_view


@api_view(['GET'])
def bots_list(request):
    bots = Bot.objects.all()
    serializer = BotSerializer(bots, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def bot_detail(request, pk):
    bot = Bot.objects.get(id=pk)
    serializer = BotSerializer(bot, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def bot_create(request):
    serializer = BotSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def bot_update(request, pk):
    bot = Bot.objects.get(id=pk)
    serializer = BotSerializer(instance=bot, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def bot_delete(request, pk):
    bot = Bot.objects.get(id=pk)
    bot.delete()
    return Response('Deleted')
