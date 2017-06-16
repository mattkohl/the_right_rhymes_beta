from django.db import models


PARTS_OF_SPEECH = [
    ('adjectival_phrase', 'adjectival phrase'),
    ('adjective', 'adjective'),
    ('adverb', 'adverb'),
    ('adverbial_phrase', 'adverbial_phrase'),
    ('combining_form', 'combining form'),
    ('interjection', 'interjection'),
    ('noun', 'noun'),
    ('phrase', 'phrase'),
    ('preposition', 'preposition'),
    ('prepositional_phrase', 'prepositional phrase'),
    ('intransitive_verb', 'intransitive verb'),
    ('intransitive_phrasal_verb', 'intransitive phrasal verb'),
    ('transitive verb', 'transitive verb'),
    ('transitive phrasal verb', 'transitive phrasal verb'),
    ('verb', 'verb'),
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
    mentioned_in = models.ManyToManyField("Example", related_name="mentions_sense", blank=True, symmetrical=False)
    derivatives = models.ManyToManyField("self", related_name="derives_from", blank=True, symmetrical=False)
    synonyms = models.ManyToManyField("self", related_name="+", blank=True, symmetrical=True)
    antonyms = models.ManyToManyField("self", related_name="+", blank=True, symmetrical=True)
    hypernyms = models.ManyToManyField("self", related_name="hyponyms", blank=True, symmetrical=False)
    meronyms = models.ManyToManyField("self", related_name="holonyms", blank=True, symmetrical=False)
    domains = models.ManyToManyField('Domain', related_name="+", blank=True, symmetrical=False)
    semantic_classes = models.ManyToManyField('SemanticClass', related_name="+", blank=True, symmetrical=False)
    dictionaries = models.ManyToManyField('Dictionary', related_name="+", blank=True, symmetrical=False)
    owner = models.ForeignKey("auth.User", related_name="senses")

    class Meta:
        ordering = ('headword', 'created',)

    def __str__(self):
        return self.headword + ', ' + self.part_of_speech + ' - ' + self.definition + ' [Published: ' + str(self.published) + ']'

    def to_dict(self):
        return {
            "pub_date": self.created,
            "headword": self.headword,
            "slug": self.headword_slug,
            "part_of_speech": self.part_of_speech,
            "definition": self.definition,
            "etymology": self.etymology,
            "notes": self.notes,
            "mentioned_in": [e.to_xref() for e in self.mentioned_in.all()],
            "derivatives": [s.to_xref() for s in self.derivatives.all()],
            "synonyms": [s.to_xref() for s in self.synonyms.all()],
            "antonyms": [s.to_xref() for s in self.antonyms.all()],
            "hypernyms": [s.to_xref() for s in self.hypernyms.all()],
            "meronyms": [s.to_xref() for s in self.meronyms.all()],
            "domains": [],
            "semantic_classes": []
        }

    def to_xref(self):
        return {
            "headword": self.headword,
            "slug": self.headword_slug,
        }


class Dictionary(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=500)
    senses = models.ManyToManyField('Sense', through=Sense.dictionaries.through, related_name='+', blank=True)
    name = models.CharField(max_length=1000)
    owner = models.ForeignKey("auth.User", related_name="dictionaries")

    class Meta:
        ordering = ('name', 'created',)

    def __str__(self):
        return self.name


class Artist(models.Model):

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000)
    also_known_as = models.ManyToManyField("self", related_name="+", blank=True, symmetrical=True)
    members = models.ManyToManyField("self", related_name="member_of", blank=True, symmetrical=False)
    origin = models.ForeignKey('Place', related_name="artists", blank=True, null=True)
    primary_songs = models.ManyToManyField('Song', related_name="+", blank=True)
    featured_songs = models.ManyToManyField('Song', related_name="+", blank=True)
    primary_examples = models.ManyToManyField('Example', related_name="+", blank=True)
    featured_examples = models.ManyToManyField('Example', related_name="+", blank=True)
    mentioned_in = models.ManyToManyField("Example", related_name="mentions_artist", blank=True, symmetrical=False)
    owner = models.ForeignKey("auth.User", related_name="artists")

    class Meta:
        ordering = ('name', 'created',)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "name": self.name,
            "slug": self.slug,
            "also_known_as": [a.to_xref() for a in self.also_known_as.all()],
            "members": [a.to_xref() for a in self.members.all()],
            "origin": self.origin.to_xref(),
            "primary_songs": [s.to_xref() for s in self.primary_songs.all()],
            "featured_songs": [s.to_xref() for s in self.featured_songs.all()],
            "primary_examples": [s.to_xref() for s in self.primary_examples.all()],
            "featured_examples": [s.to_xref() for s in self.featured_examples.all()],
            "mentioned_in": [e.to_xref() for e in self.mentioned_in.all()]

        }

    def to_xref(self):
        return {
            "name": self.name,
            "slug": self.slug,
        }

    def __iter__(self):
        yield "name", self.name
        yield "slug", self.slug


class Place(models.Model):

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000)
    full_name = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    contains = models.ManyToManyField("self", related_name="within", blank=True, symmetrical=False)
    mentioned_in = models.ManyToManyField("Example", related_name="mentions_place", blank=True, symmetrical=False)
    owner = models.ForeignKey("auth.User", related_name="places")

    class Meta:
        ordering = ('name', 'created',)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "name": self.name,
            "slug": self.slug,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "artists": [a.to_xref() for a in self.artists.all()],
            "contains": [p.to_xref() for p in self.contains.all()],
            "mentioned_in": [e.to_xref() for e in self.mentioned_in.all()]
        }

    def to_xref(self):
        return {
            "name": self.name,
            "slug": self.slug,
            "latitude": self.latitude,
            "longitude": self.longitude
        }


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    primary_artists = models.ManyToManyField(Artist, through=Artist.primary_songs.through, related_name="+")
    featured_artists = models.ManyToManyField(Artist, through=Artist.featured_songs.through, related_name="+", blank=True)
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

    def to_dict(self):
        return {
            "title": self.title,
            "slug": self.slug,
            "release_date": self.release_date,
            "release_date_string": self.release_date_string,
            "album": self.album,
            "primary_artists": [a.to_xref() for a in self.primary_artists.all()],
            "featured_artists": [a.to_xref() for a in self.featured_artists.all()],
            "lyrics": self.lyrics,
        }

    def to_xref(self):
        return {
            "title": self.title,
            "slug": self.slug,
            "release_date": self.release_date,
            "release_date_string": self.release_date_string,
            "album": self.album,
            "primary_artists": [a.to_xef() for a in self.primary_artists.all()],
            "featured_artists": [a.to_xref() for a in self.featured_artists.all()]
        }


class Example(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=1000)
    from_song = models.ForeignKey("Song", related_name="examples")
    primary_artists = models.ManyToManyField(Artist, through=Artist.primary_examples.through, related_name="+")
    featured_artists = models.ManyToManyField(Artist, through=Artist.featured_examples.through, related_name="+", blank=True)
    text = models.CharField(max_length=1000)
    owner = models.ForeignKey("auth.User", related_name="examples")

    class Meta:
        ordering = ["text"]

    def __str__(self):
        return str(self.text)

    def to_dict(self):
        return {
            "slug": self.slug,
            "song": self.from_song.title,
            "primary_artists": [a.to_xref() for a in self.primary_artists.all()],
            "featured_artists": [a.to_xref() for a in self.featured_artists.all()],
            "text": self.text
        }

    def to_xref(self):
        return {
            "slug": self.slug,
            "song": self.from_song.title,
            "primary_artists": [a.to_xref() for a in self.primary_artists.all()],
            "featured_artists": [a.to_xref() for a in self.featured_artists.all()],
            "text": self.text,
            "annotations": [a.to_xref() for a in self.annotations.all()]
        }


class Domain(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000)
    senses = models.ManyToManyField('Sense', through=Sense.domains.through, related_name='+', blank=True)
    broader = models.ManyToManyField("self", related_name="narrower", blank=True, symmetrical=False)
    owner = models.ForeignKey("auth.User", related_name="domains")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "name": self.name,
            "slug": self.slug
        }

    def to_xref(self):
        return {
            "name": self.name,
            "slug": self.slug
        }


class SemanticClass(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000)
    senses = models.ManyToManyField('Sense', through=Sense.semantic_classes.through, related_name='+', blank=True)
    broader = models.ManyToManyField("self", related_name="narrower", blank=True, symmetrical=False)
    owner = models.ForeignKey("auth.User", related_name="semantic_classes")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Semantic Classes"

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "name": self.name,
            "slug": self.slug
        }

    def to_xref(self):
        return {
            "name": self.name,
            "slug": self.slug
        }


class Annotation(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000)
    offset = models.IntegerField()
    example = models.ForeignKey("Example", related_name="annotations")
    sense = models.ForeignKey("Sense", related_name="annotations", blank=True, null=True)
    artist = models.ForeignKey("Artist", related_name="annotations", blank=True, null=True)
    place = models.ForeignKey("Place", related_name="annotations", blank=True, null=True)
    rhymes = models.ManyToManyField("self", related_name="rhymes", blank=True, symmetrical=True)
    owner = models.ForeignKey("auth.User", related_name="annotations")

    class Meta:
        ordering = ["text"]

    def __str__(self):
        return self.text + " [" + self.example.text + "]"

    def __iter__(self):
        yield "text", self.text
        yield "slug", self.slug
        yield "start_position", self.offset
        # yield "example", self.example.to_xref()
        # yield "sense", self.sense.to_xref()
        # yield "artist", self.artist.to_xref()
        # yield "place", self.place.to_xref()
        # yield "rhymes", [r.to_xref() for r in self.rhymes.all()]

    def to_dict(self):
        return {
            "text": self.text,
            "slug": self.slug,
            "start_position": self.offset,
            "example": self.example.to_xref(),
            "sense": self.sense.to_xref(),
            "artist": self.artist.to_xref(),
            "place": self.place.to_xref(),
            "rhymes": [r.to_xref() for r in self.rhymes.all()]
        }

    def to_xref(self):
        return {
            "text": self.text,
            "slug": self.slug,
            "start_position": self.offset,
            "sense": self.sense.to_xref(),
            "artist": self.artist.to_xref(),
            "place": self.place.to_xref(),
            "rhymes": [r.to_xref() for r in self.rhymes.all()]
        }