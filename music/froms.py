from django import forms
from playlist.models import Playlist
from .models import Song


class SongUploadForm(forms.ModelForm):
    playlist = forms.ModelChoiceField(queryset=Playlist.objects.none(), required=True)

    class Meta:
        model = Song
        fields = ["name", "genre", "song_file"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(SongUploadForm, self).__init__(*args, **kwargs)
        self.fields["playlist"].queryset = Playlist.objects.filter(user=user)
