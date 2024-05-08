from django.db import models

class RomanTemple(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    dedicatee = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    setting = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    modernplace = models.CharField(max_length=255)
    ancientplace = models.CharField(max_length=255)
    pleiadesplace = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    orientation = models.CharField(max_length=255)
    compass = models.CharField(max_length=255)
    geocertainty = models.IntegerField()
    vowed = models.IntegerField()
    date = models.CharField(max_length=255)
    startdateearly = models.IntegerField()
    startdatelate = models.IntegerField()
    century = models.CharField(max_length=255)
    enddate = models.CharField(max_length=255)
    preceded = models.CharField(max_length=255)
    succeeded = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    dedicationday = models.CharField(max_length=255)
    deitytype = models.CharField(max_length=255)
    culture = models.CharField(max_length=255)
    style = models.CharField(max_length=255)
    extant = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    meetings = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    vici = models.CharField(max_length=255)
    pleiades = models.CharField(max_length=255)
    dare = models.CharField(max_length=255)
    arachne = models.CharField(max_length=255)
    livius = models.CharField(max_length=255)
    wikipedia = models.CharField(max_length=255)
    wikidata = models.CharField(max_length=255)
    digitalromanforum = models.CharField(max_length=255)
    digitalesforumromanum = models.CharField(max_length=255)
    trismegistos = models.CharField(max_length=255)
    ads = models.CharField(max_length=255)
    cona = models.CharField(max_length=255)
    topostext = models.CharField(max_length=255)
    sls = models.CharField(max_length=255)
    patrimonium = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name
