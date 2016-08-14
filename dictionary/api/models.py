from django.db import models


PARTS_OF_SPEECH = [
    ('adjective', 'adjective'),
    ('combining_form', 'combining form'),
    ('interjection', 'interjection'),
    ('noun', 'noun'),
    ('phrase', 'phrase'),
    ('verb', 'verb')
]


class Sense(models.Model):

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    headword = models.CharField(max_length=500)
    headword_slug = models.SlugField(max_length=500)
    published = models.BooleanField(default=False)
    part_of_speech = models.CharField(choices=PARTS_OF_SPEECH, max_length=500)
    definition = models.CharField(max_length=2000, default="__stub_definition__")
    etymology = models.CharField(max_length=2000, null=True, blank=True)
    notes = models.CharField(max_length=2000, null=True, blank=True)
    synonyms = models.ManyToManyField("self", related_name="+", blank=True, symmetrical=True)
    antonyms = models.ManyToManyField("self", related_name="+", blank=True, symmetrical=True)
    hypernyms = models.ManyToManyField("self", related_name="hyponyms", blank=True, symmetrical=False)
    meronyms = models.ManyToManyField("self", related_name="holonyms", blank=True, symmetrical=False)
    owner = models.ForeignKey("auth.User", related_name="senses")

    class Meta:
        ordering = ('headword', 'created',)

    def __str__(self):
        return self.headword + ' - ' + self.definition + ' [Published: ' + str(self.published) + ']'


class Artist(models.Model):

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000)
    also_known_as = models.ManyToManyField("self", related_name="+", blank=True, symmetrical=True)
    members = models.ManyToManyField("self", related_name="member_of", blank=True, symmetrical=False)
    origin = models.ManyToManyField('Place', related_name="+", blank=True)
    primary_songs = models.ManyToManyField('Song', related_name="+", blank=True)
    featured_songs = models.ManyToManyField('Song', related_name="+", blank=True)
    owner = models.ForeignKey("auth.User", related_name="artists")

    class Meta:
        ordering = ('name', 'created',)

    def __str__(self):
        return self.name


class Place(models.Model):

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000)
    full_name = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    artists = models.ManyToManyField(Artist, through=Artist.origin.through, related_name="+", blank=True)
    contains = models.ManyToManyField("self", related_name="within", blank=True, symmetrical=False)
    owner = models.ForeignKey("auth.User", related_name="places")

    class Meta:
        ordering = ('name', 'created',)

    def __str__(self):
        return self.name


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    primary_artist = models.ManyToManyField(Artist, through=Artist.primary_songs.through, related_name="+")
    feat_artist = models.ManyToManyField(Artist, through=Artist.featured_songs.through, related_name="+", blank=True)
    release_date = models.DateField()
    release_date_string = models.CharField(max_length=10)
    album = models.CharField(max_length=1000)
    lyrics = models.TextField(null=True, blank=True)
    release_date_verified = models.BooleanField(default=False)
    owner = models.ForeignKey("auth.User", related_name="songs")

    class Meta:
        ordering = ["title", "album"]

    def __str__(self):
        return '"' + str(self.title) + '" (' + str(self.album) + ') '
