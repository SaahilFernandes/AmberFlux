from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

client = QdrantClient(":memory:")  # Use real host:port for production

collection_name = "video_frames"

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=512, distance=Distance.COSINE)
)

def store_vectors(feature_data):
    points = []
    for item in feature_data:
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=item["vector"],
                payload={"image_path": item["path"]}
            )
        )
    client.upsert(collection_name=collection_name, points=points)

def query_similar_frames(vector):
    search_result = client.search(
        collection_name=collection_name,
        query_vector=vector,
        limit=5
    )
    return [{"score": hit.score, "image_path": hit.payload["image_path"]} for hit in search_result]
