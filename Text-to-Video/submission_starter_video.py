from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import boto3
import logging
import random
import time 
from typing import List, Optional, TypedDict
logging.basicConfig( 
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

class RetrieverResponse(TypedDict):
    status: str
    error: Optional[str]
    retrieved_docs: List[str]
def retriever(question) -> RetrieverResponse: 
        """
        To be filled by the Partipant. Ideally we expect the participant to retrive top -k documents with each document of String datatype
        as an element of the list.
        Returns a dictionary 
            {
                "status" : "error" OR "success
                "error" : "No documents retrieved" OR None
                "retrieved_docs"  : [] or retrieved document
            }
        """
        return {
            "status" : "success",
            "error" : None,
            "retrieved_docs" : ["document1", "document2", "document3"]
        }

class GeneratorResponse(TypedDict):
     status : str
     error : Optional[str]
     s3_BUCKET_NAME : str
     region : str
     Storage_Uri : Optional[str]
def generator(retrieved_docs, question) -> GeneratorResponse:
        """
        To be filled by the Partipant. We expect the particpants to generate a video and store it in an s3 bucket.
        Returns a dictionary
            {
                "status" : "error" OR "success
                "error" : Appropraite error message for any intermediate steps  OR None
                "s3_BUCKET_NAME" :  The s3 bucket assigned to the team, this will be used an integrity check in the main backend
                "Storage_Uri" : The storage Uri of the generated video in the assigned s3 bucket or None
            }
        """
        return {
            "status" : "success",
            "error" : None,
            "s3_BUCKET_NAME" : "ragarena-videos",
            "region" : "us-east-1",
            "Storage_Uri" : "https://ragarena-videos.s3.amazonaws.com/video.mp4"
        }

@app.post('/generate-video') 
# DO NOT CHANGE THIS FUNCTION!!!
async def generate_video(request: Request):
    data = await request.json()
    if not data:
        return {
            "status" : "error",
            "error" : 'No input data provided',
            "s3_BUCKET_NAME" : None,
            "retrieved_docs" : [],
            "region" : None,
            "Storage_Uri" : None   
        }

    question = data.get("question")
    if question is None:
        return {
            "status" : "error",
            "error" : 'Question cannot be parsed from request',
            "s3_BUCKET_NAME" : None,
            "retrieved_docs" : [],
            "region" : None,
            "Storage_Uri" : None,
            
        }
    retriever_response = retriever(question)
    if retriever_response["status"] == "error":
        return {
            "status" : "error",
            "error" : retriever_response["error"],
            "s3_BUCKET_NAME" : None,
            "retrieved_docs" : [],
            "region" : None,
            "Storage_Uri" : None
        }
    elif retriever_response["status"] == "success":
        retrieved_docs = retriever_response["retrieved_docs"]
        generator_response = generator(retrieved_docs=retrieved_docs,question=question)
        logger.debug(f"generator response is {generator_response}")
        if generator_response["status"] == "error":
                    return {
        "status" : "error",
        "error" : generator_response["error"],
        "s3_BUCKET_NAME" : generator_response["s3_BUCKET_NAME"],
        "retrieved_docs" : retrieved_docs,
        "region" : generator_response["region"],
        "Storage_Uri" : None
    }
        elif generator_response["status"] == "success":
                                    return {
        "status" : "success",
        "error" : generator_response["error"],
        "s3_BUCKET_NAME" : generator_response["s3_BUCKET_NAME"],
        "retrieved_docs" : retrieved_docs,
          "region" : generator_response["region"],
        "Storage_Uri" : generator_response["Storage_Uri"]
    }


if __name__ == "__main__":
    import uvicorn
    # To run with uvicorn: uvicorn video_baseline:app --host 0.0.0.0 --port 6001 --reload
    uvicorn.run("video_second:app", host='0.0.0.0', port=6001, reload=True)