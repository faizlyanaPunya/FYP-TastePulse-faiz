import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, SpatialDropout1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import warnings
import time
warnings.filterwarnings('ignore')

def train_models(df, models_config):
    """
    Train specified models on the dataset.
    
    Args:
        df: Input DataFrame with 'text' and 'sentiment' columns
        models_config: Dict with 'train_multinomial' and 'train_lstm' boolean flags
    
    Returns:
        model_results: Dict containing trained models and predictions
        models_trained: Boolean flag
        test_df: Test data (20% split) with predictions for insights
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Prepare data
        status_text.text("Preparing data...")
        progress_bar.progress(10)
        
        X = df['text'].fillna('')
        y = df['sentiment']
        
        mask = X.str.len() > 0
        X = X[mask]
        y = y[mask]
        
        # Get indices for test data to preserve other columns
        X_train, X_test, y_train, y_test, train_idx, test_idx = train_test_split(
            X, y, X.index, test_size=0.2, random_state=42, stratify=y
        )
        
        model_results = {}
        predictions = {}
        
        # Train Multinomial Naive Bayes
        if models_config['train_multinomial']:
            status_text.text("Training Multinomial Naive Bayes...")
            progress_bar.progress(40)
            
            vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
            X_train_vec = vectorizer.fit_transform(X_train)
            X_test_vec = vectorizer.transform(X_test)
            
            mnb_model = MultinomialNB()
            mnb_model.fit(X_train_vec, y_train)
            y_pred_mnb = mnb_model.predict(X_test_vec)
            
            model_results['MultinomialNB'] = {
                'model': mnb_model,
                'y_pred': y_pred_mnb,
                'y_test': y_test,
                'vectorizer': vectorizer,
                'X_test_vec': X_test_vec
            }
            predictions['MultinomialNB'] = y_pred_mnb
        
        # Train LSTM
        if models_config['train_lstm']:
            status_text.text("Tokenizing text for LSTM...")
            progress_bar.progress(60)
            
            tokenizer = Tokenizer(num_words=5000)
            tokenizer.fit_on_texts(X_train)
            X_train_seq = tokenizer.texts_to_sequences(X_train)
            X_test_seq = tokenizer.texts_to_sequences(X_test)
            
            max_len = 100
            X_train_pad = pad_sequences(X_train_seq, maxlen=max_len)
            X_test_pad = pad_sequences(X_test_seq, maxlen=max_len)
            
            unique_classes = np.unique(y_train)
            class_to_idx = {cls: idx for idx, cls in enumerate(unique_classes)}
            y_train_encoded = np.array([class_to_idx[cls] for cls in y_train])
            
            status_text.text("Training LSTM model...")
            progress_bar.progress(75)
            
            lstm_model = Sequential([
                Embedding(input_dim=5000, output_dim=128, input_length=max_len),
                SpatialDropout1D(0.2),
                LSTM(100, dropout=0.2, recurrent_dropout=0.2),
                Dense(64, activation='relu'),
                Dense(len(unique_classes), activation='softmax')
            ])
            
            lstm_model.compile(
                optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )
            
            lstm_model.fit(
                X_train_pad, y_train_encoded,
                epochs=5,
                batch_size=32,
                validation_split=0.1,
                verbose=0
            )
            
            status_text.text("Generating LSTM predictions...")
            progress_bar.progress(90)
            
            y_pred_lstm_encoded = np.argmax(lstm_model.predict(X_test_pad, verbose=0), axis=1)
            idx_to_class = {idx: cls for cls, idx in class_to_idx.items()}
            y_pred_lstm = np.array([idx_to_class[idx] for idx in y_pred_lstm_encoded])
            
            model_results['LSTM'] = {
                'model': lstm_model,
                'y_pred': y_pred_lstm,
                'y_test': y_test,
                'tokenizer': tokenizer
            }
            predictions['LSTM'] = y_pred_lstm
        
        # Create test dataframe with predictions
        status_text.text("Preparing test data for insights...")
        progress_bar.progress(95)
        
        test_df = df.loc[test_idx].copy()
        
        # Add predictions from the first trained model
        first_model = list(predictions.keys())[0]
        test_df['predicted_sentiment'] = predictions[first_model]
        test_df['true_sentiment'] = y_test.values
        
        # Convert date if exists
        if 'createTimeISO' in test_df.columns:
            test_df['date'] = pd.to_datetime(test_df['createTimeISO'], errors='coerce')
        elif 'date' in test_df.columns:
            test_df['date'] = pd.to_datetime(test_df['date'], errors='coerce')
        
        status_text.text("Training complete!")
        progress_bar.progress(100)
        
        # Clear progress indicators after a brief delay to keep UI clean
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        st.toast("✅ Training complete!", icon="🚀")
        
        return model_results, True, test_df
        
    except Exception as e:
        st.error(f"❌ Error during training: {str(e)}")
        return {}, False, None

