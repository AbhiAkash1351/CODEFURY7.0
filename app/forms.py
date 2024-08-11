from django import forms
from .models import Post
from .models import ChatMessage
from .models import HelpSeek


class HelpSeekForm(forms.ModelForm):
    class Meta:
        model = HelpSeek
        fields = ['name', 'age', 'mobile_number', 'purpose',
                  'payment_info', 'help_needed', 'raise_fund']
        widgets = {
            'payment_info': forms.Textarea(attrs={'rows': 2}),
            'help_needed': forms.Textarea(attrs={'rows': 4}),
            'purpose': forms.Textarea(attrs={'rows': 2}),
        }


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type a message...',
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type a message...',
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
