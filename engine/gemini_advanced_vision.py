"""
Gemini-Style Advanced Vision AI System
Full interactive AI with vision, conversation, and intelligence
"""

import cv2
import numpy as np
import threading
import time
import json
import random
import base64
import subprocess
from datetime import datetime
from collections import deque
import speech_recognition as sr
import pyttsx3

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class GeminiAdvancedVision:
    def __init__(self):
        self.is_active = False
        self.camera = None
        self.conversation_history = deque(maxlen=100)
        self.visual_memory = deque(maxlen=20)
        self.user_profile = {
            'name': 'User',
            'preferences': {},
            'interaction_style': 'friendly',
            'learning_data': {}
        }
        
        # Vision tracking
        self.current_scene = "unknown"
        self.detected_objects = []
        self.face_analysis = {}
        self.gesture_state = None
        self.attention_level = 0
        self.engagement_score = 0
        
        # AI personality
        self.personality = {
            'mode': 'intelligent_assistant',
            'creativity': 0.8,
            'helpfulness': 0.9,
            'curiosity': 0.7,
            'proactiveness': 0.6,
            'empathy': 0.8
        }
        
        # Missing attributes
        self.interaction_quality = 8.5
        self.current_language = 'en-US'
        self.proactive_responses = True
        self.context_awareness = True
        self.long_term_memory = {
            'emotional_baseline': {},
            'interaction_history': []
        }
        
        # Initialize systems
        self._init_vision_system()
        self._init_audio_system()
        self._init_ai_system()
        self._init_yolo_system()
        
        # Phone camera setup
        self.use_phone_camera = False
        self.adb_process = None
    
    def _init_vision_system(self):
        """Initialize advanced vision system"""
        global MEDIAPIPE_AVAILABLE
        if MEDIAPIPE_AVAILABLE:
            try:
                self.mp_face_mesh = mp.solutions.face_mesh
                self.mp_hands = mp.solutions.hands
                self.mp_pose = mp.solutions.pose
                self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
                self.mp_drawing = mp.solutions.drawing_utils
                
                self.face_mesh = self.mp_face_mesh.FaceMesh(
                    max_num_faces=3, refine_landmarks=True,
                    min_detection_confidence=0.5, min_tracking_confidence=0.5
                )
                
                self.hands = self.mp_hands.Hands(
                    static_image_mode=False, max_num_hands=4,
                    min_detection_confidence=0.7, min_tracking_confidence=0.5
                )
                
                self.pose = self.mp_pose.Pose(
                    static_image_mode=False,
                    min_detection_confidence=0.5, min_tracking_confidence=0.5
                )
                
                self.segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
                
                print("🧠 Advanced MediaPipe Vision System Initialized")
            except Exception as e:
                print(f"MediaPipe error: {e}")
                MEDIAPIPE_AVAILABLE = False
        
    def _init_yolo_system(self):
        """Initialize YOLO object detection"""
        global YOLO_AVAILABLE
        if YOLO_AVAILABLE:
            try:
                self.yolo_model = YOLO('yolov8n.pt')
                self.coco_classes = [
                    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
                    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
                    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
                    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
                    'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
                    'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
                    'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
                ]
                
                # Enhanced object mapping for better detection
                self.object_mappings = {
                    'remote': 'remote_control',
                    'mouse': 'computer_mouse', 
                    'toothbrush': 'charger',  # Often misclassified as charger
                    'hair drier': 'charger',  # Often misclassified as charger
                    'scissors': 'tool',
                    'teddy bear': 'toy',
                    'sports ball': 'ball',
                    'wine glass': 'glass',
                    'dining table': 'table',
                    'potted plant': 'plant',
                    'cell phone': 'phone'
                }
                
                # Detection confidence thresholds for different object types
                self.confidence_thresholds = {
                    'person': 0.5,
                    'laptop': 0.4,
                    'cell phone': 0.3,
                    'book': 0.3,
                    'cup': 0.3,
                    'bottle': 0.3,
                    'chair': 0.4,
                    'mouse': 0.25,
                    'keyboard': 0.3,
                    'remote': 0.25,
                    'clock': 0.3,
                    'scissors': 0.2,
                    'toothbrush': 0.2,  # Low threshold for potential chargers
                    'hair drier': 0.2   # Low threshold for potential chargers
                }
                
                print("🎯 YOLOv8 Enhanced Object Detection Initialized")
            except Exception as e:
                print(f"YOLO error: {e}")
                YOLO_AVAILABLE = False
        else:
            print("⚠️ YOLOv8 not available - install ultralytics")
    
    def _init_phone_camera(self):
        """Initialize phone camera - check all available cameras"""
        try:
            print("📱 Scanning for all available cameras...")
            
            best_camera = None
            best_resolution = 0
            
            # Check all possible camera indices
            for cam_id in range(10):  # Check more camera indices
                try:
                    test_camera = cv2.VideoCapture(cam_id)
                    if test_camera.isOpened():
                        ret, frame = test_camera.read()
                        if ret and frame is not None:
                            h, w = frame.shape[:2]
                            resolution = w * h
                            
                            print(f"✅ Camera {cam_id}: {w}x{h} pixels")
                            
                            # Prefer higher resolution cameras (likely phone cameras)
                            if resolution > best_resolution:
                                if best_camera:
                                    best_camera.release()
                                best_camera = test_camera
                                best_resolution = resolution
                                best_cam_id = cam_id
                            else:
                                test_camera.release()
                        else:
                            test_camera.release()
                    else:
                        print(f"❌ Camera {cam_id}: Not available")
                except Exception as e:
                    continue
            
            # Use the best camera found
            if best_camera and best_resolution > 640*480:  # Better than basic webcam
                print(f"📱 Using high-resolution camera {best_cam_id}: {best_resolution} pixels")
                self.camera = best_camera
                return True
            elif best_camera:
                print(f"💻 Using standard camera {best_cam_id}")
                self.camera = best_camera
                return True
            
            print("⚠️ No cameras detected")
            return False
                    
        except Exception as e:
            print(f"⚠️ Camera detection failed: {e}")
            return False
    
    def _init_audio_system(self):
        """Initialize advanced audio system"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS for natural speech
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice for friendlier interaction
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            self.tts_engine.setProperty('rate', 165)
            self.tts_engine.setProperty('volume', 0.9)
            
            print("🎤 Advanced Audio System Initialized")
        except Exception as e:
            print(f"Audio error: {e}")
    
    def _init_ai_system(self):
        """Initialize AI conversation system"""
        if GEMINI_AVAILABLE:
            try:
                # Configure Gemini (you'll need to add your API key)
                # genai.configure(api_key="YOUR_API_KEY")
                # self.gemini_model = genai.GenerativeModel('gemini-pro-vision')
                print("🤖 Gemini AI System Ready (API key needed)")
            except Exception as e:
                print(f"Gemini error: {e}")
        
        # Fallback conversation system
        self.conversation_patterns = {
            'greetings': [
                "Hello! I can see you clearly. How are you today?",
                "Hi there! I'm analyzing what I see. What would you like to know?",
                "Good to see you! I'm processing your visual context. How can I help?"
            ],
            'vision_questions': [
                "I can see {objects} in your environment. What would you like to know about them?",
                "I notice {scene_description}. Is there something specific you'd like me to analyze?",
                "From what I can see, {observation}. How can I assist you with this?"
            ],
            'emotional_responses': [
                "I can see you're {emotion}. {contextual_response}",
                "Your expression suggests you're {emotion}. {supportive_response}",
                "I notice you seem {emotion}. {helpful_response}"
            ]
        }
    
    def start_gemini_vision(self):
        """Start the advanced Gemini-style vision system"""
        if self.is_active:
            return "🤖 Advanced Vision AI already active"
        
        try:
            # Try phone camera via ADB first, then fallback to PC camera
            self.use_phone_camera = self._init_phone_camera()
            
            if not self.use_phone_camera:
                # Fallback to PC camera
                for cam_id in [0, 1, 2]:
                    self.camera = cv2.VideoCapture(cam_id)
                    if self.camera.isOpened():
                        break
                    self.camera.release()
                
                if not self.camera.isOpened():
                    return "❌ Cannot access any camera"
                
                # Set high-quality capture
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_active = True
            
            # Start enhanced processing threads for Gemini Live
            threading.Thread(target=self._vision_processing_loop, daemon=True).start()
            threading.Thread(target=self._audio_processing_loop, daemon=True).start()
            threading.Thread(target=self._ai_analysis_loop, daemon=True).start()
            threading.Thread(target=self._proactive_ai_loop, daemon=True).start()
            threading.Thread(target=self._continuous_engagement_monitor, daemon=True).start()
            threading.Thread(target=self._context_awareness_loop, daemon=True).start()
            threading.Thread(target=self._memory_consolidation_loop, daemon=True).start()
            threading.Thread(target=self._real_time_adaptation_loop, daemon=True).start()
            
            greeting = self._generate_startup_greeting()
            self._speak(greeting)
            
            return f"🚀 {greeting}"
            
        except Exception as e:
            self.is_active = False
            return f"❌ Error: {str(e)}"
    
    def _generate_startup_greeting(self):
        """Generate intelligent startup greeting"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 21:
            time_greeting = "Good evening"
        else:
            time_greeting = "Hello"
        
        capabilities = []
        if MEDIAPIPE_AVAILABLE:
            capabilities.append("advanced computer vision")
        if GEMINI_AVAILABLE:
            capabilities.append("Gemini AI intelligence")
        capabilities.append("natural conversation")
        
        return f"{time_greeting}! I'm your advanced AI assistant with {', '.join(capabilities)}. I can see, understand, and have intelligent conversations about anything you show me!"
    
    def _vision_processing_loop(self):
        """Advanced vision processing with AI analysis"""
        frame_count = 0
        
        while self.is_active:
            try:
                if self.use_phone_camera:
                    ret, frame = self._get_phone_frame()
                else:
                    ret, frame = self.camera.read()
                    
                if not ret:
                    continue
                
                frame = cv2.flip(frame, 1)
                frame_count += 1
                
                # Process every frame for real-time, analyze deeply every 10th frame
                processed_frame = self._process_frame_advanced(frame, deep_analysis=(frame_count % 10 == 0))
                
                cv2.imshow('Gemini Advanced Vision AI', processed_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('c'):  # Capture and analyze
                    self._capture_and_analyze(frame)
                elif key == ord('m'):  # Change AI mode
                    self._cycle_ai_mode()
                elif key == ord('p'):  # Toggle proactive mode
                    self.personality['proactiveness'] = 1.0 - self.personality['proactiveness']
                    self._speak(f"Proactive mode {'enabled' if self.personality['proactiveness'] > 0.5 else 'disabled'}")
                
            except Exception as e:
                print(f"Vision error: {e}")
                time.sleep(0.1)
        
        self.stop_gemini_vision()
    
    def _process_frame_advanced(self, frame, deep_analysis=False):
        """Advanced frame processing with AI insights"""
        h, w, _ = frame.shape
        
        global MEDIAPIPE_AVAILABLE
        if MEDIAPIPE_AVAILABLE:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Multi-person face analysis
            face_results = self.face_mesh.process(rgb_frame)
            if face_results.multi_face_landmarks:
                for i, face_landmarks in enumerate(face_results.multi_face_landmarks):
                    # Draw enhanced face mesh
                    self.mp_drawing.draw_landmarks(
                        frame, face_landmarks, self.mp_face_mesh.FACEMESH_CONTOURS,
                        None, self.mp_drawing.DrawingSpec(color=(0, 255, 100), thickness=1, circle_radius=1)
                    )
                    
                    if deep_analysis:
                        self.face_analysis[f'person_{i}'] = self._analyze_face_advanced(face_landmarks, w, h)
            
            # Advanced hand tracking
            hand_results = self.hands.process(rgb_frame)
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(255, 100, 0), thickness=2, circle_radius=2)
                    )
                    
                    if deep_analysis:
                        self.gesture_state = self._analyze_gesture_advanced(hand_landmarks, w, h)
            
            # Pose analysis
            pose_results = self.pose.process(rgb_frame)
            if pose_results.pose_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, pose_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(100, 255, 255), thickness=2, circle_radius=2)
                )
            
            # Scene segmentation for context
            if deep_analysis:
                segmentation_results = self.segmentation.process(rgb_frame)
                self._analyze_scene_context(frame, segmentation_results)
        
        return self._add_ai_overlay(frame)
    
    def _analyze_face_advanced(self, face_landmarks, w, h):
        """Advanced facial analysis with AI insights"""
        try:
            landmarks = np.array([(lm.x * w, lm.y * h) for lm in face_landmarks.landmark])
            
            # Advanced emotion analysis
            emotion_data = self._calculate_emotion_advanced(landmarks)
            
            # Attention and engagement
            attention = self._calculate_attention_level(landmarks, w, h)
            
            # Age and demographic estimation (simplified)
            demographic = self._estimate_demographics(landmarks)
            
            return {
                'emotion': emotion_data,
                'attention': attention,
                'demographic': demographic,
                'engagement': self._calculate_engagement(emotion_data, attention)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_emotion_advanced(self, landmarks):
        """Advanced emotion calculation with multiple features"""
        try:
            # Mouth analysis
            mouth_points = [61, 291, 13, 14, 17, 18, 267, 269, 270, 271, 272]
            mouth_landmarks = landmarks[mouth_points]
            mouth_curve = self._calculate_mouth_curvature(mouth_landmarks)
            
            # Eye analysis
            left_eye_points = [33, 7, 163, 144, 145, 153, 154, 155, 133]
            right_eye_points = [362, 382, 381, 380, 374, 373, 390, 249, 263]
            
            left_eye = landmarks[left_eye_points]
            right_eye = landmarks[right_eye_points]
            eye_openness = self._calculate_eye_openness_advanced(left_eye, right_eye)
            
            # Eyebrow analysis
            left_brow = landmarks[[70, 63, 105, 66, 107]]
            right_brow = landmarks[[296, 334, 293, 300, 276]]
            brow_position = self._calculate_brow_position(left_brow, right_brow, left_eye, right_eye)
            
            # Combine features for emotion classification
            emotions = {
                'happy': max(0, mouth_curve * 2 + eye_openness * 0.5),
                'sad': max(0, -mouth_curve * 1.5 + (1 - eye_openness) * 0.3),
                'surprised': max(0, eye_openness * 1.5 + brow_position * 1.2),
                'angry': max(0, -brow_position * 1.5 + (1 - eye_openness) * 0.5),
                'neutral': 1 - max(abs(mouth_curve), abs(brow_position), abs(eye_openness - 0.5))
            }
            
            # Normalize emotions
            total = sum(emotions.values())
            if total > 0:
                emotions = {k: v/total for k, v in emotions.items()}
            
            primary_emotion = max(emotions, key=emotions.get)
            confidence = emotions[primary_emotion]
            
            return {
                'primary': primary_emotion,
                'confidence': confidence,
                'all_emotions': emotions,
                'features': {
                    'mouth_curve': mouth_curve,
                    'eye_openness': eye_openness,
                    'brow_position': brow_position
                }
            }
        except Exception as e:
            return {'primary': 'neutral', 'confidence': 0.5, 'error': str(e)}
    
    def _calculate_mouth_curvature(self, mouth_landmarks):
        """Calculate mouth curvature for smile detection"""
        try:
            left_corner = mouth_landmarks[0]
            right_corner = mouth_landmarks[1]
            center_points = mouth_landmarks[2:5]
            
            corner_avg_y = (left_corner[1] + right_corner[1]) / 2
            center_avg_y = np.mean([p[1] for p in center_points])
            
            width = abs(left_corner[0] - right_corner[0])
            if width > 0:
                curvature = (corner_avg_y - center_avg_y) / width
                return np.clip(curvature, -0.1, 0.1) * 10  # Normalize to -1 to 1
            return 0
        except:
            return 0
    
    def _calculate_eye_openness_advanced(self, left_eye, right_eye):
        """Advanced eye openness calculation"""
        try:
            def eye_aspect_ratio(eye_points):
                # Vertical distances
                v1 = np.linalg.norm(eye_points[1] - eye_points[5])
                v2 = np.linalg.norm(eye_points[2] - eye_points[4])
                # Horizontal distance
                h = np.linalg.norm(eye_points[0] - eye_points[3])
                return (v1 + v2) / (2.0 * h) if h > 0 else 0
            
            left_ear = eye_aspect_ratio(left_eye[:6])
            right_ear = eye_aspect_ratio(right_eye[:6])
            
            avg_ear = (left_ear + right_ear) / 2
            return np.clip(avg_ear * 5, 0, 1)  # Normalize to 0-1
        except:
            return 0.5
    
    def _calculate_brow_position(self, left_brow, right_brow, left_eye, right_eye):
        """Calculate eyebrow position relative to eyes"""
        try:
            left_brow_y = np.mean(left_brow[:, 1])
            right_brow_y = np.mean(right_brow[:, 1])
            left_eye_y = np.mean(left_eye[:, 1])
            right_eye_y = np.mean(right_eye[:, 1])
            
            left_distance = (left_eye_y - left_brow_y) / 50  # Normalize
            right_distance = (right_eye_y - right_brow_y) / 50
            
            return (left_distance + right_distance) / 2
        except:
            return 0
    
    def _calculate_attention_level(self, landmarks, w, h):
        """Calculate attention level based on gaze and pose"""
        try:
            # Eye center calculation
            left_eye_center = np.mean(landmarks[[33, 133]], axis=0)
            right_eye_center = np.mean(landmarks[[362, 263]], axis=0)
            eye_center = (left_eye_center + right_eye_center) / 2
            
            # Distance from frame center
            frame_center = np.array([w/2, h/2])
            distance = np.linalg.norm(eye_center - frame_center)
            max_distance = min(w, h) * 0.3
            
            attention = max(0, 1 - (distance / max_distance))
            return attention
        except:
            return 0.5
    
    def _calculate_engagement(self, emotion_data, attention):
        """Calculate overall engagement score"""
        try:
            emotion_score = emotion_data.get('confidence', 0.5)
            if emotion_data.get('primary') in ['happy', 'surprised']:
                emotion_score *= 1.2
            elif emotion_data.get('primary') in ['sad', 'angry']:
                emotion_score *= 0.8
            
            engagement = (attention * 0.6 + emotion_score * 0.4)
            return np.clip(engagement, 0, 1)
        except:
            return 0.5
    
    def _analyze_gesture_advanced(self, hand_landmarks, w, h):
        """Advanced gesture recognition with context"""
        try:
            landmarks = np.array([(lm.x * w, lm.y * h) for lm in hand_landmarks.landmark])
            
            # Finger positions
            finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
            finger_joints = [3, 6, 10, 14, 18]
            
            fingers_up = []
            
            # Thumb (different logic due to orientation)
            if landmarks[4][0] > landmarks[3][0]:  # Right hand
                fingers_up.append(landmarks[4][0] > landmarks[3][0])
            else:  # Left hand
                fingers_up.append(landmarks[4][0] < landmarks[3][0])
            
            # Other fingers
            for i in range(1, 5):
                fingers_up.append(landmarks[finger_tips[i]][1] < landmarks[finger_joints[i]][1])
            
            # Advanced gesture recognition
            gesture_patterns = {
                'thumbs_up': [True, False, False, False, False],
                'peace_sign': [False, True, True, False, False],
                'pointing': [False, True, False, False, False],
                'ok_sign': [True, False, False, False, False],  # Simplified
                'rock_on': [False, True, False, False, True],
                'stop_hand': [True, True, True, True, True],
                'fist': [False, False, False, False, False],
                'three_fingers': [False, True, True, True, False],
                'four_fingers': [False, True, True, True, True]
            }
            
            # Find best matching gesture
            best_match = None
            best_score = 0
            
            for gesture, pattern in gesture_patterns.items():
                score = sum(1 for i, expected in enumerate(pattern) if fingers_up[i] == expected)
                if score > best_score and score >= 4:  # At least 4/5 fingers match
                    best_match = gesture
                    best_score = score
            
            return {
                'gesture': best_match,
                'confidence': best_score / 5 if best_match else 0,
                'fingers_up': fingers_up,
                'hand_position': self._get_hand_position(landmarks, w, h)
            }
        except Exception as e:
            return {'gesture': None, 'error': str(e)}
    
    def _get_hand_position(self, landmarks, w, h):
        """Get hand position in frame"""
        try:
            center = np.mean(landmarks, axis=0)
            x_pos = "left" if center[0] < w/3 else "right" if center[0] > 2*w/3 else "center"
            y_pos = "top" if center[1] < h/3 else "bottom" if center[1] > 2*h/3 else "middle"
            return f"{y_pos}_{x_pos}"
        except:
            return "unknown"
    
    def _analyze_scene_context(self, frame, segmentation_results):
        """Analyze scene context with YOLO object detection"""
        try:
            global YOLO_AVAILABLE
            if YOLO_AVAILABLE and hasattr(self, 'yolo_model'):
                # YOLO detection with adaptive thresholds
                results = self.yolo_model(frame, conf=0.2, iou=0.4, verbose=False, max_det=25)
                objects_detected = []
                
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            confidence = float(box.conf[0])
                            class_id = int(box.cls[0])
                            if class_id < len(self.coco_classes):
                                obj_name = self.coco_classes[class_id]
                                
                                # Use adaptive confidence threshold
                                min_confidence = self.confidence_thresholds.get(obj_name, 0.3)
                                
                                if confidence >= min_confidence:
                                    # Apply object mapping
                                    if obj_name in self.object_mappings:
                                        mapped_name = self.object_mappings[obj_name]
                                        if mapped_name == 'charger' and confidence > 0.2:
                                            obj_name = 'charger'
                                        else:
                                            obj_name = mapped_name
                                    
                                    objects_detected.append(obj_name)
                                    
                                    # Draw bounding box with adaptive colors
                                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                                    if confidence > 0.7:
                                        color = (0, 255, 0)  # Green for high confidence
                                    elif confidence > 0.5:
                                        color = (0, 200, 255)  # Yellow for medium confidence
                                    elif confidence > 0.3:
                                        color = (255, 150, 0)  # Orange for low-medium confidence
                                    else:
                                        color = (255, 100, 100)  # Light red for low confidence
                                    
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                                    cv2.putText(frame, f"{obj_name} {confidence:.0%}", 
                                              (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                
                # Update detected objects with counts and filtering
                object_counts = {}
                for obj in objects_detected:
                    # Clean object names
                    clean_obj = obj.replace('_', ' ')
                    object_counts[clean_obj] = object_counts.get(clean_obj, 0) + 1
                
                # Create final object list with counts
                final_objects = []
                for obj, count in object_counts.items():
                    if count > 1:
                        final_objects.append(f"{obj}({count})")
                    else:
                        final_objects.append(obj)
                
                self.detected_objects = final_objects[:12]  # Show more objects
                
                # Reduce detection noise - only print significant changes
                current_unique = set([obj.split('(')[0] for obj in objects_detected])
                last_unique = set(getattr(self, '_last_unique_objects', []))
                
                if len(current_unique - last_unique) > 0 or len(last_unique - current_unique) > 0:
                    if len(current_unique) > 0:
                        print(f"🎯 Objects detected: {', '.join(list(current_unique)[:6])}")
                    self._last_unique_objects = list(current_unique)
            else:
                # Enhanced fallback detection
                self._enhanced_basic_detection(frame)
            
            # Scene classification
            self._classify_scene()
                
        except Exception as e:
            print(f"Detection error: {e}")
            self.detected_objects = []
            self.current_scene = "general_room"
    
    def _enhanced_basic_detection(self, frame):
        """Enhanced basic object detection fallback with charger detection"""
        h, w, _ = frame.shape
        objects_detected = []
        
        # Multi-method detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Edge detection for rectangular objects
        edges = cv2.Canny(gray, 20, 80)  # Lower thresholds for better small object detection
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 800:  # Lower area threshold
                x, y, rect_w, rect_h = cv2.boundingRect(contour)
                aspect_ratio = rect_w / rect_h
                
                # Draw detection boxes
                cv2.rectangle(frame, (x, y), (x+rect_w, y+rect_h), (255, 0, 0), 1)
                
                # Classify by size and aspect ratio - including small objects
                if 1.3 < aspect_ratio < 2.2 and area > 8000:
                    objects_detected.append('laptop')
                    cv2.putText(frame, 'laptop', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
                elif 0.7 < aspect_ratio < 1.3 and 3000 < area < 15000:
                    objects_detected.append('book')
                    cv2.putText(frame, 'book', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
                elif aspect_ratio > 2.5 and y > h * 0.6:
                    objects_detected.append('keyboard')
                    cv2.putText(frame, 'keyboard', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
                elif 0.4 < aspect_ratio < 0.9 and 1000 < area < 6000:
                    objects_detected.append('phone')
                    cv2.putText(frame, 'phone', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
                # NEW: Small rectangular objects (chargers, cables)
                elif 0.3 < aspect_ratio < 4.0 and 800 < area < 3000:
                    objects_detected.append('charger')
                    cv2.putText(frame, 'charger', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                # Long thin objects (cables)
                elif aspect_ratio > 4.0 and 500 < area < 2000:
                    objects_detected.append('cable')
                    cv2.putText(frame, 'cable', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
        
        # Color-based detection for common objects
        # White/light objects (chargers often white)
        white_mask = cv2.inRange(hsv, (0, 0, 200), (180, 30, 255))
        white_contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in white_contours:
            area = cv2.contourArea(contour)
            if 500 < area < 3000:
                x, y, w_rect, h_rect = cv2.boundingRect(contour)
                aspect_ratio = w_rect / h_rect
                if 0.5 < aspect_ratio < 2.0:
                    objects_detected.append('white_charger')
                    cv2.rectangle(frame, (x, y), (x+w_rect, y+h_rect), (255, 255, 255), 1)
                    cv2.putText(frame, 'charger', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Black objects (many chargers are black)
        black_mask = cv2.inRange(hsv, (0, 0, 0), (180, 255, 50))
        black_contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in black_contours:
            area = cv2.contourArea(contour)
            if 400 < area < 2500:
                x, y, w_rect, h_rect = cv2.boundingRect(contour)
                aspect_ratio = w_rect / h_rect
                if 0.4 < aspect_ratio < 2.5:
                    objects_detected.append('black_charger')
                    cv2.rectangle(frame, (x, y), (x+w_rect, y+h_rect), (0, 0, 0), 1)
                    cv2.putText(frame, 'charger', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (128, 128, 128), 1)
        
        # Green objects (plants)
        green_mask = cv2.inRange(hsv, (35, 50, 50), (85, 255, 255))
        green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in green_contours:
            if cv2.contourArea(contour) > 2000:
                objects_detected.append('plant')
        
        # Circular objects (cups, bottles)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 30, param1=40, param2=25, minRadius=10, maxRadius=100)
        if circles is not None:
            for circle in circles[0, :]:
                objects_detected.append('cup')
        
        # Clean up and organize detected objects
        cleaned_objects = []
        charger_found = False
        
        for obj in objects_detected:
            if 'charger' in obj.lower():
                if not charger_found:
                    cleaned_objects.append('charger')
                    charger_found = True
            else:
                cleaned_objects.append(obj)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_objects = []
        for obj in cleaned_objects:
            if obj not in seen:
                seen.add(obj)
                unique_objects.append(obj)
        
        self.detected_objects = unique_objects[:12]  # Show more objects
    
    def _classify_scene(self):
        """Classify scene based on detected objects"""
        obj_str = ' '.join(self.detected_objects).lower()
        
        if any(word in obj_str for word in ['laptop', 'keyboard', 'mouse', 'computer']):
            self.current_scene = "computer_workspace"
        elif any(word in obj_str for word in ['book', 'paper']):
            self.current_scene = "study_area"
        elif any(word in obj_str for word in ['cup', 'bottle', 'plant']):
            self.current_scene = "living_space"
        elif any(word in obj_str for word in ['chair', 'table', 'couch']):
            self.current_scene = "furniture_area"
        elif len(self.detected_objects) >= 3:
            self.current_scene = "busy_workspace"
        else:
            self.current_scene = "general_room"
    
    def _add_ai_overlay(self, frame):
        """Add advanced AI overlay with insights"""
        h, w, _ = frame.shape
        
        # Main AI panel
        panel_height = 200
        cv2.rectangle(frame, (10, 10), (450, panel_height), (20, 20, 20), -1)
        cv2.rectangle(frame, (10, 10), (450, panel_height), (0, 255, 150), 2)
        
        # Title with AI indicator
        cv2.putText(frame, "GEMINI ADVANCED VISION AI", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # AI Status
        ai_status = "🧠 ANALYZING" if len(self.face_analysis) > 0 else "👁️ OBSERVING"
        cv2.putText(frame, ai_status, (20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 1)
        
        # Scene analysis
        cv2.putText(frame, f"Scene: {self.current_scene.replace('_', ' ').title()}", (20, 85), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 200, 0), 1)
        
        # Objects detected
        if self.detected_objects:
            objects_text = f"Objects: {', '.join(self.detected_objects[:3])}"
            cv2.putText(frame, objects_text, (20, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 150, 0), 1)
        
        # Face analysis results
        if self.face_analysis:
            person_data = list(self.face_analysis.values())[0]
            if 'emotion' in person_data:
                emotion_info = person_data['emotion']
                emotion_text = f"Emotion: {emotion_info['primary'].title()} ({emotion_info['confidence']:.1%})"
                cv2.putText(frame, emotion_text, (20, 135), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 255), 1)
                
                attention_text = f"Attention: {person_data.get('attention', 0):.1%}"
                cv2.putText(frame, attention_text, (20, 160), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 255), 1)
        
        # Gesture info
        if self.gesture_state and self.gesture_state.get('gesture'):
            gesture_text = f"Gesture: {self.gesture_state['gesture'].replace('_', ' ').title()}"
            cv2.putText(frame, gesture_text, (20, 185), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 150), 1)
        
        # AI Controls panel
        controls_y = h - 100
        cv2.rectangle(frame, (10, controls_y), (400, h-10), (30, 30, 30), -1)
        cv2.rectangle(frame, (10, controls_y), (400, h-10), (100, 100, 100), 1)
        
        cv2.putText(frame, "AI Controls: Q=Quit | C=Capture&Analyze | M=AI Mode | P=Proactive", 
                   (15, controls_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        mode_text = f"Mode: {self.personality['mode'].replace('_', ' ').title()}"
        cv2.putText(frame, mode_text, (15, controls_y + 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        proactive_status = "ON" if self.personality['proactiveness'] > 0.5 else "OFF"
        cv2.putText(frame, f"Proactive: {proactive_status} | Creativity: {self.personality['creativity']:.1f}", 
                   (15, controls_y + 75), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 200, 255), 1)
        
        # Time and status
        current_time = datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, current_time, (w-120, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def _audio_processing_loop(self):
        """Advanced audio processing with AI conversation"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("🎤 Listening for voice commands...")
        except Exception as e:
            print(f"Audio setup error: {e}")
            return
        
        while self.is_active:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=8)
                
                try:
                    text = self.recognizer.recognize_google(audio, language='en-US')
                    if text and len(text.strip()) > 1:
                        print(f"🎤 Heard: {text}")
                        self._process_ai_conversation(text)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"Speech recognition error: {e}")
                    
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                time.sleep(1)
    
    def _process_ai_conversation(self, user_input):
        """Process conversation with advanced AI responses"""
        timestamp = datetime.now()
        
        # Add to conversation history
        conversation_entry = {
            'timestamp': timestamp.isoformat(),
            'user_input': user_input,
            'visual_context': {
                'scene': self.current_scene,
                'objects': self.detected_objects.copy(),
                'face_analysis': self.face_analysis.copy(),
                'gesture': self.gesture_state
            }
        }
        
        # Generate AI response
        ai_response = self._generate_ai_response(user_input, conversation_entry['visual_context'])
        
        conversation_entry['ai_response'] = ai_response
        self.conversation_history.append(conversation_entry)
        
        # Speak response
        self._speak(ai_response)
        
        # Log conversation
        print(f"\n[{timestamp.strftime('%H:%M:%S')}] User: {user_input}")
        print(f"[{timestamp.strftime('%H:%M:%S')}] AI: {ai_response}")
    
    def _generate_ai_response(self, user_input, visual_context):
        """Generate comprehensive AI responses using video and audio"""
        user_lower = user_input.lower()
        objects = visual_context.get('objects', [])
        scene = visual_context.get('scene', 'general_room')
        face_data = visual_context.get('face_analysis', {})
        gesture_data = visual_context.get('gesture')
        
        # Get emotion and attention for context
        emotion = 'neutral'
        attention = 0.5
        if face_data:
            person_data = list(face_data.values())[0]
            emotion = person_data.get('emotion', {}).get('primary', 'neutral')
            attention = person_data.get('attention', 0.5)
        
        # VISUAL ANALYSIS QUESTIONS
        if any(phrase in user_lower for phrase in ['what do you see', 'what is this', 'identify', 'what objects', 'describe', 'analyze']):
            response = self._generate_detailed_visual_response(objects, scene, emotion, attention, gesture_data)
            return response
        
        # SPECIFIC OBJECT QUESTIONS - Enhanced for ALL objects
        elif self._contains_object_query(user_lower):
            return self._handle_specific_object_query(user_input, objects, scene)
        
        # MATH & CALCULATIONS with visual context
        elif any(word in user_lower for word in ['calculate', 'math', 'plus', 'minus', 'multiply', 'divide', 'solve', 'count']):
            return self._handle_math_with_vision(user_input, objects, visual_context)
        
        # KNOWLEDGE QUESTIONS with visual enhancement
        elif any(phrase in user_lower for phrase in ['what is', 'who is', 'tell me about', 'explain', 'how does', 'why']):
            return self._handle_knowledge_with_vision(user_input, objects, visual_context)
        
        # PROBLEM SOLVING with visual context
        elif any(word in user_lower for word in ['problem', 'issue', 'broken', 'not working', 'fix', 'help', 'trouble']):
            return self._handle_problem_solving_with_vision(user_input, objects, scene, emotion)
        
        # CREATIVE TASKS with visual inspiration
        elif any(word in user_lower for word in ['story', 'poem', 'creative', 'imagine', 'write']):
            return self._handle_creative_with_vision(user_input, objects, scene, emotion)
        
        # EMOTIONAL SUPPORT based on visual cues
        elif emotion in ['sad', 'angry', 'frustrated'] or any(word in user_lower for word in ['sad', 'upset', 'angry', 'frustrated']):
            return self._handle_emotional_support(emotion, attention, objects)
        
        # GENERAL CONVERSATION with full context
        else:
            return self._handle_general_conversation(user_input, objects, scene, emotion, attention, gesture_data)
    
    def _generate_detailed_visual_response(self, objects, scene, emotion, attention, gesture_data):
        """Generate detailed visual analysis response"""
        response_parts = []
        
        # Scene description
        response_parts.append(f"I can see you're in a {scene.replace('_', ' ')}")
        
        # Object analysis
        if objects:
            if len(objects) == 1:
                response_parts.append(f"I detect a {objects[0]}")
            elif len(objects) <= 3:
                response_parts.append(f"I can identify {', '.join(objects[:-1])} and a {objects[-1]}")
            else:
                response_parts.append(f"I see multiple objects including {', '.join(objects[:3])} and {len(objects)-3} more items")
        else:
            response_parts.append("I'm analyzing the objects in your environment")
        
        # Emotional state
        if emotion != 'neutral':
            response_parts.append(f"You appear {emotion}")
        
        # Attention level
        if attention > 0.8:
            response_parts.append("You seem very focused")
        elif attention < 0.3:
            response_parts.append("You seem a bit distracted")
        
        # Gesture recognition
        if gesture_data and gesture_data.get('gesture'):
            gesture = gesture_data['gesture'].replace('_', ' ')
            response_parts.append(f"I notice you're making a {gesture} gesture")
        
        return ". ".join(response_parts) + ". What would you like to know more about?"
    
    def _contains_object_query(self, user_input):
        """Check if user is asking about specific objects"""
        object_keywords = [
            'laptop', 'computer', 'phone', 'book', 'cup', 'bottle', 'charger', 'cable', 'mouse', 'keyboard',
            'chair', 'table', 'plant', 'clock', 'remote', 'tv', 'screen', 'bag', 'pen', 'paper',
            'glass', 'plate', 'bowl', 'spoon', 'fork', 'knife', 'camera', 'headphones', 'speaker'
        ]
        return any(obj in user_input for obj in object_keywords)
    
    def _handle_specific_object_query(self, user_input, objects, scene):
        """Handle questions about specific objects"""
        user_lower = user_input.lower()
        
        # Find which object they're asking about
        mentioned_objects = []
        for obj in objects:
            obj_clean = obj.split('(')[0].lower()
            if obj_clean in user_lower or any(word in user_lower for word in obj_clean.split('_')):
                mentioned_objects.append(obj_clean)
        
        if mentioned_objects:
            obj = mentioned_objects[0]
            return f"Yes, I can clearly see the {obj} in your {scene.replace('_', ' ')}! It's well-positioned and clearly visible. What would you like to know about it? I can describe its location, suggest uses, or answer any questions about it."
        else:
            # Check what they're asking about
            for word in ['laptop', 'computer', 'phone', 'charger', 'book', 'cup', 'bottle']:
                if word in user_lower:
                    return f"I don't currently see a {word} clearly in the frame. Try positioning it more centrally or with better lighting. I'm continuously scanning and will detect it once it's visible."
            
            return "I'm analyzing all objects in view. Could you point to or move the item you're asking about? This will help me identify it more accurately."
    
    def _handle_math_with_vision(self, query, objects, visual_context):
        """Handle math with enhanced visual context"""
        import re
        numbers = re.findall(r'\d+\.?\d*', query)
        
        # Count objects if requested
        if 'count' in query.lower() or 'how many' in query.lower():
            if objects:
                return f"I can count {len(objects)} distinct objects: {', '.join(objects[:5])}{'...' if len(objects) > 5 else ''}. The total count is {len(objects)} items."
            else:
                return "I don't see any distinct objects to count right now. Try showing me some items clearly."
        
        # Regular math operations
        if 'plus' in query.lower() or 'add' in query.lower():
            if len(numbers) >= 2:
                result = float(numbers[0]) + float(numbers[1])
                context = f" Looking at your {visual_context.get('scene', 'workspace').replace('_', ' ')}, " if visual_context.get('scene') else " "
                return f"The answer is {result}.{context}I calculated {numbers[0]} + {numbers[1]} = {result}!"
        elif 'minus' in query.lower() or 'subtract' in query.lower():
            if len(numbers) >= 2:
                result = float(numbers[0]) - float(numbers[1])
                return f"The answer is {result}. I calculated {numbers[0]} - {numbers[1]} = {result}!"
        elif 'multiply' in query.lower() or 'times' in query.lower():
            if len(numbers) >= 2:
                result = float(numbers[0]) * float(numbers[1])
                return f"The answer is {result}. I calculated {numbers[0]} × {numbers[1]} = {result}!"
        elif 'divide' in query.lower():
            if len(numbers) >= 2 and float(numbers[1]) != 0:
                result = float(numbers[0]) / float(numbers[1])
                return f"The answer is {result}. I calculated {numbers[0]} ÷ {numbers[1]} = {result}!"
        else:
            return "I can solve math problems and count objects! Ask me to add, subtract, multiply, divide numbers, or count items in view."
    
    def _handle_science_with_vision(self, query, visual_desc):
        """Handle science with visual context"""
        context = f"Looking at your environment with {visual_desc}, " if visual_desc else ""
        
        if 'gravity' in query.lower():
            return f"{context}gravity is the force keeping you grounded right now! It attracts all objects with mass. On Earth, it's 9.81 m/s². It's why things fall and planets orbit!"
        elif 'atom' in query.lower():
            return f"{context}everything around you is made of atoms! They have a nucleus with protons and neutrons, surrounded by electrons. Incredibly tiny but make up everything!"
        elif 'light' in query.lower():
            return f"{context}light travels at 299,792,458 m/s - the fastest speed possible! The light illuminating your space is made of photons that behave as waves and particles!"
        else:
            return f"{context}I love science questions! I can explain physics, chemistry, biology, space, and more. What scientific concept interests you?"
    
    def _handle_programming_with_vision(self, query, visual_desc):
        """Handle programming with visual context"""
        context = f"I can see your workspace with {visual_desc} - perfect for coding! " if visual_desc else ""
        
        if 'python' in query.lower():
            return f'{context}Python is amazing! Example: print("Hello!") displays text. It\'s great for beginners with clean syntax. What Python concept interests you?'
        elif 'javascript' in query.lower():
            return f"{context}JavaScript powers the web! Example: console.log('Hello!') prints to console. Essential for interactive websites!"
        elif 'html' in query.lower():
            return f"{context}HTML structures web pages! Example: <h1>Title</h1> creates headings. It's the foundation of all websites!"
        else:
            return f"{context}I can help with programming! Python, JavaScript, HTML, CSS, algorithms - what coding challenge are you working on?"
    
    def _handle_knowledge_with_vision(self, query, objects, visual_context):
        """Handle knowledge questions with visual enhancement"""
        query_lower = query.lower()
        scene_context = f"Looking at your {visual_context.get('scene', 'environment').replace('_', ' ')}, " if visual_context.get('scene') else ""
        
        # Technology questions
        if any(word in query_lower for word in ['laptop', 'computer', 'technology']):
            if 'laptop' in objects or 'computer' in objects:
                return f"{scene_context}I can see your computer setup! Modern laptops use processors, RAM, and storage to run programs. They're incredible machines that can handle everything from simple tasks to complex AI processing like what I'm doing right now!"
            else:
                return "Computers are amazing machines! They use binary code (0s and 1s) to process information incredibly fast. What specific aspect of technology interests you?"
        
        # Science questions
        elif any(word in query_lower for word in ['science', 'physics', 'chemistry', 'biology']):
            return f"{scene_context}science is all around us! From the light illuminating your space to the chemical reactions in batteries powering your devices. What scientific concept would you like me to explain?"
        
        # Geography questions
        elif 'capital' in query_lower:
            if 'france' in query_lower:
                return f"{scene_context}the capital of France is Paris! Famous for the Eiffel Tower, Louvre Museum, and incredible culture. It's a city of art, fashion, and history."
            elif 'japan' in query_lower:
                return f"{scene_context}the capital of Japan is Tokyo! One of the world's largest cities, known for cutting-edge technology and rich cultural traditions."
            else:
                return "I can tell you about capitals of any country! Which country's capital are you curious about?"
        
        # History questions
        elif any(word in query_lower for word in ['history', 'historical', 'ancient']):
            return f"{scene_context}history is fascinating! From ancient civilizations to modern innovations. What historical period or event interests you?"
        
        # Movies/Entertainment
        elif 'bahubali' in query_lower:
            return f"{scene_context}Bahubali is an epic Indian film series by S.S. Rajamouli! It's about a warrior prince with incredible action sequences and groundbreaking visual effects. The films were massive blockbusters!"
        
        # General knowledge
        else:
            return f"{scene_context}I can answer questions about science, technology, history, geography, culture, and much more! What topic interests you most?"
    
    def _handle_creative_with_vision(self, query, objects, scene, emotion):
        """Handle creative tasks with visual inspiration"""
        visual_elements = []
        if objects:
            visual_elements.extend(objects[:3])
        if scene != 'general_room':
            visual_elements.append(scene.replace('_', ' '))
        
        inspiration = f"Drawing inspiration from {', '.join(visual_elements)}, " if visual_elements else ""
        
        if 'story' in query.lower():
            if 'laptop' in objects:
                return f"{inspiration}here's a story: Sarah sat at her laptop, the screen glowing softly in the quiet room. As she typed, an AI companion watched through the camera, ready to help with any challenge that arose. Together, they solved problems that seemed impossible just moments before."
            else:
                return f"{inspiration}here's a story: In a world where technology could truly see and understand, every conversation became an adventure of discovery and learning."
        
        elif 'poem' in query.lower():
            if emotion == 'happy':
                return f"{inspiration}a joyful poem:\nIn this moment, bright and clear,\nWith {', '.join(objects[:2]) if objects else 'wonder'} drawing near,\nHappiness fills every space,\nAs we share this time and place."
            else:
                return f"{inspiration}a thoughtful poem:\nIn your space where questions grow,\nAI eyes help knowledge flow,\nTogether we explore and find,\nThe wonders of the curious mind."
        
        elif 'imagine' in query.lower():
            return f"{inspiration}let's imagine together! What if your {objects[0] if objects else 'environment'} could tell stories of all the moments it has witnessed? What creative scenario would you like to explore?"
        
        else:
            return f"{inspiration}I love creative challenges! I can write stories, poems, help brainstorm ideas, or create imaginative scenarios. What creative project sparks your interest?"
    
    def _handle_problem_solving_with_vision(self, query, objects, scene, emotion):
        """Handle problem solving with visual context"""
        query_lower = query.lower()
        context = f"I can see your {scene.replace('_', ' ')} with {', '.join(objects[:2]) if objects else 'your setup'}. "
        
        # Device-specific problems based on what's visible
        if 'phone' in query_lower and 'cell phone' in objects:
            return f"{context}I can see your phone! For phone issues: 1) Force restart (hold power 10-15 seconds), 2) Check charging cable/port, 3) Try different charger, 4) Look for physical damage, 5) Boot in safe mode. What exactly is the phone doing?"
        
        elif 'laptop' in query_lower and 'laptop' in objects:
            return f"{context}I can see your laptop! For laptop problems: 1) Check power adapter connection, 2) Try hard reset (hold power 30 seconds), 3) Remove battery if possible, 4) Check for overheating, 5) Boot from external drive. What symptoms are you seeing?"
        
        elif 'computer' in query_lower:
            return f"{context}For computer issues: 1) Verify all power connections, 2) Check monitor cable, 3) Listen for startup beeps, 4) Try different power outlet, 5) Reseat RAM if comfortable. What happens when you press power?"
        
        # Charging problems
        elif 'charger' in query_lower or ('charging' in query_lower and 'charger' in objects):
            return f"{context}I can see a charger! For charging issues: 1) Try different outlet, 2) Check cable for damage, 3) Clean charging port, 4) Test with different cable, 5) Check if adapter is warm (should be). Is the charging light showing?"
        
        # Study/work problems based on environment
        elif 'study' in query_lower and scene == 'study_area':
            return f"{context}Perfect study environment! For better learning: 1) Use active recall techniques, 2) Take breaks every 25-30 minutes, 3) Eliminate distractions, 4) Practice spaced repetition, 5) Teach concepts aloud. What subject are you struggling with?"
        
        # Focus issues with emotional context
        elif 'focus' in query_lower or 'concentration' in query_lower:
            emotional_advice = ""
            if emotion == 'stressed':
                emotional_advice = " You seem stressed - try deep breathing first. "
            elif emotion == 'tired':
                emotional_advice = " You look tired - consider a short break. "
            
            return f"{context}{emotional_advice}For better focus: 1) Remove phone notifications, 2) Use Pomodoro technique, 3) Organize workspace, 4) Stay hydrated, 5) Try background music. What's distracting you most?"
        
        # General problem solving
        else:
            return f"{context}I'm here to help solve any challenge! Based on what I can see and your emotional state, let's work through this systematically. What specific problem are you facing?"
    
    def _handle_emotional_support(self, emotion, attention, objects):
        """Provide emotional support based on visual cues"""
        context = f"I can see you have {', '.join(objects[:2]) if objects else 'your environment'} around you. "
        
        if emotion == 'sad':
            return f"{context}I notice you seem sad. It's okay to feel this way sometimes. Would you like to talk about what's bothering you, or would you prefer a distraction? I'm here to listen and help however I can."
        elif emotion == 'angry' or emotion == 'frustrated':
            return f"{context}I can see you're feeling frustrated. Take a deep breath - let's work through whatever is causing this stress. What's the main issue you're dealing with right now?"
        elif emotion == 'stressed':
            return f"{context}You seem stressed. Sometimes it helps to step back and organize thoughts. Would you like to talk through what's overwhelming you, or try some quick relaxation techniques?"
        else:
            return f"{context}I'm here to support you through any challenges. What's on your mind today?"
    
    def _handle_general_conversation(self, user_input, objects, scene, emotion, attention, gesture_data):
        """Handle general conversation with full context"""
        context_parts = []
        
        # Build rich context
        if objects:
            context_parts.append(f"I can see {', '.join(objects[:3])}")
        
        if scene != 'general_room':
            context_parts.append(f"you're in a {scene.replace('_', ' ')}")
        
        if emotion != 'neutral':
            context_parts.append(f"you appear {emotion}")
        
        if gesture_data and gesture_data.get('gesture'):
            gesture = gesture_data['gesture'].replace('_', ' ')
            context_parts.append(f"you're making a {gesture} gesture")
        
        context = ". ".join(context_parts) if context_parts else "I can see you clearly"
        
        # Greetings
        if any(greeting in user_input.lower() for greeting in ['hello', 'hi', 'hey']):
            return f"Hello! {context.capitalize()}. I'm your AI assistant with advanced vision and conversation abilities. How can I help you today?"
        
        # Gratitude
        elif 'thank you' in user_input.lower():
            return f"You're very welcome! {context.capitalize()}. I'm always happy to help with any questions or tasks!"
        
        # Capabilities
        elif any(phrase in user_input.lower() for phrase in ['what can you do', 'capabilities', 'help me']):
            return f"I can see and understand your environment - {context}. I can help with: 🧮 Math & counting, 🔬 Science & knowledge, 💻 Tech support, 🎨 Creative tasks, 🧠 Problem solving, 💬 Natural conversation. What interests you?"
        
        # Default response with context
        else:
            return f"I understand what you're saying. {context.capitalize()}. I'm here to help with any questions, problems, or just have a conversation. What would you like to explore?"
    
    def _handle_visual_analysis_advanced(self, query, visual_context):
        """Advanced visual analysis like Gemini"""
        if 'what do you see' in query.lower():
            scene = visual_context['scene'].replace('_', ' ')
            objects = visual_context.get('objects', [])
            faces = len(visual_context.get('face_analysis', {}))
            
            analysis = f"I can see you're in a {scene}"
            if faces > 0:
                analysis += f" with {faces} person{'s' if faces > 1 else ''}"
            if objects:
                analysis += f". I notice {', '.join(objects[:3])}"
            analysis += ". The lighting is good for detailed analysis. What would you like me to focus on?"
            return analysis
        
        elif 'how do i look' in query.lower():
            if visual_context.get('face_analysis'):
                person_data = list(visual_context['face_analysis'].values())[0]
                emotion = person_data.get('emotion', {}).get('primary', 'neutral')
                confidence = person_data.get('emotion', {}).get('confidence', 0)
                return f"You look {emotion} with {confidence:.0%} confidence! You appear engaged and your expression looks great!"
            else:
                return "I can see you clearly! Look directly at the camera for detailed analysis of your expression."
        
        else:
            return "I'm continuously analyzing what I see. The visual processing is working well and I can provide detailed insights about anything in view!"
    
    def _handle_conversation_with_vision(self, query, visual_desc):
        """Handle conversation with visual context"""
        if any(greeting in query.lower() for greeting in ['hello', 'hi', 'hey']):
            return f"Hello! I can see {visual_desc} and I'm ready to help with anything - math, science, programming, creative tasks, or just chat. What's on your mind?"
        elif 'thank you' in query.lower():
            return f"You're very welcome! I can see {visual_desc} and I'm always happy to help with any question or challenge!"
        elif 'how are you' in query.lower():
            return f"I'm excellent! I can see {visual_desc} and all my systems are working perfectly. I'm ready for any question or task!"
        elif 'capabilities' in query.lower() or 'what can you do' in query.lower():
            return f"I'm like Gemini with vision! I can: 🧮 Solve math, 🔬 Explain science, 💻 Help with programming, 🌍 Answer knowledge questions, 🎨 Create stories/poems, 🔧 Solve problems, 👁️ Analyze what I see ({visual_desc}). What interests you?"
        else:
            return f"I can see {visual_desc} and I understand what you're saying. As your AI assistant with vision, I can help with any topic. What would you like to explore?"
    
    def _build_visual_description(self, visual_context):
        """Build natural language description of visual context"""
        descriptions = []
        
        if visual_context['objects']:
            if len(visual_context['objects']) == 1:
                descriptions.append(f"a {visual_context['objects'][0]}")
            elif len(visual_context['objects']) == 2:
                descriptions.append(f"a {visual_context['objects'][0]} and a {visual_context['objects'][1]}")
            else:
                descriptions.append(f"several objects including {', '.join(visual_context['objects'][:2])}")
        
        if visual_context['face_analysis']:
            person_data = list(visual_context['face_analysis'].values())[0]
            emotion = person_data.get('emotion', {}).get('primary', 'neutral')
            if emotion != 'neutral':
                descriptions.append(f"you appear {emotion}")
        
        if visual_context['gesture'] and visual_context['gesture'].get('gesture'):
            gesture = visual_context['gesture']['gesture']
            descriptions.append(f"you're making a {gesture.replace('_', ' ')} gesture")
        
        return ', '.join(descriptions) if descriptions else "your environment"
    
    def _infer_activity(self):
        """Infer what the user might be doing based on visual context"""
        if 'computer_workspace' in self.current_scene:
            return "working on a computer"
        elif 'study_area' in self.current_scene:
            return "studying or reading"
        elif 'busy_workspace' in self.current_scene:
            return "working in a busy environment"
        elif 'screen' in self.detected_objects:
            return "using a computer or device"
        elif 'book' in self.detected_objects:
            return "reading or studying"
        else:
            return "relaxing or having a conversation"
    
    def _get_appearance_compliment(self, emotion):
        """Get appropriate compliment based on emotion"""
        compliments = {
            'happy': "You have a wonderful, bright expression!",
            'neutral': "You look calm and composed.",
            'surprised': "You look alert and engaged!",
            'sad': "I hope everything is okay. You're always welcome to chat.",
            'angry': "You seem intense. Is there something I can help with?"
        }
        return compliments.get(emotion, "You look great!")
    
    def _ai_analysis_loop(self):
        """Continuous AI analysis and learning"""
        while self.is_active:
            try:
                # Update engagement and attention scores
                if self.face_analysis:
                    person_data = list(self.face_analysis.values())[0]
                    self.attention_level = person_data.get('attention', 0)
                    self.engagement_score = person_data.get('engagement', 0)
                
                # Learn from interaction patterns
                self._update_user_profile()
                
                time.sleep(2)  # Analyze every 2 seconds
                
            except Exception as e:
                time.sleep(2)
    
    def _proactive_ai_loop(self):
        """Proactive AI suggestions and interactions"""
        last_proactive_time = time.time()
        
        while self.is_active:
            try:
                if self.personality['proactiveness'] < 0.5:
                    time.sleep(30)
                    continue
                
                current_time = time.time()
                
                # Proactive suggestions every 5 minutes (reduced frequency)
                if current_time - last_proactive_time > 300:  # 5 minutes
                    suggestion = self._generate_proactive_suggestion()
                    if suggestion:
                        self._speak(suggestion)
                        last_proactive_time = current_time
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                time.sleep(60)
    
    def _generate_proactive_suggestion(self):
        """Generate proactive suggestions based on context"""
        suggestions = []
        
        # Based on attention level
        if self.attention_level < 0.3:
            suggestions.append("I notice your attention seems low. Would you like to take a break or try some focusing exercises?")
        
        # Based on detected objects
        if 'screen' in self.detected_objects and self.engagement_score < 0.4:
            suggestions.append("I see you're working on a screen. Remember to take regular breaks to rest your eyes!")
        
        if 'book' in self.detected_objects:
            suggestions.append("I notice you have reading material. Would you like me to help you analyze or discuss what you're studying?")
        
        # Based on time patterns
        hour = datetime.now().hour
        if 14 <= hour <= 16:  # Afternoon
            suggestions.append("It's mid-afternoon - a great time for a quick energy boost. How are you feeling?")
        
        # Based on emotion history
        if len(self.conversation_history) > 5:
            recent_emotions = []
            for entry in list(self.conversation_history)[-5:]:
                if 'face_analysis' in entry['visual_context']:
                    face_data = entry['visual_context']['face_analysis']
                    if face_data:
                        emotion = list(face_data.values())[0].get('emotion', {}).get('primary')
                        if emotion:
                            recent_emotions.append(emotion)
            
            if recent_emotions.count('sad') > 2:
                suggestions.append("I've noticed you seem a bit down lately. Is there anything I can help you with or would you like to talk about something positive?")
        
        return random.choice(suggestions) if suggestions else None
    
    def _update_user_profile(self):
        """Update user profile based on interactions"""
        try:
            # Simple learning - track interaction preferences
            if len(self.conversation_history) > 0:
                recent_entry = self.conversation_history[-1]
                
                # Track preferred interaction times
                hour = datetime.now().hour
                if 'interaction_times' not in self.user_profile['learning_data']:
                    self.user_profile['learning_data']['interaction_times'] = {}
                
                if hour not in self.user_profile['learning_data']['interaction_times']:
                    self.user_profile['learning_data']['interaction_times'][hour] = 0
                
                self.user_profile['learning_data']['interaction_times'][hour] += 1
                
                # Track emotional patterns
                if 'emotional_patterns' not in self.user_profile['learning_data']:
                    self.user_profile['learning_data']['emotional_patterns'] = {}
                
                if 'face_analysis' in recent_entry['visual_context']:
                    face_data = recent_entry['visual_context']['face_analysis']
                    if face_data:
                        emotion = list(face_data.values())[0].get('emotion', {}).get('primary')
                        if emotion:
                            if emotion not in self.user_profile['learning_data']['emotional_patterns']:
                                self.user_profile['learning_data']['emotional_patterns'][emotion] = 0
                            self.user_profile['learning_data']['emotional_patterns'][emotion] += 1
        
        except Exception as e:
            pass  # Silent learning failure
    
    def _capture_and_analyze(self, frame):
        """Capture frame and provide detailed analysis"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_analysis_{timestamp}.png"
        cv2.imwrite(filename, frame)
        
        # Generate detailed analysis
        analysis = self._generate_detailed_analysis()
        
        self._speak(f"I've captured and analyzed the current frame. {analysis}")
        print(f"📸 Saved analysis: {filename}")
        print(f"🧠 Analysis: {analysis}")
    
    def _generate_detailed_analysis(self):
        """Generate detailed analysis of current state"""
        analysis_parts = []
        
        # Scene analysis
        analysis_parts.append(f"You're in a {self.current_scene.replace('_', ' ')}")
        
        # Object analysis
        if self.detected_objects:
            analysis_parts.append(f"I can identify {len(self.detected_objects)} objects: {', '.join(self.detected_objects)}")
        
        # Face analysis
        if self.face_analysis:
            person_data = list(self.face_analysis.values())[0]
            emotion_data = person_data.get('emotion', {})
            emotion = emotion_data.get('primary', 'neutral')
            confidence = emotion_data.get('confidence', 0)
            attention = person_data.get('attention', 0)
            
            analysis_parts.append(f"Your emotional state is {emotion} with {confidence:.0%} confidence and {attention:.0%} attention level")
        
        # Gesture analysis
        if self.gesture_state and self.gesture_state.get('gesture'):
            gesture = self.gesture_state['gesture']
            analysis_parts.append(f"You're making a {gesture.replace('_', ' ')} gesture")
        
        return ". ".join(analysis_parts) + "."
    
    def _cycle_ai_mode(self):
        """Cycle through AI personality modes"""
        modes = ['intelligent_assistant', 'creative_companion', 'analytical_observer', 'friendly_helper']
        current_index = modes.index(self.personality['mode'])
        self.personality['mode'] = modes[(current_index + 1) % len(modes)]
        
        # Adjust personality parameters
        mode_configs = {
            'intelligent_assistant': {'creativity': 0.6, 'helpfulness': 0.9, 'curiosity': 0.7},
            'creative_companion': {'creativity': 0.9, 'helpfulness': 0.7, 'curiosity': 0.8},
            'analytical_observer': {'creativity': 0.4, 'helpfulness': 0.8, 'curiosity': 0.9},
            'friendly_helper': {'creativity': 0.7, 'helpfulness': 1.0, 'curiosity': 0.6}
        }
        
        config = mode_configs[self.personality['mode']]
        self.personality.update(config)
        
        mode_descriptions = {
            'intelligent_assistant': "I'm now in intelligent assistant mode - focused on providing helpful and accurate information.",
            'creative_companion': "I'm now in creative companion mode - ready to explore ideas and think outside the box!",
            'analytical_observer': "I'm now in analytical observer mode - I'll provide detailed analysis and insights.",
            'friendly_helper': "I'm now in friendly helper mode - warm, supportive, and ready to assist!"
        }
        
        self._speak(mode_descriptions[self.personality['mode']])
    
    def _speak(self, text):
        """Advanced text-to-speech with personality"""
        if not text:
            return
        
        try:
            # Adjust speech parameters based on personality
            rate = 165
            if self.personality['mode'] == 'analytical_observer':
                rate = 150  # Slower for analysis
            elif self.personality['mode'] == 'creative_companion':
                rate = 175  # Faster for creativity
            
            self.tts_engine.setProperty('rate', rate)
            
            # Stop any running speech first
            self.tts_engine.stop()
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"AI: {text}")
    
    def _continuous_engagement_monitor(self):
        """Monitor engagement continuously for proactive responses"""
        while self.is_active:
            try:
                if self.face_analysis:
                    person_data = list(self.face_analysis.values())[0]
                    attention = person_data.get('attention', 0)
                    emotion = person_data.get('emotion', {}).get('primary', 'neutral')
                    
                    # Track engagement patterns
                    if attention < 0.3 and self.proactive_responses:
                        self._trigger_engagement_response("low_attention")
                    elif emotion in ['sad', 'frustrated'] and self.context_awareness:
                        self._trigger_engagement_response("emotional_support")
                    elif attention > 0.8:
                        self._trigger_engagement_response("high_engagement")
                
                time.sleep(2)
            except Exception as e:
                time.sleep(2)
    
    def _context_awareness_loop(self):
        """Maintain context awareness across interactions"""
        while self.is_active:
            try:
                # Update contextual understanding
                current_context = {
                    'timestamp': datetime.now().isoformat(),
                    'scene': self.current_scene,
                    'objects': self.detected_objects,
                    'user_state': self._analyze_user_state(),
                    'interaction_quality': self.interaction_quality
                }
                
                # Add to visual memory
                self.visual_memory.append(current_context)
                
                # Analyze context patterns
                self._analyze_context_patterns()
                
                time.sleep(5)
            except Exception as e:
                time.sleep(5)
    
    def _memory_consolidation_loop(self):
        """Consolidate short-term memory to long-term storage"""
        while self.is_active:
            try:
                # Consolidate every 10 minutes
                time.sleep(600)
                
                if len(self.conversation_history) > 10:
                    self._consolidate_memories()
                    self._save_long_term_memory()
                
            except Exception as e:
                time.sleep(600)
    
    def _real_time_adaptation_loop(self):
        """Adapt behavior in real-time based on user feedback"""
        while self.is_active:
            try:
                # Analyze recent interactions for adaptation
                if len(self.conversation_history) > 5:
                    recent_interactions = list(self.conversation_history)[-5:]
                    self._adapt_personality(recent_interactions)
                
                time.sleep(30)
            except Exception as e:
                time.sleep(30)
    
    def _trigger_engagement_response(self, trigger_type):
        """Trigger proactive engagement responses"""
        responses = {
            'low_attention': "I notice you might be getting distracted. Would you like to take a break or refocus?",
            'emotional_support': "I can see you might be feeling down. I'm here if you want to talk about it.",
            'high_engagement': "You seem very focused! This is a great time for productive work."
        }
        
        if trigger_type in responses and time.time() - getattr(self, 'last_proactive_time', 0) > 180:
            print(f"AI Suggestion: {responses[trigger_type]}")
            self.last_proactive_time = time.time()
    
    def _analyze_user_state(self):
        """Analyze comprehensive user state"""
        state = {
            'attention_level': self.attention_level,
            'engagement_score': self.engagement_score,
            'emotional_state': 'neutral',
            'interaction_quality': self.interaction_quality,
            'language_preference': self.current_language
        }
        
        if self.face_analysis:
            person_data = list(self.face_analysis.values())[0]
            state['emotional_state'] = person_data.get('emotion', {}).get('primary', 'neutral')
            state['attention_level'] = person_data.get('attention', 0)
        
        return state
    
    def _consolidate_memories(self):
        """Consolidate short-term memories into long-term storage"""
        try:
            # Extract patterns from recent conversations
            recent_conversations = list(self.conversation_history)[-50:]
            
            # Analyze emotional patterns
            emotions = []
            for conv in recent_conversations:
                if 'visual_context' in conv and 'face_analysis' in conv['visual_context']:
                    face_data = conv['visual_context']['face_analysis']
                    if face_data:
                        emotion = list(face_data.values())[0].get('emotion', {}).get('primary')
                        if emotion:
                            emotions.append(emotion)
            
            # Update long-term memory
            if emotions:
                self.long_term_memory['emotional_baseline'] = {
                    'dominant_emotions': list(set(emotions)),
                    'emotional_stability': len(set(emotions)) / len(emotions) if emotions else 1
                }
            
            # Store interaction patterns
            self.long_term_memory['interaction_history'].append({
                'session_date': datetime.now().isoformat(),
                'conversation_count': len(recent_conversations),
                'dominant_emotion': max(set(emotions), key=emotions.count) if emotions else 'neutral',
                'engagement_quality': self.interaction_quality
            })
            
        except Exception as e:
            print(f"Memory consolidation error: {e}")
    
    def _save_long_term_memory(self):
        """Save long-term memory to persistent storage"""
        try:
            import json
            with open('jarvis_long_term_memory.json', 'w') as f:
                json.dump(self.long_term_memory, f, indent=2)
        except Exception as e:
            print(f"Memory save error: {e}")
    
    def _adapt_personality(self, recent_interactions):
        """Adapt personality based on user feedback and interaction patterns"""
        try:
            # Analyze user response patterns
            positive_responses = 0
            total_responses = len(recent_interactions)
            
            for interaction in recent_interactions:
                user_input = interaction.get('user_input', '').lower()
                if any(word in user_input for word in ['good', 'great', 'thanks', 'helpful', 'perfect']):
                    positive_responses += 1
            
            # Adjust personality parameters
            if total_responses > 0:
                satisfaction_rate = positive_responses / total_responses
                
                if satisfaction_rate > 0.7:
                    self.personality['helpfulness'] = min(1.0, self.personality['helpfulness'] + 0.1)
                elif satisfaction_rate < 0.3:
                    self.personality['creativity'] = min(1.0, self.personality['creativity'] + 0.1)
                    self.personality['empathy'] = min(1.0, self.personality['empathy'] + 0.1)
            
        except Exception as e:
            print(f"Personality adaptation error: {e}")
    
    def _get_phone_frame(self):
        """Get frame from phone camera"""
        try:
            ret, frame = self.camera.read()
            if ret:
                return ret, frame
            else:
                # Try to reconnect
                self.camera.release()
                self.camera = cv2.VideoCapture('http://localhost:8080/video')
                return self.camera.read()
        except Exception as e:
            return False, None
    
    def stop_gemini_vision(self):
        """Stop the advanced vision system with memory consolidation"""
        if not self.is_active:
            return "Advanced Vision AI not active"
        
        self.is_active = False
        
        # Final memory consolidation
        try:
            self._consolidate_memories()
            self._save_long_term_memory()
        except Exception as e:
            print(f"Final memory save error: {e}")
        
        try:
            if self.camera:
                self.camera.release()
            cv2.destroyAllWindows()
            
            # Clean up ADB forwarding
            if self.use_phone_camera:
                try:
                    subprocess.run('C:\\platform-tools\\adb.exe forward --remove tcp:8080', shell=True, capture_output=True)
                except:
                    pass
                
        except Exception as e:
            print(f"Cleanup error: {e}")
        
        print("✅ Gemini Live session ended successfully!")
        return "Gemini Live stopped"
    
    def get_advanced_status(self):
        """Get comprehensive system status"""
        return {
            'active': self.is_active,
            'mediapipe_available': MEDIAPIPE_AVAILABLE,
            'gemini_available': GEMINI_AVAILABLE,
            'current_scene': self.current_scene,
            'detected_objects': self.detected_objects,
            'face_analysis': self.face_analysis,
            'gesture_state': self.gesture_state,
            'attention_level': self.attention_level,
            'engagement_score': self.engagement_score,
            'personality': self.personality,
            'conversation_count': len(self.conversation_history),
            'user_profile': self.user_profile
        }

# Global instance
gemini_vision = GeminiAdvancedVision()

# Public functions
def start_gemini_advanced():
    return gemini_vision.start_gemini_vision()

def stop_gemini_advanced():
    return gemini_vision.stop_gemini_vision()

def get_gemini_status():
    return gemini_vision.get_advanced_status()

def is_gemini_active():
    return gemini_vision.is_active