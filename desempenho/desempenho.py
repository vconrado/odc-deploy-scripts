import datacube
from shapely.wkt import loads
from shapely import geometry
import time
import numpy as np
import pandas as pd
import geopandas as gpd
#import matplotlib.pyplot as plt
from time import gmtime, strftime
import os
import threading
import time

dc = datacube.Datacube()

def get_prod_cell_size(product):
    cell_size = 0
    for m in product.measurements:
        cell_size = cell_size + np.dtype(product.measurements[m].dtype).itemsize
    return cell_size


def get_data(product, x, y, time):
    if time is None:
        return dc.load(product = product.name,
                        x = x,
                        y = y,
                        output_crs = product.grid_spec.crs,
                        crs = product.grid_spec.crs.crs_str,
                        resolution = product.grid_spec.resolution)
    else:
        return dc.load(product = product.name,
                        x = x,
                        y = y,
                        time = time,
                        output_crs = product.grid_spec.crs,
                        crs = product.grid_spec.crs.crs_str,
                        resolution = product.grid_spec.resolution)


def test_func(test_name, product_name, x_steps, y_steps, ts=False, time_lst=None, maximo=None):
    product = dc.index.products.get_by_name(product_name)
    
    print("Running {}:{}  ".format(test_name, product_name))

    # calc cell size
    cell_size = get_prod_cell_size(product)
        
    ds_lst = dc.find_datasets(product=product.name)
    product_bbox = datacube.api.core.get_bounds(ds_lst, product.grid_spec.crs)

    sp = loads(product_bbox.wkt)
    xs, ys = sp.exterior.xy

    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs)
    max_y = max(ys)

    dx = (max_x - min_x)/(x_steps)
    dy = (max_y - min_y)/(y_steps)

    x0 = min_x
    y0 = min_y
    count = 0
    d = []

    for i in range(0,x_steps):
        x = x0 + i*dx
        for j in range(0, y_steps):
            y = y0 + j*dy

            start_time = time.time()
            if ts is True:
                data = get_data(product, x+dx/2, y+dx/2, time_lst)
            else:
                data = get_data(product, (x, x+dx), (y, y+dy), time_lst)
            dif_time = (time.time() - start_time)
            
            
            if ts is True:
                geom = geometry.Point([x+dx/2, y+dx/2])
            else:
                geom = geometry.Polygon([[x, y],
                                     [x+dx, y],
                                     [x+dx, y+dy],
                                     [x, y+dy],
                                     [x, y]])
            
            data_loaded_B=data.sizes["x"] * data.sizes["y"] * data.sizes["time"] * cell_size
            MB_s = (data_loaded_B/(1025*1024))/dif_time
            
            
            d.append({        
                    "prod": product.name,
                    "count": count, 
                    "x0": x, 
                    "xf": x+dx, 
                    "y0": y, 
                    "yf": y+dy, 
                    "x_size": data.sizes["x"], 
                    "y_size":data.sizes["y"], 
                    "time_size": data.sizes["time"],
                    "data_loaded_B":data_loaded_B,
                    "MB_s":MB_s,
                    "dif_time": dif_time,
                    "geom": geom
            })
            data = None
            count=count+1
            # TODO remover (só para teste)
            print("{}".format(count))
            if maximo is not None:
                if count >= maximo:
                    print("Parou pelo maximo")
                    df = pd.DataFrame(d)
                    return gpd.GeoDataFrame(df, geometry='geom', crs={'init': product.grid_spec.crs.crs_str})
                
    df = pd.DataFrame(d)
    return gpd.GeoDataFrame(df, geometry='geom', crs={'init': product.grid_spec.crs.crs_str})


def the_thread(test_name, product, x, dx, y, dy, time_lst, ts, cell_size, data, index):
    print("the_thread({},{},{},{},{},{},{},{},{})".format(test_name, product, x, dx, y, dy, time_lst, ts, index))
    if ts is True:
        geom = geometry.Point([x+dx/2, y+dx/2])
    else:
        geom = geometry.Polygon([[x, y],
                             [x+dx, y],
                             [x+dx, y+dy],
                             [x, y+dy],
                             [x, y]])
    start_time = time.time()
    if ts is True:
        data = get_data(product, x+dx/2, y+dx/2, time_lst)
    else:
        data = get_data(product, (x, x+dx), (y, y+dy), time_lst)
    dif_time = (time.time() - start_time)

    data_loaded_B=data.sizes["x"] * data.sizes["y"] * data.sizes["time"] * cell_size
    MB_s = (data_loaded_B/(1025*1024))/dif_time

    d = {        
        "prod": product.name,
        "count": index, 
        "x0": x, 
        "xf": x+dx, 
        "y0": y, 
        "yf": y+dy, 
        "x_size": data.sizes["x"], 
        "y_size":data.sizes["y"], 
        "time_size": data.sizes["time"],
        "data_loaded_B":data_loaded_B,
        "MB_s":MB_s,
        "dif_time": dif_time,
        "geom": geom
        }
    result[index] = d
    print("Thread {}.{}#{} finalizada".format(test_name, product.name, index))
        

def p_test_func(threads, test_name, product_name, x_steps, y_steps, ts=False, time_lst=None, maximo=None):
    product = dc.index.products.get_by_name(product_name)
    
    print("Running {}:{}  ".format(test_name, product_name))
    
    # calc cell size
    cell_size = get_prod_cell_size(product)
        
    ds_lst = dc.find_datasets(product=product.name)
    product_bbox = datacube.api.core.get_bounds(ds_lst, product.grid_spec.crs)
    
    sp = loads(product_bbox.wkt)
    xs, ys = sp.exterior.xy
    
    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs)
    max_y = max(ys)

    dx = (max_x - min_x)/(x_steps)
    dy = (max_y - min_y)/(y_steps)
    
    x0 = min_x
    y0 = min_y
    count = 0
    result = []

    if maximo is None:
        maximo = float("inf")

    threads = []    
    for i in range(0,x_steps):
        x = x0 + i*dx
        for j in range(0, y_steps):
            y = y0 + j*dy
            if count < maximo:
                args = (test_name, product, x, dx, y, dy, time_lst, ts, cell_size, result, count)
                t = threading.Thread(target=the_thread,args=args)
                threads.append(t)
            
            count=count+1
    
    for i in range(0, len(threads)):
        threads[i].start();
    
    print("Aguardando finalizacao das threads");
    for i in range(0, len(threads)):
        threads[i].join();
    
    df = pd.DataFrame(result)
    return gpd.GeoDataFrame(df, geometry='geom', crs={'init': product.grid_spec.crs.crs_str})



def save_gdf(gdf, product_name, rodada, subdir, columns=None):
    base_path = "/datacube/scripts/desempenho/dados"
    directory = "{}/{}/{}/{}".format(base_path, rodada, product_name, subdir)
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_shp = "{}/{}.shp".format(directory, subdir)
    # shp
    gdf.to_file(file_shp)
    #csv
    file_csv = "{}/{}.csv".format(directory, subdir)
    if columns is not None:
        gdf[columns].to_csv(file_csv, index=False)
    else:
        gdf.to_csv(file_csv, index=False)
    
    
def dataset_gdf(product_name):
    ds_lst = dc.find_datasets(product=product_name)
    d = []
    for ds in ds_lst:
        d.append({
            "id": str(ds.id),
            "product": ds.type.name,
            "geom": loads(ds.extent.wkt),
            "time": str(ds.center_time),
            "format": str(ds.format),
            "local_path": str(ds.local_path),
            "measurements": str(ds.measurements),
            
            
        })
    df = pd.DataFrame(d)
    return gpd.GeoDataFrame(df, geometry='geom', crs={'init': ds_lst[0].crs.crs_str})
