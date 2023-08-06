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
     companies = []
     def __init__(self, companies):
          global companies
          companies = companies

     @staticmethod
     @router.on_event("startup")
     def on_startup():
          print("Started APP")

     @staticmethod
     @router.on_event("shutdown")
     def on_shutdown():
          print("Stopped app")

     @staticmethod
     @router.get("/home")
     async def healthcheck():
          return "OK"

     @staticmethod
     @router.get("/home/failure")
     async def healthcheckFailure():
          return HTTPException(status_code=403, detail="")

     @staticmethod
     @router.post("/home/register")
     async def registerCompany(payload: inputPayload):
          companies.append(payload.company)
          return "Succesfully added"

     @staticmethod
     @router.get("/home/verify/{company}")
     async def getCOmpany(company: str):
          if company.lower() in (company.lower() for company in companies):
               return "Valid one"
          return HTTPException(status_code=400, detail="Not valid")

     @staticmethod
     @router.get("/home/verify")
     async def getCOmpanyAsQuery(company: str):
          if company.lower() in (company.lower() for company in companies):
               return "Valid one"
          return HTTPException(status_code=400, detail="Not valid")

     @staticmethod
     async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
          return {"q": q, "skip": skip, "limit": limit}

     @staticmethod
     @router.get("/items/")
     async def read_items(commons: dict = Depends(common_parameters)):
          return commons