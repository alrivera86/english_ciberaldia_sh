import React, { useEffect, useState } from "react";
import axios from "axios";

const BASE_URL = "http://82.25.74.175:8000"; // 🔥 Cambia por la URL de tu backend

const VideoDashboard = () => {
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);

  useEffect(() => {
    fetchVideos();
  }, []);

  const fetchVideos = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/videos`);
      setVideos(response.data.videos);
    } catch (error) {
      console.error("Error al obtener los videos", error);
    }
  };

  const handleDownload = (videoName) => {
    window.open(`${BASE_URL}/download/${videoName}`, "_blank");
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-5">
      <h1 className="text-3xl font-bold mb-6">📽️ Videos Generados</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-5xl">
        {videos.length === 0 ? (
          <p className="text-gray-400">No hay videos disponibles.</p>
        ) : (
          videos.map((video, index) => (
            <div key={index} className="bg-gray-800 p-4 rounded-lg shadow-lg flex flex-col items-center">
              <p className="text-lg font-semibold">{video}</p>
              
              {/* Botón para ver video */}
              <button
                className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-3"
                onClick={() => setSelectedVideo(video)}
              >
                🎬 Ver Video
              </button>

              {/* Botón para descargar */}
              <button
                className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded mt-2"
                onClick={() => handleDownload(video)}
              >
                ⬇️ Descargar
              </button>
            </div>
          ))
        )}
      </div>

      {/* Reproductor de video */}
      {selectedVideo && (
        <div className="mt-6 w-full max-w-3xl">
          <h2 className="text-2xl font-semibold mb-3">🎥 Reproduciendo: {selectedVideo}</h2>
          <video controls className="w-full rounded-lg shadow-lg">
            <source src={`${BASE_URL}/videos/${selectedVideo}`} type="video/mp4" />
            Tu navegador no soporta la reproducción de videos.
          </video>
          <button
            className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded mt-3"
            onClick={() => setSelectedVideo(null)}
          >
            ❌ Cerrar Video
          </button>
        </div>
      )}
    </div>
  );
};

export default VideoDashboard;

