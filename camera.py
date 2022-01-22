import cv2
import threading
import time
# from second import findEncodings
# from second import markAttendance
import second
import face_recognition
import logging
# from numpy import np

logger = logging.getLogger(__name__)

thread = None
# encodeListKnown = findEncodings()
images = []
classNames = []

class Camera:
	def __init__(self,fps=20,video_source=0):
		logger.info(f"Initializing camera class with {fps} fps and video_source={video_source}")
		self.fps = fps
		self.video_source = video_source
		self.camera = cv2.VideoCapture(self.video_source)
		# We want a max of 5s history to be stored, thats 5s*fps
		self.max_frames = 5*self.fps
		self.frames = []
		self.isrunning = False
	def run(self):
		logging.debug("Preparing thread")
		global thread
		if thread is None:
			logging.debug("Creating thread")
			thread = threading.Thread(target=self._capture_loop,daemon=True)
			logger.debug("Starting thread")
			self.isrunning = True
			thread.start()
			logger.info("Thread started")

	def _capture_loop(self):
		dt = 1/self.fps
		logger.debug("Observation started")
		while self.isrunning:
			v,im = self.camera.read()
			if v:
				if len(self.frames)==self.max_frames:
					self.frames = self.frames[1:]
				self.frames.append(im)
			time.sleep(dt)
			return self.frames
		logger.info("Thread stopped successfully")

#Falta agregar analizar las fotos desde el recurso de cámara local:s

	# def stream(classNames, markAttendance, self.frames):
    	
	# 	encodeListKnown = findEncodings(images)
	# 	while True:
	# 	success, img = self.frames.read()
	# 	imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
	# 	imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
	# 	facesCurFrame = face_recognition.face_locations(imgS)
	# 	encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # 		for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
    # 		    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
    # 		    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
    # 		    print(faceDis)
    # 		    matchIndex = np.argmin(faceDis)

    # 	        if matches[matchIndex]:
    # 	            name = classNames[matchIndex].upper()
    # 	            print(name)
    # 	            y1,x2,y2,x1 = faceLoc
    # 	            x1,y1,x2,y2 = x1*4, y1*4, x2*4, y2*4
    # 	            cv2.rectangle(img, (x1,y1), (x2,y2), (0, 255, 0), 2)
    # 	            cv2.rectangle(img, (x1, y2-35), (x2,y2), (0,255,0), cv2.FILLED)
    # 	            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
    # 	            markAttendance(name)

    # 	        if faceDis[matchIndex] < 0.5:
    # 	            name = classNames[matchIndex].upper()
    # 	            markAttendance(name)
    # 	            y1,x2,y2,x1 = faceLoc
    # 	            x1,y1,x2,y2 = x1*4, y1*4, x2*4, y2*4
    # 	            cv2.rectangle(img, (x1,y1), (x2,y2), (0, 255, 0), 2)
    # 	            cv2.rectangle(img, (x1, y2-35), (x2,y2), (0,255,0), cv2.FILLED)
    # 	            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
    # 	        else: 
    # 	            name = 'Unknown'
    # 	            y1,x2,y2,x1 = faceLoc
    # 	            x1,y1,x2,y2 = x1*4, y1*4, x2*4, y2*4
    # 	            cv2.rectangle(img, (x1,y1), (x2,y2), (0, 0, 255), 2)
    # 	            cv2.rectangle(img, (x1, y2-35), (x2,y2), (0,0,255), cv2.FILLED)
    # 	            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
	# 		return (img,name)


	def stop(self):
		logger.debug("Stopping thread")
		self.isrunning = False

	def get_frame(self, _bytes=True):
		if len(self.frames)>0:
			if _bytes:
				img = cv2.imencode('.png',self.frames[-1])[1].tobytes()
			else:
				img = self.frames[-1]
		else:
			with open("initcam/not_found.jpeg","rb") as f:
				img = f.read()
		return img