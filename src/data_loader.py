import pandas as pd

def load_data(csv_path):
    df = pd.read_csv(csv_path)

    df['createTimeISO'] = pd.to_datetime(
        df['createTimeISO'],
        format='%m/%d/%Y %H:%M:%S',
        errors='coerce'
    )

    df['positive'] = pd.to_numeric(df['positive'], errors='coerce')
    df['neutral'] = pd.to_numeric(df['neutral'], errors='coerce')
    df['negative'] = pd.to_numeric(df['negative'], errors='coerce')

    df['sentiment_score'] = df['positive'] - df['negative']
    df = df.dropna(subset=['createTimeISO', 'sentiment_score'])

    df['date'] = df['createTimeISO'].dt.date
    df['place'] = df['place'].astype(str).str.strip()
    df['sentiment'] = df['sentiment'].astype(str).str.lower().str.strip()

    return df