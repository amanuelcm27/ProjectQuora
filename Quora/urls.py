from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path("profile/<int:pk>/", create_or_show_profile, name="profile"),
    path("edit_profile/<int:pk>/",edit_profile,name="edit_profile"),
    path("question/", question, name="question"),
    path("edit_question/<int:pk>/<str:flag>/", edit_question,name="edit_question"),
    path("delete_question/<int:pk>/<str:flag>/", delete_question,name="delete_question"),
    path("answers/",requested_answers,name="requested_answers"),
    path("answer/<int:pk>/",answer,name="answer"),
    path("answer/<int:pk>/media/answer_images/", handle_answer_images, name="handle_answer_images"),
    path("answer/<str:pk>/", view_answer, name="view_answer"),
    path("edit_answer/<int:pk>/", edit_answer,name="edit_answer"),
    path("edit_answer/<int:pk>/media/answer_images/",handle_answer_images, name="handle_answer_images"),
    path("delete_answer/<int:pk>/<str:flag>/", delete_answer, name="delete_answer"),
    path("upvote_downvote/<int:pk>/<str:flag>/", upvote_downvote_answer, name="upvote_downvote"),
    path("follow/<str:pk>/<str:flag>/", follow_user, name="follow"),
    path("following/", view_following, name="following"),
    path("comment/<int:answer_pk>/", comment , name="comment"),
    path("reply/<int:comment_pk>/<int:answer_pk>/",reply, name="reply"),
    path("all_replies/<int:comment_pk>/",all_replies, name="all_replies"),
    path("delete_comment/<int:commentId>/<str:flag>/",delete_comment,name="delete_comment"),
    path("edit_comment/<int:commentId>/",edit_comment, name="edit_comment"),
    path("create_space/",create_space,name="create_space"),
    path("spaces/",view_spaces,name="spaces"),
    path("follow_space/<int:space_id>/",follow_space,name="follow_space"),
    path("message/",create_message,name="message"),
    path("received_msg/<int:pk>/",received_message,name="received_msg"),
    path("search/",search,name="search")
]
