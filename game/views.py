from django.shortcuts import render, HttpResponse, redirect
from game.models import *
from django.contrib import messages
# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    elif request.method == "POST":
        roomId = request.POST.get("room-id", None)
        playerName = request.POST.get("player-name", "Unknown Player")
        if(roomId):
            try:
                room = Room.objects.get(id=roomId)
                return redirect(f"/game/{room.id}/{playerName}/")
            except Room.DoesNotExist:
                messages.error(request, "Room does not exist.")
                return redirect("/")
                
        else:
            room = Room.objects.create()
            return redirect(f"/game/{room.id}/{playerName}/")


def game(request, id=None, name=None):
    try:
        room = Room.objects.get(id=id)
        return render(request, "game.html", {"room": room, "name": name})
    except Room.DoesNotExist:
        messages.error(request, "Room does not exist. You fool!!")
        return redirect("/")