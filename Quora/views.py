from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.timesince import timesince
from django.db.models import Q
from datetime import  datetime
from django.core import serializers

@login_required
def index(request):
    questions = Question.objects.all().order_by("date_created")
    followingObjects = Follow.objects.filter(follower=request.user)
    following = [fol.followee for fol in followingObjects]
    best_answers = {}
    for question in questions:
        answers = question.answer_set.all()
        # store list of upvotes for all answers for a question
        upvotes_list = [upvote.upvotes.count() for upvote in answers]
        if answers:
            for answer in answers:
                if answer.upvotes.count() == max(upvotes_list):
                    best_answers[question] = answer
        else:
            best_answers[question] = None
    followed_spaces = Space.objects.filter(follow=request.user)
    context = {"questions": questions, "best_answers": best_answers,"spaces":followed_spaces,"following":following}
    return render(request, "Quora/home.html", context)


def register(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = form.cleaned_data['email']
            new_user.save()
            login(request, new_user)
            return redirect("index")
    context = {"form": form}
    return render(request, "registration/register.html", context)


@login_required
def create_or_show_profile(request, pk):
    user = User.objects.get(id=pk)
    questions = Question.objects.filter(creator=user)
    answers= Answer.objects.filter(responder = user)
    followers = Follow.objects.filter(followee=user)
    following = Follow.objects.filter(follower=user)
    show_profile = False
    profile_form = None
    profile_info = None
    credentials = []
    try:
        profile_info = Profile.objects.get(user=user.id)
        show_profile = True
        credentials = [
                {'icon': 'fas fa-suitcase', 'label': 'Profession', 'value': profile_info.profession},
                {'icon': 'fas fa-graduation-cap', 'label': 'Degree', 'value': profile_info.degree_type},
                {'icon': 'fas fa-map-marker', 'label': 'Lives in', 'value': profile_info.location},
                {'icon': 'fas fa-calendar', 'label': 'Joined', 'value': profile_info.date_joined.strftime("%b %d,%Y")}
            ]
    except Profile.DoesNotExist:
        profile_form = ProfileForm()
        if request.method == "POST":
            profile_form = ProfileForm(request.POST, request.FILES)
            if profile_form.is_valid():
                new_profile = profile_form.save(commit=False)
                new_profile.user = user
                new_profile.save()
                return redirect("index")

    context = {"profile_form": profile_form,
               "profile_info": profile_info, "show_profile": show_profile,
               "questions": questions,"answers":answers,
               "followers":followers , "following":following, "credentials":credentials}
    return render(request, "Quora/profile_form.html", context)


@login_required
def edit_profile(request, pk):
    profile = Profile.objects.get(user=pk)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():

            # # If a new file is provided, overwrite the existing file
            # if 'avatar' in request.FILES:
            #     profile.avatar.delete()  # Delete the existing file
            #     profile.avatar = request.FILES['avatar']
            print(request.FILES)
            form.save()
            return redirect('profile', request.user.id)
    context = {"form": form, "question": question}
    return render(request, 'Quora/edit_profile.html', context)



@login_required
def question(request):
    users = User.objects.all()
    if request.method == "POST":
        content = request.POST.get("content")
        topic = request.POST.get("topic")
        selected_user_ids = request.POST.getlist("to")
        new_question = Question.objects.create(
            content=content,
            topic=topic,
            creator=request.user
        )
        new_question.to.set(User.objects.filter(id__in=selected_user_ids))
        return redirect("view_answer" , new_question.content)
    # if request.method == "POST":
    #     form = QuestionForm(request.POST)
    #     if form.is_valid():
    #         form.user = request.user  # Set the 'user' attribute on the form
    #         form.save()
    #         return redirect("index")
    # else:
    form = QuestionForm()
    context = {"form": form,"users":users}
    return render(request, "Quora/question_form.html", context)


@login_required
def edit_question(request, pk, flag):
    question = Question.objects.get(id=pk)
    form = EditQuestionForm(instance=question)
    if request.method == "POST":
        if flag == "edit":
            form = EditQuestionForm(data=request.POST, instance=question)
            if form.is_valid():
                form.save()
                return redirect("profile",pk=request.user.id)

    context = {"form":form , "flag":flag, "question":question}
    return render(request, "Quora/edit_question.html", context)


@login_required
def delete_question(request,pk,flag):
    question = Question.objects.get(id=pk)
    if flag == 'confirm':
        question.delete()
        return redirect("profile", pk=request.user.id)
    context = {"question": question}
    return render(request, "Quora/edit_question.html", context)


@login_required
def requested_answers(request):
    user = request.user
    questions = user.question_for.all()
    context = {"questions": questions}
    return render(request, 'Quora/answer.html', context)


@login_required
def answer(request, pk):
    question = Question.objects.get(id=pk)
    form = AnswerForm()
    if request.method == "POST":
        form = AnswerForm(request.POST,request.FILES)
        if form.is_valid():
            content = form.cleaned_data['content']
            Answer.objects.create(content=content, question=question,responder=request.user)
            # images = request.FILES.getlist('images')
            # print(images)
            # for image in images:
            #     Image.objects.create(img_answer=answer, image=image)
            return redirect('view_answer',question.content)
    context = {"form": form, "question": question}
    return render(request, 'Quora/answer_page.html', context)


@login_required
@csrf_exempt
def handle_answer_images(request, pk):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        # Create the destination path
        destination_path = os.path.join(settings.MEDIA_ROOT, 'answer_images', uploaded_file.name)
        with open(destination_path, 'wb+') as destination:  # Save the uploaded file to the destination path
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        # Construct the URL for the uploaded image
        uploaded_url = os.path.join(settings.MEDIA_URL, 'answer_images', uploaded_file.name)
        return JsonResponse({'location': uploaded_url})  # Return a JSON response with the uploaded image URL

    # Handle other cases, e.g., if the request is not a POST request or no file is provided
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def view_answer(request, pk):
    question = Question.objects.get(content=pk)
    followingObjects = Follow.objects.filter(follower=request.user)
    following = [fol.followee for fol in followingObjects]
    answers = question.answer_set.all().order_by("-date_created")
    context = {'question': question, 'answers': answers, "following": following}
    return render(request, 'Quora/view_answer.html', context)


@login_required
def edit_answer(request, pk):
    answer = Answer.objects.get(id=pk)
    question = answer.question
    form = AnswerForm(instance=answer)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect('view_answer', answer.question.content)
    context = {"form": form, "question": question}
    return render(request, 'Quora/edit_answer.html', context)


@login_required
def delete_answer(request,pk,flag):
    answer = Answer.objects.get(id=pk)
    question = answer.question
    if flag == "confirm":
        answer.delete()
        return redirect('view_answer', question.content)
    context = {"question": question, "answer":answer, "flag":flag}
    return render(request, 'Quora/edit_answer.html', context)


@login_required
def upvote_downvote_answer(request, pk, flag):
    answer = Answer.objects.get(id=pk)
    user = request.user
    if flag == "upvote":
        if user not in answer.upvotes.all():
            answer.upvote(user)
        elif user in answer.upvotes.all():
            answer.upvotes.remove(user)

    elif flag == "downvote":
        if user not in answer.downvotes.all():
            answer.downvote(user)
        elif user in answer.downvotes.all():
            answer.downvotes.remove(user)

    upvote_count = answer.upvotes.count()
    downvote_count = answer.downvotes.count()
    user_has_upvoted = user in answer.upvotes.all()
    data = {"upvote_count": upvote_count, "user_has_upvoted": user_has_upvoted, "downvote_count": downvote_count}
    return JsonResponse(data)


@login_required
def follow_user(request, pk, flag):
    follower = request.user
    followee = get_object_or_404(User, username=pk)
    if flag == "unfollow":
        userToDelete = Follow.objects.filter(follower=follower, followee=followee)
        userToDelete.delete()
    else:
        Follow.objects.create(follower=follower, followee=followee)
    data = {"flag": flag}
    return JsonResponse(data)


@login_required
def view_following(request):
    user = request.user
    following = Follow.objects.filter(follower=user)
    user_answers = {}
    for users in following:
        answers = Answer.objects.filter(responder=users.followee)
        user_answers[users.followee] = answers.latest("date_created")
    context = {"following": following,  "user_answers":user_answers}
    return render(request, 'Quora/following.html', context)


@login_required
def comment(request, answer_pk):
    creator = request.user
    answer = get_object_or_404(Answer, id=answer_pk)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            comment = Comment.objects.create(
                answer=answer,
                content=content,
                creator=creator
            )
            return JsonResponse(
                {"fail": 0,
                 "creator_id":creator.id,
                 "creator": creator.username,
                 "content": content,
                 "comment_id": comment.id,
                 "comment_date": timesince(comment.date_created, timezone.now()),
                 "avatar": comment.creator.profile_user.avatar.url}
            )
        else:
            return JsonResponse({"fail": 1, "message": "comment cannot be blank."})


@login_required
def reply(request, comment_pk, answer_pk):
    to_comment = get_object_or_404(Comment,id=comment_pk)
    creator = request.user
    answer = get_object_or_404(Answer,id=answer_pk)
    if request.method == "POST":
        Comment.objects.create (
            answer=answer, content=request.POST.get("content"), creator=creator, reply=to_comment
        )
    return redirect("index")


@login_required
def all_replies(request, comment_pk):
    comment = get_object_or_404(Comment, id=comment_pk)
    replies = Comment.objects.filter(
        reply=comment
    )
    # data = {"replies":[]}
    # for reply in replies:
    #     data["replies"].append(reply.content)
    data = {"replies": [{
                "creator_id":reply.creator.id,
                "content": reply.content,
                "creator": reply.creator.username,  # Adjust as needed
                "date_created": timesince(reply.date_created, timezone.now()),
                "avatar":reply.creator.profile_user.avatar.url}
            for reply in replies
        ]
    }
    return JsonResponse(data)


@login_required
def delete_comment(request, commentId, flag):
    comment = get_object_or_404(Comment, id=commentId)
    if flag == "confirm":
        comment.delete()
        return JsonResponse({'message': 'Comment deleted successfully.'})
    # Handle other cases or return an appropriate response
    return JsonResponse({'message': 'Invalid request.'}, status=400)


@login_required
def edit_comment(request,commentId) :
    comment = get_object_or_404(Comment, id=commentId)
    if request.method == "POST":
        comment.content = request.POST.get("content")
        comment.save()
        return redirect("index")


@login_required
def create_space(request):
    creator = request.user
    if request.method == "POST":
        spaces = Space.objects.filter(name=request.POST.get('name').lower())
        if not spaces:
            new_space = Space.objects.create(
                name=request.POST.get("name").lower(),
                creator=creator,
                description=request.POST.get("description")
            )
    return redirect("index")


@login_required
def view_spaces(request):
    spaces = Space.objects.all()
    return render(request,"Quora/spaces.html",{"spaces":spaces})


@login_required
def follow_space(request,space_id):
    spaces = get_object_or_404(Space,id=space_id)
    followee = request.user
    spaces.follow.add(followee)
    return redirect("spaces")


@login_required
def create_message(request):
    active_user = request.user
    users = User.objects.all()
    senders_receivers = User.objects.filter(
        Q(sender__receiver=active_user) | Q(receiver__sender=active_user)
    ).distinct()
    latest_message_sent = active_user.sender.order_by('-date_created').first()
    if request.method == "POST":
        receiver = request.POST.get("messageTo")
        user = User.objects.get(username=receiver)
        content = request.POST.get("message")
        message = Message.objects.create(sender=active_user, receiver=user, content=content)
        return JsonResponse(

            {"fail": 0,
             "message": content,
             "message_id": message.id,
             "date_created": timesince(message.date_created, timezone.now())}
        )
    context = {"users": users, "interactors": senders_receivers,"latest":latest_message_sent}

    return render(request, "Quora/message.html", context)


@login_required
def received_message(request, pk):
    user = get_object_or_404(User, id=pk)
    onchatpage = True
    received = Message.objects.filter(sender=user,receiver=request.user)
    sent = Message.objects.filter(sender=request.user, receiver=user)
    all_messages = received.union(sent)
    all_messages = all_messages.order_by('-date_created')
    data = {"messages": [{
        "sender_id": message.sender.id,
        "receiver_id": message.receiver.id,
        "date_created":timesince(message.date_created, timezone.now(),),
        "content": message.content,
        }
        for message in all_messages
    ]
    }
    context = {"all_messages":all_messages,"onchatpage":onchatpage}
    return JsonResponse(data)


@login_required
def search(request):
    search_term = request.GET.get("search") or ""
    search_results = Question.objects.filter(content__icontains=search_term)
    context = {"search_results":search_results,"search_term":search_term}
    return render(request,"Quora/search_page.html",context)
