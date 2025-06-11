import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def create_visualization(df, viz_type, config):
    """
    Create a visualization based on the type and configuration
    
    Args:
        df (pandas.DataFrame): Dataframe to visualize
        viz_type (str): Type of visualization (bar, line, scatter, etc.)
        config (dict): Configuration for the visualization
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    # Extract configuration
    x = config.get('x')
    y = config.get('y')
    title = config.get('title', '')
    color = config.get('color')
    
    # Ensure the columns exist in the dataframe
    if x and x not in df.columns:
        return go.Figure().add_annotation(
            text=f"Column '{x}' not found in dataframe",
            showarrow=False,
            font=dict(size=14)
        )
    
    if y and y not in df.columns:
        return go.Figure().add_annotation(
            text=f"Column '{y}' not found in dataframe",
            showarrow=False,
            font=dict(size=14)
        )
    
    # Create visualization based on type
    if viz_type == 'bar':
        if x and y:
            # Group by x and calculate mean of y
            grouped_df = df.groupby(x)[y].mean().reset_index()
            fig = px.bar(grouped_df, x=x, y=y, title=title, color=color)
        else:
            fig = go.Figure().add_annotation(
                text="Bar chart requires 'x' and 'y' columns",
                showarrow=False,
                font=dict(size=14)
            )
    
    elif viz_type == 'line':
        if x and y:
            # Sort by x for better line charts
            sorted_df = df.sort_values(by=x)
            fig = px.line(sorted_df, x=x, y=y, title=title, color=color)
        else:
            fig = go.Figure().add_annotation(
                text="Line chart requires 'x' and 'y' columns",
                showarrow=False,
                font=dict(size=14)
            )
    
    elif viz_type == 'scatter':
        if x and y:
            fig = px.scatter(df, x=x, y=y, title=title, color=color)
        else:
            fig = go.Figure().add_annotation(
                text="Scatter plot requires 'x' and 'y' columns",
                showarrow=False,
                font=dict(size=14)
            )
    
    elif viz_type == 'pie':
        if x:
            # Count occurrences for pie chart
            counts = df[x].value_counts().reset_index()
            counts.columns = [x, 'count']
            fig = px.pie(counts, values='count', names=x, title=title)
        else:
            fig = go.Figure().add_annotation(
                text="Pie chart requires 'x' column",
                showarrow=False,
                font=dict(size=14)
            )
    
    elif viz_type == 'histogram':
        if x:
            fig = px.histogram(df, x=x, title=title, color=color)
        else:
            fig = go.Figure().add_annotation(
                text="Histogram requires 'x' column",
                showarrow=False,
                font=dict(size=14)
            )
    
    elif viz_type == 'heatmap':
        if x and y:
            # Create a pivot table for heatmap
            pivot_data = df.pivot_table(index=y, columns=x, aggfunc='size', fill_value=0)
            fig = px.imshow(pivot_data, title=title)
        else:
            fig = go.Figure().add_annotation(
                text="Heatmap requires 'x' and 'y' columns",
                showarrow=False,
                font=dict(size=14)
            )
    
    elif viz_type == 'box':
        if x and y:
            fig = px.box(df, x=x, y=y, title=title, color=color)
        else:
            fig = go.Figure().add_annotation(
                text="Box plot requires 'x' and 'y' columns",
                showarrow=False,
                font=dict(size=14)
            )
    
    elif viz_type == 'violin':
        if x and y:
            fig = px.violin(df, x=x, y=y, title=title, color=color)
        else:
            fig = go.Figure().add_annotation(
                text="Violin plot requires 'x' and 'y' columns",
                showarrow=False,
                font=dict(size=14)
            )
    
    elif viz_type == 'treemap':
        if x:
            # Count occurrences for treemap
            counts = df[x].value_counts().reset_index()
            counts.columns = [x, 'count']
            fig = px.treemap(counts, path=[x], values='count', title=title)
        else:
            fig = go.Figure().add_annotation(
                text="Treemap requires 'x' column",
                showarrow=False,
                font=dict(size=14)
            )
    
    elif viz_type == 'table':
        if x:
            # Create a table with selected columns
            columns = [x]
            if y:
                columns.append(y)
            
            table_data = df[columns].head(10)  # Show only first 10 rows
            
            fig = go.Figure(data=[go.Table(
                header=dict(values=list(table_data.columns),
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=[table_data[col] for col in table_data.columns],
                           fill_color='lavender',
                           align='left'))
            ])
            fig.update_layout(title=title)
        else:
            fig = go.Figure().add_annotation(
                text="Table requires at least 'x' column",
                showarrow=False,
                font=dict(size=14)
            )
    
    else:
        # Default case for unsupported visualization types
        fig = go.Figure().add_annotation(
            text=f"Visualization type '{viz_type}' not supported",
            showarrow=False,
            font=dict(size=14)
        )
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y,
        template="plotly_white"
    )
    
    return fig

def render_chart_in_streamlit(fig):
    """Mostra un grafico in Streamlit."""
    st.plotly_chart(fig, use_container_width=True)

def suggest_visualizations(df: pd.DataFrame) -> list:
    """
    Suggerisce grafici in base al contenuto del dataframe.
    
    Args:
        df (pandas.DataFrame): Dataframe to analyze
        
    Returns:
        list: List of visualization suggestions
    """
    suggestions = []
    numeric_columns = df.select_dtypes(include='number').columns.tolist()
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    date_columns = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
    
    # Bar chart for categorical vs numeric
    if len(categorical_columns) > 0 and len(numeric_columns) > 0:
        suggestions.append({
            "type": "bar",
            "config": {
                "x": categorical_columns[0],
                "y": numeric_columns[0],
                "title": f"Media di {numeric_columns[0]} per {categorical_columns[0]}"
            },
            "description": f"Mostra la media di {numeric_columns[0]} per ogni categoria di {categorical_columns[0]}"
        })
    
    # Pie chart for categorical
    if len(categorical_columns) > 0:
        suggestions.append({
            "type": "pie",
            "config": {
                "x": categorical_columns[0],
                "title": f"Distribuzione di {categorical_columns[0]}"
            },
            "description": f"Mostra la distribuzione delle categorie di {categorical_columns[0]}"
        })
    
    # Histogram for numeric
    if len(numeric_columns) > 0:
        suggestions.append({
            "type": "histogram",
            "config": {
                "x": numeric_columns[0],
                "title": f"Distribuzione di {numeric_columns[0]}"
            },
            "description": f"Mostra la distribuzione dei valori di {numeric_columns[0]}"
        })
    
    # Line chart for date vs numeric
    if len(date_columns) > 0 and len(numeric_columns) > 0:
        suggestions.append({
            "type": "line",
            "config": {
                "x": date_columns[0],
                "y": numeric_columns[0],
                "title": f"Trend di {numeric_columns[0]} nel tempo"
            },
            "description": f"Mostra l'andamento di {numeric_columns[0]} nel tempo"
        })
    
    # Scatter plot for numeric vs numeric
    if len(numeric_columns) > 1:
        suggestions.append({
            "type": "scatter",
            "config": {
                "x": numeric_columns[0],
                "y": numeric_columns[1],
                "title": f"Relazione tra {numeric_columns[0]} e {numeric_columns[1]}"
            },
            "description": f"Mostra la relazione tra {numeric_columns[0]} e {numeric_columns[1]}"
        })
    
    return suggestions
