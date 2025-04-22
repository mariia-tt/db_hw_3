SELECT Composition.name, Song.lyrics FROM Song
JOIN Composition ON Song.composition_identifier = Composition.composition_identifier
WHERE Song.feat IS NOT NULL