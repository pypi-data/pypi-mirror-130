from functools import cached_property,wraps
from typing import Any,List, Tuple, Union
from random import randint
from path import Path
import subprocess
import atexit
import httpx
import os

import pkg_resources
import platform

FOLDER = platform.system()
if not FOLDER:
    raise Exception("Unknown OS")

BIN = pkg_resources.resource_filename("pygopus",Path(f"/bin/{FOLDER}/pygobin"))

if platform.system() == "Windows":
    BIN = pkg_resources.resource_filename("pygopus",Path(f"/bin/{FOLDER}/pygobin.exe"))

def check_path(path:str):
    p = Path(path)
    if not p.exists():
        raise Exception(f"{ path } is not exists.Please check carefully") 

def kill_go():
    import psutil
    for p in psutil.process_iter():
        if "pygobin" in p.name():
            proc = psutil.Process(p.pid)
            proc.terminate()

atexit.register(kill_go)

def auto_abort(func):
    @wraps(func)
    def instead(self,*args,**kwd):
        try:
            res = func(self,*args,**kwd)
            return res
        except Exception as e:
            kill_go()
            raise e
        finally:
            ...
    return instead

def create_workbook(path:str):
    import shutil
    tpl = pkg_resources.resource_filename("pygopus",Path("/bin/tpl.xlsx"))
    shutil.copyfile(tpl,Path(path))

class WorkBook:

    def __init__(self,path:str,write_mode="",debug=False) -> None:
        # check file here
        if write_mode != "w+":
            # means user want open
            check_path(path)
        else:
            create_workbook(path)
            print(f"{path} file created.")



        port = randint(45555,55588)
        pygo_bin = Path(BIN)
        mode = os.stat(pygo_bin).st_mode | 0o100
        pygo_bin.chmod(mode)
        cmd = f"{BIN} -path {path} -port {port}".split()
        # p = subprocess.Popen(args=cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        kwd = {}
        if debug:
            ...
        else:
            kwd = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = subprocess.Popen(args=cmd,**kwd)
        self._pid = p.pid
        self._api  = f"http://127.0.0.1:{port}"
        self.proc_meta = (self._pid,self._api)

        while True:
            try:
                httpx.get(f"{self._api}/hello")
                break
            except httpx.ConnectError: 
                if debug:
                    print("Waiting for starting server.")




    def __len__(self):
        return len(self.sheets())

    @classmethod
    def create(cls):
        ...

    @auto_abort
    def get_sheet(self,name:str):
        return Sheet(name,self.proc_meta)

    @auto_abort
    def add(self,name:str):
        params = dict(sheet_name=name)
        res = httpx.get(self._api+"/add_sheet",params=params)
        return "ok"


    @auto_abort
    def delete(self,name:str):
        params = dict(sheet_name=name)
        res = httpx.get(self._api+"/delete_sheet ",params=params)
        return "ok"

    @auto_abort
    def sheets(self):
        res = httpx.get(self._api + "/sheets").json()
        return [Sheet(p[1],self.proc_meta) for p in res.items()]

    @auto_abort
    def save(self):
        res = httpx.get(self._api + "/save")
        if res.status_code == 200:
            return "ok"
        else:
            raise Exception(f"Can't save WorkBook for some reason")

    @auto_abort
    def save_as(self,path:str):
        params = dict(path=path)
        res = httpx.get(self._api + "/save_as",params=params)
        if res.status_code == 200:
            return "ok"
        else:
            raise Exception(f"Can't save WorkBook for some reason")


    def close(self):
        import psutil
        ps = psutil.Process(self._pid)
        ps.terminate()



class Sheet:

    def __init__(self,name:str,proc_meta:Tuple) -> None:
        self.proc_meta = proc_meta
        self.name = name
    
    def __setitem__(self,k,v):
        return self.set(k,v)

    def __getitem__(self,k):
        return self.select(k)

    def __repr__(self):
        return f"<pygopus.Sheet name='{self.name}'>"

    @property
    @auto_abort
    def rows(self):
        res = httpx.get(f"{self.proc_meta[1]}/rows?sheet_name={self.name}")
        return res.json()

    @auto_abort
    def select(self,axis:str):
        axis = axis.upper()
        params = dict(
            sheet_name=self.name,
            cell_axis=axis 
        )
        res = httpx.get(f"{self.proc_meta[1]}/cell",params=params)
        return res.json()

    @auto_abort
    def set(self,axis:str,val:Any):
        axis = axis.upper()
        params = dict(
            sheet_name=self.name,
            cell_axis=axis,
            val=val
        )
        res = httpx.get(f"{self.proc_meta[1]}/set_cell",params=params)
        # print(res.url)
        if res.status_code == 200:
            return 'ok'
        else:
            raise Exception(f"Can't set {axis}'s value for some reason")

    @auto_abort
    def write_rows(self,data:List,start_at="A"):
        d = {f"{start_at}{i+1}":row for i,row in enumerate(data)}
        param = {
            "sheetname":self.name,
            "rows":d
        }
        res = httpx.post(f"{self.proc_meta[1]}/write_rows",json=param,timeout=None)

        if res.status_code == 200:
            return 'ok'
        else:
            raise Exception(f"Wrong")

    @auto_abort
    def range(self):
        ...

    # Just make it simple at the very begining. 
    # then try some string trick like val > 100 
    @auto_abort
    def find(self,val:str):
        ...


    def option(self):
        ...



    @cached_property
    def cols(self):
        ...


