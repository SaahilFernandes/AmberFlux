## Demo Video
[![Watch our demo video](https://img.youtube.com/vi/1_LsR3KNdkY/mqdefault.jpg)](https://youtu.be/1_LsR3KNdkY)

## Prerequisites

*   Python 3.8+
*   pip (Python package installer)
*   FFmpeg (Recommended for broader video format support by OpenCV. Installation varies by OS.)

## Setup and Installation

1.  **Clone the repository (if applicable) or create the project directory and files.**

2.  **Navigate to the project directory:**
    ```bash
    cd /path/to/video_similarity_app
    ```

3.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    source venv/Scripts/activate
    # On macOS/Linux
    source venv/bin/activate
    ```

4.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    The `requirements.txt` file should contain:
    ```
    fastapi
    uvicorn[standard]
    opencv-python
    numpy
    qdrant-client
    python-multipart
    ```

## Running the Application

1.  Ensure your virtual environment is activated.
2.  Start the FastAPI application using Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```
    The application will typically be available at `http://127.0.0.1:8000`. The `--reload` flag enables auto-reloading when code changes are made (useful for development).

## API Endpoints

The API documentation (Swagger UI) is automatically generated and available at `http://127.0.0.1:8000/docs` when the application is running. You can use this interface to test the endpoints.

### 1. Root

*   **GET `/`**
*   **Description:** A simple health check endpoint.
*   **Response (200 OK):**
    ```json
    {
      "message": "FastAPI is running"
    }
    ```

### 2. Upload Video

*   **POST `/upload_video/`**
*   **Description:** Uploads a video file, extracts frames, computes feature vectors, and stores them.
*   **Request:**
    *   `Content-Type: multipart/form-data`
    *   `file`: The video file to upload (e.g., an MP4 file).
*   **Response (200 OK):**
    ```json
    {
      "message": "X frames extracted and stored."
    }
    ```
    (Where X is the number of frames processed)
*   **Side Effects:**
    *   Saves extracted frames as JPG images in the `extracted_frames/` directory.
    *   Saves the uploaded video temporarily as `temp_<filename>`.
    *   Populates the in-memory Qdrant database with feature vectors.

### 3. Search Similar Frames

*   **POST `/search_similar/`**
*   **Description:** Searches for frames in the database that are similar to the provided query feature vector.
*   **Request Body (JSON):**
    A JSON array representing the 512-dimensional feature vector.
    ```json
    {
      "vector": [0.00123, 0.0, ..., 0.00543] // 512 float values
    }
    ```
*   **Response (200 OK):**
    A JSON array of the top 5 most similar frames, including their similarity score and image path.
    ```json
    [
      {
        "score": 0.9999,
        "image_path": "extracted_frames/frame_X.jpg"
      },
      {
        "score": 0.8756,
        "image_path": "extracted_frames/frame_Y.jpg"
      }
      // ... up to 5 results
    ]
    ```

## How to Test

1.  **Start the application:** `uvicorn main:app --reload`
2.  **Open the API docs:** Go to `http://127.0.0.1:8000/docs` in your browser.

3.  **Upload a video:**
    *   Expand the `POST /upload_video/` endpoint.
    *   Click "Try it out".
    *   Click "Choose File" and select a test video (e.g., `test_video.mp4`).
    *   Click "Execute".
    *   Verify the success response and check the `extracted_frames/` directory.

4.  **Search for similar frames:**
    *   To get a sample vector for testing, you can temporarily modify `main.py` in the `upload_video` function to print or return a vector from `feature_data` (see `Testing Details` section in previous instructions).
    *   Expand the `POST /search_similar/` endpoint.
    *   Click "Try it out".
    *   In the "Request body", paste the 512-element feature vector (ensure it's a valid JSON array of floats, all on one line if copied from a multi-line terminal output).
    *   Click "Execute".
    *   Observe the results, which should list similar frames.

## Notes

*   **In-Memory Qdrant:** The Qdrant database is configured to run in-memory (`QdrantClient(":memory:")`). This means all data (vectors) will be lost when the application stops. For persistent storage, you would need to set up a persistent Qdrant instance (e.g., using Docker or a Qdrant Cloud service) and update the client connection string in `qdrant_utils.py`.
*   **Feature Vector:** The feature vector is a 512-dimensional color histogram (8 bins for each of the B, G, R channels, i.e., 8x8x8).
*   **Error Handling:** The current implementation has basic error handling. For production, more robust error handling would be necessary.
*   **Temporary Video File:** The uploaded video is saved temporarily as `temp_<filename>` in the project root. This file is not automatically cleaned up in the current version.

## Potential Future Enhancements

*   Add more sophisticated feature extraction methods (e.g., SIFT, SURF, CNN-based features).
*   Implement cleanup for temporary video files.
*   Add authentication and authorization.
*   Support for persistent Qdrant storage.
*   More comprehensive error handling and logging.
*   Option to specify frame extraction interval via API.
*   Return actual image data or URLs to images in the search results.
