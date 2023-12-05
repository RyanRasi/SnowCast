from tensorflow.keras.models import load_model

# Load the saved model
model = load_model('model.h5')

# Use the loaded model for predictions or further training
predictions = model.predict(X_test)