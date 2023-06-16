from src.data.tracklet.boxes import YoloBox


class YoloObject:

    def __init__(self, ID, objectType, box):
        self.ID = ID
        self.objectType = objectType
        self.box = box


class Car(YoloObject):
    def __init__(self, ID, box):
        super().__init__(
            ID=ID, objectType="car", box=box
        )


class Person(YoloObject):
    def __init__(self, ID, box):
        super().__init__(ID, "person", box)


class Truck(YoloObject):
    def __init__(self, ID, box):
        super().__init__(ID, "truck", box)


class StopSign(YoloObject):
    def __init__(self, ID, box):
        super().__init__(ID, "stop sign", box)


class TrafficLight(YoloObject):
    def __init__(self, ID, box):
        super().__init__(ID, "traffic light", box)


class Umbrella(YoloObject):
    def __init__(self, ID, box):
        super().__init__(ID, "umbrella", box)


class Skateboard(YoloObject):
    def __init__(self, ID, box):
        super().__init__(ID, "skateboard", box)


class Cyclist(YoloObject):
    def __init__(self, ID, box):
        super().__init__(
            ID=ID, objectType="cyclist", box=box
        )


class CyclistFactory:
    def __init__(self, person=None, bicycle=None):
        self.person = person
        self.bicycle = bicycle

    def produce(self, imageIndex):
        if self.__bicycleIsSeated():
            return True, Cyclist(
                ID=self.person.ID,
                box=self.__buildBox(imageIndex),
            )
        return False, None

    def __buildBox(self, imageIndex):
        u0 = [
            self.person.box.u[0],
            self.bicycle.box.u[0]
        ]
        u1 = [
            self.person.box.u[1],
            self.bicycle.box.u[1]
        ]
        v0 = [
            self.person.box.v[0],
            self.bicycle.box.v[0]
        ]
        v1 = [
            self.person.box.v[1],
            self.bicycle.box.v[1]
        ]

        return YoloBox(
            u=(
                min(u0), max(u1)
            ),
            v=(
                min(v0), max(v1)
            ),
            imageIndex=imageIndex
        )

    def __bicycleIsSeated(self):
        return self.person is not None and self.bicycle is not None
