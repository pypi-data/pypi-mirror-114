import subprocess
import pandas as pd



def write_pickle(dataframe, name):
    """
    Save a pickle file to HDFS from your JHUB

    Parameters:

    dataframe: Pandas dataframe which needs to be saved as a pickle
    name: Name of the pickle file you want to save (str). 
          Give the name if you want to save in the same directory as notebook or provide a full path

    Return:

    None
    """

    hdfs_path = "hdfs://COPPROD/commercial_workbench/cws/z_abv_cws_cdls_patient_risk_scoring/psee_analytics_jhub/"
    local_record_path = subprocess.check_output(["pwd"]).decode("utf-8")[:15]
    file = open(local_record_path+"files_in_hdfs.txt","a")
    
    if "/" in name:
        local_name = name.split("/")[-1]
        file_path = "/".join(name.split("/")[:-1])+"/"
        
        command = ["hdfs", "dfs", "-mkdir", "-p", hdfs_path+file_path]
        make_dir = subprocess.check_output(command)
        
        dataframe.to_pickle(local_name)
        try:
            command = ["hdfs", "dfs", "-copyFromLocal", local_name, hdfs_path+file_path]
            subprocess.check_output(command)
            file.write(file_path+local_name+"\n")
            file.close()
        
        except:
            command = ["hdfs", "dfs", "-rm", "-r", "-f", hdfs_path+file_path+local_name]
            subprocess.check_output(command)
            command = ["hdfs", "dfs", "-copyFromLocal", local_name, hdfs_path+file_path]
            subprocess.check_output(command)
        
        command = ["rm", "-rf", local_name]
        subprocess.check_output(command)
        
    else:
        local_path = subprocess.check_output(["pwd"]).decode("utf-8")[7:-1]+"/"
        
        command = ["hdfs", "dfs", "-mkdir", "-p", hdfs_path+local_path]
        make_dir = subprocess.check_output(command)
        
        dataframe.to_pickle(name)
        try:
            command = ["hdfs", "dfs", "-copyFromLocal", name, hdfs_path+local_path]
            subprocess.check_output(command)
            file.write(local_path+name+"\n")
            file.close()

        except:
            command = ["hdfs", "dfs", "-rm", "-r", "-f", hdfs_path+local_path+name]
            subprocess.check_output(command)
            command = ["hdfs", "dfs", "-copyFromLocal", name, hdfs_path+local_path]
            subprocess.check_output(command)

        command = ["rm", "-rf", name]
        subprocess.check_output(command)
    

def read_pickle(name):
    """
    Read a pickle file from HDFS to your JHUB

    Parameters:

    name: Name of the pickle file you want to read (str). 
          Give the name if you have the file in the same directory as notebook or provide a full path

    Return:
    dataframe: Returns a pandas dataframe
    """

    hdfs_path = "hdfs://COPPROD/commercial_workbench/cws/z_abv_cws_cdls_patient_risk_scoring/psee_analytics_jhub/"
    
    local_path = subprocess.check_output(["pwd"]).decode("utf-8")[:-1]+"/"
    
    if "/" in name:       
        command = ["hdfs", "dfs", "-copyToLocal", hdfs_path+name, local_path]
        subprocess.check_output(command)
        local_name = name.split("/")[-1]
        get_df = pd.read_pickle(local_name)

        command = ["rm", "-rf", local_name]
        subprocess.check_output(command)
    
    
    else:
        command = ["hdfs", "dfs", "-copyToLocal", hdfs_path+local_path[7:]+name, local_path]
        subprocess.check_output(command)
        
        get_df = pd.read_pickle(name)

        command = ["rm", "-rf", name]
        subprocess.check_output(command)
        
    return get_df

def write_excel(dataframe, name):
    """
    Save an excel file to HDFS from your JHUB

    Parameters:

    dataframe: Pandas dataframe which needs to be saved as an excel
    name: Name of the excel file you want to save (str). 
          Give the name if you want to save in the same directory as notebook or provide a full path

    Return:

    None
    """

    hdfs_path = "hdfs://COPPROD/commercial_workbench/cws/z_abv_cws_cdls_patient_risk_scoring/psee_analytics_jhub/"
    local_record_path = subprocess.check_output(["pwd"]).decode("utf-8")[:15]
    file = open(local_record_path+"files_in_hdfs.txt","a")
    
    if "/" in name:
        local_name = name.split("/")[-1]
        file_path = "/".join(name.split("/")[:-1])+"/"
        
        command = ["hdfs", "dfs", "-mkdir", "-p", hdfs_path+file_path]
        make_dir = subprocess.check_output(command)
        
        dataframe.to_excel(local_name)
        try:
            command = ["hdfs", "dfs", "-copyFromLocal", local_name, hdfs_path+file_path]
            subprocess.check_output(command)
            file.write(file_path+local_name+"\n")
            file.close()
        
        except:
            command = ["hdfs", "dfs", "-rm", "-r", "-f", hdfs_path+file_path+local_name]
            subprocess.check_output(command)
            command = ["hdfs", "dfs", "-copyFromLocal", local_name, hdfs_path+file_path]
            subprocess.check_output(command)
        
        command = ["rm", "-rf", local_name]
        subprocess.check_output(command)
        
    else:
        local_path = subprocess.check_output(["pwd"]).decode("utf-8")[7:-1]+"/"
        
        command = ["hdfs", "dfs", "-mkdir", "-p", hdfs_path+local_path]
        make_dir = subprocess.check_output(command)
        
        dataframe.to_excel(name)
        try:
            command = ["hdfs", "dfs", "-copyFromLocal", name, hdfs_path+local_path]
            subprocess.check_output(command)
            file.write(local_path+name+"\n")
            file.close()
        
        except:
            command = ["hdfs", "dfs", "-rm", "-r", "-f", hdfs_path+local_path+name]
            subprocess.check_output(command)
            command = ["hdfs", "dfs", "-copyFromLocal", name, hdfs_path+local_path]
            subprocess.check_output(command)

        command = ["rm", "-rf", name]
        subprocess.check_output(command)
    

def read_excel(name):
    """
    Read an excel file from HDFS to your JHUB

    Parameters:

    name: Name of the excel file you want to read (str). 
          Give the name if you have the file in the same directory as notebook or provide a full path

    Return:
    dataframe: Returns a pandas dataframe
    """

    hdfs_path = "hdfs://COPPROD/commercial_workbench/cws/z_abv_cws_cdls_patient_risk_scoring/psee_analytics_jhub/"
    
    local_path = subprocess.check_output(["pwd"]).decode("utf-8")[:-1]+"/"
    
    if "/" in name:       
        command = ["hdfs", "dfs", "-copyToLocal", hdfs_path+name, local_path]
        subprocess.check_output(command)
        local_name = name.split("/")[-1]
        get_df = pd.read_excel(local_name)

        command = ["rm", "-rf", local_name]
        subprocess.check_output(command)
    
    
    else:
        command = ["hdfs", "dfs", "-copyToLocal", hdfs_path+local_path[7:]+name, local_path]
        subprocess.check_output(command)
        
        get_df = pd.read_excel(name)

        command = ["rm", "-rf", name]
        subprocess.check_output(command)
        
    return get_df


def write_csv(dataframe, name):
    """
    Save an csv file to HDFS from your JHUB

    Parameters:

    dataframe: Pandas dataframe which needs to be saved as a csv
    name: Name of the csv file you want to save (str). 
          Give the name if you want to save in the same directory as notebook or provide a full path

    Return:

    None
    """

    hdfs_path = "hdfs://COPPROD/commercial_workbench/cws/z_abv_cws_cdls_patient_risk_scoring/psee_analytics_jhub/"
    local_record_path = subprocess.check_output(["pwd"]).decode("utf-8")[:15]
    file = open(local_record_path+"files_in_hdfs.txt","a")
    
    if "/" in name:
        local_name = name.split("/")[-1]
        file_path = "/".join(name.split("/")[:-1])+"/"
        
        command = ["hdfs", "dfs", "-mkdir", "-p", hdfs_path+file_path]
        make_dir = subprocess.check_output(command)
        
        dataframe.to_csv(local_name)
        try:
            command = ["hdfs", "dfs", "-copyFromLocal", local_name, hdfs_path+file_path]
            subprocess.check_output(command)
            file.write(file_path+local_name+"\n")
            file.close()
        
        except:
            command = ["hdfs", "dfs", "-rm", "-r", "-f", hdfs_path+file_path+local_name]
            subprocess.check_output(command)
            command = ["hdfs", "dfs", "-copyFromLocal", local_name, hdfs_path+file_path]
            subprocess.check_output(command)

            
        command = ["rm", "-rf", local_name]
        subprocess.check_output(command)
        
    else:
        local_path = subprocess.check_output(["pwd"]).decode("utf-8")[7:-1]+"/"
        
        command = ["hdfs", "dfs", "-mkdir", "-p", hdfs_path+local_path]
        make_dir = subprocess.check_output(command)
        
        dataframe.to_csv(name)
        try:
            command = ["hdfs", "dfs", "-copyFromLocal", name, hdfs_path+local_path]
            subprocess.check_output(command)
            file.write(local_path+name+"\n")
            file.close()       
        except:
            command = ["hdfs", "dfs", "-rm", "-r", "-f", hdfs_path+local_path+name]
            subprocess.check_output(command)
            command = ["hdfs", "dfs", "-copyFromLocal", name, hdfs_path+local_path]
            subprocess.check_output(command)



        command = ["rm", "-rf", name]
        subprocess.check_output(command)
    

def read_csv(name):
    """
    Read a csv file from HDFS to your JHUB

    Parameters:

    name: Name of the csv file you want to read (str). 
          Give the name if you have the file in the same directory as notebook or provide a full path

    Return:
    dataframe: Returns a pandas dataframe
    """

    hdfs_path = "hdfs://COPPROD/commercial_workbench/cws/z_abv_cws_cdls_patient_risk_scoring/psee_analytics_jhub/"
    
    local_path = subprocess.check_output(["pwd"]).decode("utf-8")[:-1]+"/"
    
    if "/" in name:       
        command = ["hdfs", "dfs", "-copyToLocal", hdfs_path+name, local_path]
        subprocess.check_output(command)
        local_name = name.split("/")[-1]
        get_df = pd.read_csv(local_name)

        command = ["rm", "-rf", local_name]
        subprocess.check_output(command)
    
    
    else:
        command = ["hdfs", "dfs", "-copyToLocal", hdfs_path+local_path[7:]+name, local_path]
        subprocess.check_output(command)
        
        get_df = pd.read_csv(name)

        command = ["rm", "-rf", name]
        subprocess.check_output(command)
        
    return get_df

