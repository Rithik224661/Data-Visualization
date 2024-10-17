from application import app
from flask import render_template, request, jsonify
import pandas as pd
import json
import plotly
import plotly.express as px

df = pd.read_json('application/jsondata.json')

@app.route("/")
def index():
    return render_template("index.html", title="Home")

@app.route("/api/data")
def get_data():
    filtered_df = apply_filters(df, request.args)
    filtered_df['intensity'] = pd.to_numeric(filtered_df['intensity'], errors='coerce')
    filtered_df['likelihood'] = pd.to_numeric(filtered_df['likelihood'], errors='coerce')
    filtered_df['relevance'] = pd.to_numeric(filtered_df['relevance'], errors='coerce')
    filtered_df['end_year'] = pd.to_numeric(filtered_df['end_year'], errors='coerce')
    
    filtered_df = filtered_df.fillna(0)

    intensity_likelihood = px.scatter(filtered_df, x="intensity", y="likelihood", color="region", hover_data=['country'])
    relevance_year = px.line(filtered_df.groupby('end_year')['relevance'].mean().reset_index(), x='end_year', y='relevance')
    
    topics_df = filtered_df['topic'].value_counts().reset_index()
    topics_df.columns = ['topic', 'count']
    topics = px.pie(topics_df, names='topic', values='count')
    
    region_df = filtered_df['region'].value_counts().reset_index()
    region_df.columns = ['region', 'count']
    region = px.bar(region_df, x='region', y='count')

    data_table = filtered_df.to_dict('records')
    return jsonify({
        'intensity_likelihood': json.loads(intensity_likelihood.to_json()),
        'relevance_year': json.loads(relevance_year.to_json()),
        'topics': json.loads(topics.to_json()),
        'region': json.loads(region.to_json()),
        'data_table': data_table
    })


@app.route("/api/filter_options")
def get_filter_options():
    df['end_year'] = pd.to_numeric(df['end_year'], errors='coerce')
    df['end_year'] = df['end_year'].dropna().astype(int)

    filters = {
        'end_year': sorted(df['end_year'].unique().tolist()),
        'topics': sorted(df['topic'].unique().tolist()),
        'sector': sorted(df['sector'].unique().tolist()),
        'region': sorted(df['region'].unique().tolist()),
        'pest': sorted(df['pestle'].unique().tolist()),
        'source': sorted(df['source'].unique().tolist()),
        'country': sorted(df['country'].unique().tolist())
    }

    if 'swot' in df.columns:
        filters['swot'] = sorted(df['swot'].unique().tolist())
    if 'city' in df.columns:
        filters['city'] = sorted(df['city'].unique().tolist())

    return jsonify(filters)

def apply_filters(df, filters):
    if filters.get('end_year'):
        df = df[df['end_year'] == int(filters['end_year'])]
    if filters.get('topics'):
        df = df[df['topic'].isin(filters['topics'].split(','))]
    if filters.get('sector'):
        df = df[df['sector'] == filters['sector']]
    if filters.get('region'):
        df = df[df['region'] == filters['region']]
    if filters.get('pest'):
        df = df[df['pestle'] == filters['pest']]
    if filters.get('source'):
        df = df[df['source'] == filters['source']]
    if filters.get('swot'):
        df = df[df['swot'] == filters['swot']]
    if filters.get('country'):
        df = df[df['country'] == filters['country']]
    if filters.get('city'):
        df = df[df['city'] == filters['city']]
    return df
