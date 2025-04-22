SELECT Composition.name, Song.explicit FROM Song
JOIN Composition ON Song.composition_identifier = Composition.composition_identifier
WHERE Song.explicit = 1