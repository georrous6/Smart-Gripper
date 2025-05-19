import cv2
import numpy as np
import tensorflow as tf

# Φόρτωσε το MobileNetV2 με weights από το ImageNet
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Λίστα με keywords που θέλουμε να αναγνωρίσουμε
TARGET_KEYWORDS = ['pop_bottle', 'balloon', 'cell_phone']  # ακριβή ονόματα από ImageNet

def preprocess_frame(frame):
    resized = cv2.resize(frame, (224, 224))
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(resized)
    return np.expand_dims(img_array, axis=0)

def detect_object():
    cap = cv2.VideoCapture(0)
    result = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        input_tensor = preprocess_frame(frame)
        preds = model.predict(input_tensor)
        decoded_preds = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=5)[0]

        label = "Not detected"
        for _, name, confidence in decoded_preds:
            if name in TARGET_KEYWORDS:
                label = f"{name}: {confidence*100:.2f}%"
                if name == "balloon":
                    result = "b"
                elif name == "pop_bottle":
                    result = "c"
                elif name == "cell_phone":
                    result = "p"
                break

        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Object Recognition", frame)

        # Αν βρέθηκε αντικείμενο ή πατηθεί 'q', σταμάτα
        if result is not None or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()
    return result
