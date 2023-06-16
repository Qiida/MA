

class Frame:

    def __init__(self, frameNr, annotations, image, idNr, autoPoint=None):
        self.frameNr = frameNr
        self.image = image
        self.idNr = idNr
        self.annotations = annotations
        self.autoPoint = autoPoint

