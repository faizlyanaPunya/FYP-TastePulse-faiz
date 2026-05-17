import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

def render(model_results):
    """Render Model Evaluation tab with performance metrics"""
    
    st.markdown("### Model Evaluation - Test Set Performance")
    
    if not model_results:
        st.warning("⚠️ No models trained yet.")
        return
    
    # Calculate all metrics for evaluation
    all_metrics = {}
    
    for model_name, result in model_results.items():
        y_test = result['y_test']
        y_pred = result['y_pred']
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        all_metrics[model_name] = {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1
        }
    
    # Display metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_list = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    columns = [col1, col2, col3, col4]
    
    for idx, metric in enumerate(metrics_list):
        with columns[idx]:
            st.markdown(f"### {metric}")
            for model_name, metrics in all_metrics.items():
                value = metrics[metric]
                st.metric(model_name, f"{value:.3f}")
    
    st.markdown("---")
    
    # Comparison chart
    metrics_df = pd.DataFrame(all_metrics).T
    
    fig_metrics = go.Figure()
    for metric in metrics_df.columns:
        fig_metrics.add_trace(go.Bar(
            name=metric,
            x=metrics_df.index,
            y=metrics_df[metric],
            text=[f"{val:.3f}" for val in metrics_df[metric]],
            textposition='auto',
        ))
    
    fig_metrics.update_layout(
        title="Model Metrics Comparison",
        barmode='group',
        xaxis_title="Model",
        yaxis_title="Score",
        yaxis=dict(range=[0, 1]),
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_metrics, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed model analysis
    st.markdown("### Detailed Model Analysis")
    
    for model_name, result in model_results.items():
        with st.expander(f"📈 {model_name} Details", expanded=False):
            y_test = result['y_test']
            y_pred = result['y_pred']
            
            col1, col2 = st.columns(2)
            
            # Confusion Matrix
            with col1:
                cm = confusion_matrix(y_test, y_pred)
                unique_labels = sorted(set(y_test) | set(y_pred))
                
                fig_cm = go.Figure(data=go.Heatmap(
                    z=cm,
                    x=unique_labels,
                    y=unique_labels,
                    colorscale="Blues",
                    text=cm,
                    texttemplate="%{text}",
                    hovertemplate="True: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>"
                ))
                fig_cm.update_layout(
                    title="Confusion Matrix",
                    xaxis_title="Predicted Label",
                    yaxis_title="True Label",
                    height=400
                )
                st.plotly_chart(fig_cm, use_container_width=True)
            
            # Classification Report
            with col2:
                report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
                report_df = pd.DataFrame(report).transpose()
                report_df = report_df[["precision", "recall", "f1-score", "support"]]
                report_df.columns = ["Precision", "Recall", "F1-Score", "Support"]
                
                # Round to avoid Jinja2 dependency
                report_df = report_df.round(3)
                
                st.markdown("#### Classification Report")
                st.dataframe(report_df, use_container_width=True)
            
            # Label distribution
            dist_data = pd.DataFrame({
                "True Labels": y_test.value_counts().sort_index(),
                "Predicted Labels": pd.Series(y_pred).value_counts().sort_index()
            }).fillna(0)
            
            fig_dist = go.Figure(data=[
                go.Bar(name="True", x=dist_data.index, y=dist_data["True Labels"]),
                go.Bar(name="Predicted", x=dist_data.index, y=dist_data["Predicted Labels"])
            ])
            fig_dist.update_layout(
                title="True vs Predicted Label Distribution",
                xaxis_title="Sentiment Label",
                yaxis_title="Count",
                barmode="group",
                height=400
            )
            st.plotly_chart(fig_dist, use_container_width=True)