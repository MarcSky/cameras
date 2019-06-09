import math
from server.camera_utils import Camera
from random import randint


class CameraManager():
    def __init__(self, cameras):
        self.cameras = cameras
        self.numberOfCameras = len(cameras)
        self.area = 0.0

    def getCamera(self, index):
        if self.numberOfCameras > index + 1:
            return self.cameras[index]
        return self.cameras[0]

    def setCamera(self, camera, index):
        self.cameras.insert(index, camera)
        self.area = 0.0

    def getArea(self):
        if self.area == 0.0:
            currentArea = 0.0
            for i, camera in enumerate(self.cameras):
                if not isinstance(camera, Camera):
                    continue

                first_camera = camera
                if i + 1 < self.numberOfCameras:
                    second_camera = self.cameras[i]
                else:
                    second_camera = self.cameras[0]

                if not isinstance(second_camera, Camera):
                    continue

                currentArea += first_camera.polygon.intersection(second_camera.polygon).area
            self.area = currentArea
        return self.area


class SimulatedAnnealing():
    def __init__(self, cameraManager):
        self.cameraManager = cameraManager

    def acceptanceProbability(self, energy, newEnergy, temperature):
        if newEnergy < energy:
            return 1.0
        return math.exp((energy - newEnergy) / temperature)

    def start(self):
        temp = 1000.0
        coolingRate = 0.1

        bestSolution = self.cameraManager

        while (temp > 1):
            newSolution = self.cameraManager

            first_camera_index = randint(0, self.cameraManager.numberOfCameras)
            second_camera_index = randint(0, self.cameraManager.numberOfCameras)

            first_camera_swap = newSolution.cameras[first_camera_index]
            second_camera_swap = newSolution.cameras[first_camera_index]

            newSolution.setCamera(first_camera_swap, second_camera_index)
            newSolution.setCamera(second_camera_swap, first_camera_index)

            currentEnergy = bestSolution.getArea()
            neighborEnergy = newSolution.getArea()

            if self.acceptanceProbability(currentEnergy, neighborEnergy, temp) > randint(0, 1000):
                bestSolution = newSolution

            temp *= 1 - coolingRate

        return bestSolution.cameras
