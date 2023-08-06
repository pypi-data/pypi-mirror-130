import pandas as pd
import geopandas as gpd
import folium
from shapely import wkt
from shapely.geometry import LineString, shape
import shapely.speedups
shapely.speedups.enable()
from IPython.display import clear_output

def choose_most_recent_geometry(df, geometry_col = 'polygon_wkt', date_col = 'date_range_start'):
    """
    Chooses the most recent geometry for each Placekey in the event that
    `df` contains multiple patterns releases.
    """

    if date_col in df.columns:
        output = df.sort_values(by = date_col, na_position = 'first')
        output = output.drop_duplicates('placekey', keep = 'last')
    else:
        output = df.drop_duplicates('placekey', keep = 'last')
    
    return output

def make_geometry(df, geometry_col = 'polygon_wkt', crs = 'EPSG:4326'):
    """
    Constructs a GeoPandas GeoDataFrame using the polygon_wkt column.
    """

    output = gpd.GeoDataFrame(df, geometry = gpd.GeoSeries.from_wkt(df[geometry_col]), crs = crs)
    
    return output

def choose_poi_and_neighbors(gdf, placekey, neighbor_radius, projection = 'EPSG:3857'):
    """
    Identifies the "target" POI and its nearby neighbors, based on the `neighbor_radius` parameter (by default expressed in meters).
    """

    # classify Neighbors v. Target POI
    gdf['POI'] = 'Neighbor'
    gdf.loc[gdf['placekey'] == placekey, 'POI'] = 'Target'
    
    # transform to a projected coordinate reference system
    gdf_proj = gdf.to_crs(projection)
    
    # get the buffer for filtering neighbors
    target = gdf_proj.loc[gdf_proj['POI'] == 'Target']
    target_buffer = target.geometry.buffer(neighbor_radius)
    
    # find the neighbors
    output_proj = gdf_proj.loc[gdf_proj.intersects(target_buffer.unary_union)]
    
    # transform back to original coordinate reference system
    output = output_proj.to_crs(gdf.crs)
    
    return output
    
def map_poi_and_neighbors(map_df, basemap = 'ESRI_imagery'):
    """
    Maps the "target" POI polygon and its neighbors.
    Options for basemap include "ESRI_imagery" or "OSM"
    """

    # center map
    center = map_df.loc[map_df['POI'] == 'Target']
        
    map_df_grouped = map_df.groupby(['polygon_wkt', 'is_synthetic', 'polygon_class', 'enclosed', 'includes_parking_lot'])['location_name'].apply(list).reset_index(name = 'location_names')
    map_df_grouped['location_names_sample'] = map_df_grouped['location_names'].str[:3]
    map_df_grouped['total_POI_count'] = map_df_grouped['location_names'].apply(len)
    map_df_grouped = map_df_grouped.merge(map_df.loc[map_df['POI'] == 'Target'][['polygon_wkt', 'POI']], on = 'polygon_wkt', how = 'outer')
    map_df_grouped.loc[map_df_grouped['POI'].isnull(), 'POI'] = 'Neighbor'
    
    map_df_grouped = gpd.GeoDataFrame(map_df_grouped, geometry = gpd.GeoSeries.from_wkt(map_df_grouped['polygon_wkt']), crs = 'EPSG:4326')
    
    # initialize map
    if basemap.lower() == 'esri_imagery':
        map_ = folium.Map(location = [center["latitude"], center["longitude"]], zoom_start = 19)
        
        tile  = folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            overlay = False,
            control = True
           ).add_to(map_)
        
    elif basemap.lower() == 'osm':
        map_ = folium.Map(location = [center["latitude"], center["longitude"]], zoom_start = 19, tiles = 'OpenStreetMap')
    
    
    # tool tip list
    tool_tip_cols = ['total_POI_count', 'location_names_sample', 'is_synthetic', 'polygon_class', 'enclosed', 'includes_parking_lot']
    
    # draw map
    folium.GeoJson(
        map_df_grouped,
        style_function = lambda x: {
            'weight':0,
            'color':'red' if x['properties']['POI'] == 'Target' else 'blue',
            'fillOpacity': 0.7 if x['properties']['POI'] == 'Target' else 0.2,
        },
        tooltip = folium.features.GeoJsonTooltip(
            fields = tool_tip_cols
        )
    ).add_to(map_)
    
    return map_

def verify_POI_geometry(df, placekeys = None, basemap = 'ESRI_imagery', neighbor_radius = 50, geometry_col = 'polygon_wkt'):
    """
    Main function for evaluating polygon_wkts.
    Returns a dataframe for the Placekeys that were evaluated with "rating" and "comment" columns appended.

    Optionally specify a list of placekeys of interest in the `placekeys` parameter, or specify None to loop through every row in the df.
    """

    df = choose_most_recent_geometry(df, geometry_col = geometry_col, date_col = 'date_range_start')
    gdf = make_geometry(df, geometry_col = geometry_col)
    
    # map
    output_pks = []
    ratings = []
    comments = []
    
    prompt = '''
    Rate polygon from 1 to 7. 
    Add an optional comment after a comma. Example input: "5, polygon extends into roadway."
    Type "quit" to exit.
    '''
    
    if placekeys is None:
        placekeys = list(df['placekey'])
    for pk in placekeys:
        map_df = choose_poi_and_neighbors(gdf, placekey = pk, neighbor_radius = neighbor_radius).reset_index(drop = True)
        display(map_poi_and_neighbors(map_df, basemap = basemap))
        input_ = input(prompt)
        if "quit" in input_.lower():
            break
        else:
            rating, *comment = input_.split(',')
            comment = comment[0] if comment else ''

            output_pks.append(pk)
            ratings.append(int(rating))
            comments.append(comment.lstrip()) # remove any leading space
            clear_output(wait=True)
    
    ratings_df = pd.DataFrame({'placekey':output_pks, 'rating':ratings, 'comment':comments})
    output = df.merge(ratings_df, on = 'placekey')
    clear_output(wait=True)
    
    return output