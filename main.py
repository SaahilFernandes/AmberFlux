from fastapi import FastAPI, UploadFile, File
from video_utils import extract_frames
from feature_utils import compute_feature_vector
from qdrant_utils import store_vectors, query_similar_frames

app = FastAPI()


@app.post("/upload_video/")
async def upload_video(file: UploadFile = File(...)):
    video_path = f"temp_{file.filename}"
    with open(video_path, "wb") as f:
        f.write(await file.read())

    frame_paths = extract_frames(video_path, interval=1)
    feature_data = []

    for path in frame_paths:
        vector = compute_feature_vector(path)
        feature_data.append({"path": path, "vector": vector})


    store_vectors(feature_data)
    if feature_data:  # Add these lines
        print("------ SAMPLE VECTOR FOR SEARCH TEST ------")  # Add these lines
        print(feature_data[0]["vector"])  # Add these lines
        print("------ END SAMPLE VECTOR ------")  # Add these lines
    return {"message": f"{len(frame_paths)} frames extracted and stored."}



@app.post("/search_similar/")
async def search_similar(vector: list[float]):
    results = query_similar_frames(vector)
    return results


@app.get("/")
def root():
    return {"message": "FastAPI is running"}

