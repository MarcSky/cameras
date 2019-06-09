import math
from camera_utils import Camera
from random import randint
import copy
import random
from shapely.geometry import Polygon


class CameraManager():
    def __init__(self, cameras, count=40):
        self.cameras = cameras
        self.numberOfCameras = count #len(cameras)
        self.area = 0.0

    def getCamera(self, index):
        if self.numberOfCameras > index + 1:
            return self.cameras[index]
        return self.cameras[0]

    def setCamera(self, camera, index):
        self.cameras.insert(index, camera)
        self.area = 0.0

    def getArea(self):
        area = 0.0
        for c in self.cameras:
            area += c.area
        return area


class SimulatedAnnealing():
    def __init__(self, cameraManager, full_buildings):
        self.cameraManager = cameraManager
        self.full_buildings = full_buildings

    def acceptanceProbability(self, energy, newEnergy, temperature):
        if newEnergy < energy:
            return 1.0
        return math.exp((energy - newEnergy) / temperature)

    def newGeneration(self, cameras):
        for c in cameras:
            c.refresh_polygon()

            for b in self.full_buildings:
                p = Polygon(b.polygon)
                c.screen_building(p)
        return cameras

    def start(self):
        temp = 1000.0
        coolingRate = 1

        random.shuffle(self.cameraManager.cameras)
        currentSolutionCameras = self.newGeneration(self.cameraManager.cameras[0:self.cameraManager.numberOfCameras])
        currentSolution = CameraManager(cameras=currentSolutionCameras, count=self.cameraManager.numberOfCameras)

        bestSolution = CameraManager(cameras=currentSolutionCameras, count=self.cameraManager.numberOfCameras)

        while (temp > 1):

            random.shuffle(self.cameraManager.cameras)
            newSolutionCameras = self.newGeneration(self.cameraManager.cameras[0:self.cameraManager.numberOfCameras])
            newSolution = CameraManager(cameras=newSolutionCameras, count=self.cameraManager.numberOfCameras)

            first_camera_index = randint(0, self.cameraManager.numberOfCameras - 1)
            second_camera_index = randint(0, self.cameraManager.numberOfCameras - 1)

            first_camera_swap = newSolution.cameras[first_camera_index]
            second_camera_swap = newSolution.cameras[first_camera_index]

            newSolution.setCamera(first_camera_swap, second_camera_index)
            newSolution.setCamera(second_camera_swap, first_camera_index)

            currentEnergy = currentSolution.getArea()
            neighborEnergy = newSolution.getArea()

            if self.acceptanceProbability(currentEnergy, neighborEnergy, temp) > float(temp/1000):
                currentSolution = copy.deepcopy(newSolution)

            if currentSolution.getArea() < bestSolution.getArea():
                bestSolution = currentSolution

            temp *= 1 - coolingRate
            print(temp)

        return bestSolution.cameras
