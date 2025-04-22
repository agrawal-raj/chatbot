from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import render
from .models import Conversation , Message
from .chatbot_app import DjangoChatBot
import json

bot  = DjangoChatBot()
# Create your views here.
def chat(request):
    conversation, created = Conversation.objects.get_or_create(
        user = request.user,
        defaults = {'user': request.user}
    )

    #get message for this conversation
    message = Message.objects.filter(conversation= conversation)

    return render(request, 'chat.html', {'messages': messages})

def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message')

        conversation  = Conversation.objects.filter(user=request.user).latest('started_at')

        Message.objects.create(
            conversation = conversation,
            text= user_input,
            is_user=True
        )

        #get bot response
        bot_response = bot.get_response(user_input)

        Message.objects.create(
            conversation = conversation,
            text = bot_response,
            is_user =False
        )
        return JsonResponse({'response': bot_response})
    return JsonResponse({'error': 'Invalid request'}, status=400)