from fastapi import FastAPI, Request, status, HTTPException, Header, Depends, APIRouter
from typing import List, Optional
from pydantic import BaseModel
import asyncio
from asyncio import Queue



class inputPayload(BaseModel):
    company: str
    class Config:
        orm_mode = False

class outputPayload(BaseModel):
     returnResponse: str
     class Config:
          orm_mode = False

class Register:
     router = APIRouter()
     def __init__(self, companies):
          self.companies = companies

     @router.on_event("startup")
     def on_startup(self):
          print("Started APP")

     @router.on_event("shutdown")
     def on_shutdown(self):
          print("Stopped app")

     @router.get("/home")
     async def healthcheck(self):
          return "OK"

     @router.get("/home/failure")
     async def healthcheckFailure(self):
          return HTTPException(status_code=403, detail="")

     @router.post("/home/register")
     async def registerCompany(payload: inputPayload):
          companies.append(payload.company)
          return "Succesfully added"

     @router.get("/home/verify/{company}")
     async def getCOmpany(self, company: str):
          if company.lower() in (company.lower() for company in companies):
               return "Valid one"
          return HTTPException(status_code=400, detail="Not valid")


     @router.get("/home/verify")
     async def getCOmpanyAsQuery(self, company: str):
          if company.lower() in (company.lower() for company in companies):
               return "Valid one"
          return HTTPException(status_code=400, detail="Not valid")


     async def common_parameters(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
          return {"q": q, "skip": skip, "limit": limit}


     @router.get("/items/")
     async def read_items(self, commons: dict = Depends(common_parameters)):
          return commons