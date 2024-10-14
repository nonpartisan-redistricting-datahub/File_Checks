import geopandas as gp
import pandas as pd
import os
import numpy as np

def make_vf_points(vf):
    vf['lat'] = vf['lat'].astype(float)
    vf['lon'] = vf['lon'].astype(float)
    points = gp.GeoDataFrame(vf,geometry = gp.points_from_xy(vf.lon, vf.lat, crs='EPSG:4269'))
    assert(len(vf)==len(points))
    return points

        
def run_vf_checks(st, election_path):
    if not os.path.exists(st):
        os.mkdir(st)

    holder = pd.read_csv('./raw-from-source/{}_individual_file000.gz'.format(st), compression='gzip')
    holder = holder[~holder["precinct"].isna()]
    holder = holder[~holder["co_fips"].isna()]
    holder["UNIQUE_ID"] = holder["co_fips"].astype(str).str.zfill(3)+"-:-"+holder["precinct"]


    shps = gp.read_file(election_path)
    shps["COUNTYFP"] = shps["COUNTYFP"].astype(str).str.zfill(3)
    shps["UNIQUE_ID"] = shps["COUNTYFP"]+shps["VTDST"]

    shps = shps.to_crs(4269)
    



    for county in list(holder["co_fips"].unique()):
        if not os.path.exists("./{}/".format(st)+str(county).zfill(3)):
            os.mkdir("./{}/".format(st)+str(county).zfill(3))       

            filtered_vf = holder[holder["co_fips"]==county]

            filtered_vf = make_vf_points(filtered_vf)
            filtered_shps = shps[shps["COUNTYFP"]==str(county).zfill(3)]

            holder_county = gp.sjoin(filtered_shps, filtered_vf, how = "right", lsuffix='x', rsuffix='y')
            county = str(county).zfill(3)

            for prec in list(filtered_shps["UNIQUE_ID"].unique()):
                if not os.path.exists("./{}/".format(st)+county.replace(" ","_")+"/"+prec.replace(" ","_").replace("/","_")+".png"):
                    ax = filtered_shps[filtered_shps["UNIQUE_ID"]==prec].boundary.plot(color = "red")
                    x_diff = filtered_shps[filtered_shps["UNIQUE_ID"]==prec].total_bounds[2] - filtered_shps[filtered_shps["UNIQUE_ID"]==prec].total_bounds[0]
                    y_diff = filtered_shps[filtered_shps["UNIQUE_ID"]==prec].total_bounds[3] - filtered_shps[filtered_shps["UNIQUE_ID"]==prec].total_bounds[1]
                    xlim = ([filtered_shps[filtered_shps["UNIQUE_ID"]==prec].total_bounds[0]-x_diff,  filtered_shps[filtered_shps["UNIQUE_ID"]==prec].total_bounds[2]+x_diff])
                    ylim = ([filtered_shps[filtered_shps["UNIQUE_ID"]==prec].total_bounds[1]-y_diff,  filtered_shps[filtered_shps["UNIQUE_ID"]==prec].total_bounds[3]+y_diff])
                    other_precs = list(holder_county[holder_county["UNIQUE_ID_x"]==prec]["UNIQUE_ID_y"].unique())
                    
                    try:
                        if len(other_precs) > 0:


        #                     print(xlim)
        #                     print([filtered_shps[filtered_shps["UNIQUE_ID"]==prec].total_bounds[0]*1,  filtered_shps[filtered_shps["UNIQUE_ID"]==prec].total_bounds[2]*1])
        #                     print(" ")



                            holder_county[holder_county["UNIQUE_ID_y"].isin(other_precs)].plot(ax = ax, column = "UNIQUE_ID_y", legend = True, s = 3, legend_kwds = {"loc":(1,0)}, cmap = "tab20")
                    except IndexError as i:
                        print("INDEX ERROR***********")
                        print(other_precs)
                        print(i)

                    ax.set_xlim(xlim)
                    ax.set_ylim(ylim)  
                    ax.set_title(prec)

                    ax.figure.savefig("./{}/".format(st)+county.replace(" ","_")+"/"+prec.replace(" ","_").replace("/","_")+".png", dpi = 350, bbox_inches = "tight")

            print(county, " complete")
        


#run_vf_checks("MT","./raw-from-source/mt_gen_2022_prec/mt_22_no_splits_prec/mt_22_no_splits_prec.shp")
#run_vf_checks("NC","/Users/peterhorton/Documents/RDH/vf_checks/raw-from-source/nc_2022_gen_prec/nc_gen_22_st_prec.shp")
#run_vf_checks("OH","/Users/peterhorton/Documents/RDH/vf_checks/raw-from-source/oh_gen_2022_prec/oh_2022_gen_prec_no_splits.shp")
#run_vf_checks("MS","/Users/peterhorton/Documents/RDH/vf_checks/raw-from-source/ms_gen_22_prec/ms_gen_22_prec.shp")
#run_vf_checks("NV","/Users/peterhorton/Documents/RDH/pber_local/NV_2022/nv_gen_22_precs/nv_gen_22_precs.shp")
run_vf_checks("KS","/Users/peterhorton/Downloads/Kansas_2022_General-main/ks_2022g (1)/ks_2022g.shp")

