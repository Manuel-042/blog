# from django.db import models
# from django_editorjs import EditorJsField
# from account.models import Blog as AccountBlog

# class Blog(AccountBlog):
#     blogpost = EditorJsField(editorjs_config={
#         "tools": {
#             "Image": {
#                 "config": {
#                     "endpoints": {
#                         "byFile": '/uploadImageFile/',
#                         "byUrl": "/uploadImageUrl/",
#                     },
#                     "additionalRequestHeaders": [{"Content-Type": 'multipart/form-data'}]
#                 }
#             }
#         }
#     })

#     class Meta:
#         proxy = True 