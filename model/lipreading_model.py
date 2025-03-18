import tensorflow as tf
from tensorflow.keras.layers import Input, Conv3D, MaxPool3D, TimeDistributed, Flatten, Bidirectional, LSTM, Dropout, Dense
from tensorflow.keras.models import Model
from config import LIPREADING_MODEL_PATH, VOCAB

def get_string_lookup_layers(vocab):
    char_to_num = tf.keras.layers.StringLookup(vocabulary=vocab, oov_token="")
    num_to_char = tf.keras.layers.StringLookup(vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True)
    return char_to_num, num_to_char

char_to_num, num_to_char = get_string_lookup_layers(VOCAB)

class LipreadingModel:
    def __init__(self, model_path: str = LIPREADING_MODEL_PATH):
        self.model = self._build_model()
        print(model_path)
        self.model.load_weights(model_path)

    def _build_model(self):
        inputs = Input(shape=(None, 46, 140, 1), name="input")
        x = Conv3D(128, 3, padding='same', activation='relu')(inputs)
        x = MaxPool3D((1, 2, 2))(x)
        x = Conv3D(256, 3, padding='same', activation='relu')(x)
        x = MaxPool3D((1, 2, 2))(x)
        x = Conv3D(75, 3, padding='same', activation='relu')(x)
        x = MaxPool3D((1, 2, 2))(x)
        x = TimeDistributed(Flatten())(x)
        x = Bidirectional(LSTM(128, kernel_initializer='Orthogonal', return_sequences=True))(x)
        x = Dropout(0.5)(x)
        x = Bidirectional(LSTM(128, kernel_initializer='Orthogonal', return_sequences=True))(x)
        x = Dropout(0.5)(x)
        outputs = Dense(char_to_num.vocabulary_size() + 1, kernel_initializer='he_normal', activation='softmax')(x)
        model = Model(inputs=inputs, outputs=outputs)
        return model

    def predict(self, frames: tf.Tensor) -> str:
        if len(frames.shape) == 4:
            frames = tf.expand_dims(frames, axis=0)
        yhat = self.model.predict(frames)
        decoded, _ = tf.keras.backend.ctc_decode(yhat, input_length=[yhat.shape[1]], greedy=True)
        decoded = decoded[0][0].numpy()
        prediction = tf.strings.reduce_join(num_to_char(decoded)).numpy().decode('utf-8').strip()
        return prediction
