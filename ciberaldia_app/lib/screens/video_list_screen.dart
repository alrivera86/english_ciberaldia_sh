import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'dart:io';
import 'dart:convert';

import 'video_player_screen.dart'; // Importa la pantalla del reproductor de video

const String baseUrl = "http://82.25.74.175:8000"; // 🔥 Cambia esto según tu servidor

class VideoListScreen extends StatelessWidget {
  final List<String> videos;
  final bool isLoading;
  final String errorMessage;

  VideoListScreen({
    required this.videos,
    required this.isLoading,
    required this.errorMessage,
  });

  // 📥 Función para descargar el video
  Future<void> _downloadVideo(BuildContext context, String videoName) async {
    try {
      final response = await http.get(Uri.parse("$baseUrl/videos/$videoName"));

      if (response.statusCode == 200) {
        final directory = await getApplicationDocumentsDirectory();
        final filePath = '${directory.path}/$videoName';
        final file = File(filePath);
        await file.writeAsBytes(response.bodyBytes);

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('✅ Video descargado: $videoName'),
          ),
        );
      } else {
        throw Exception('❌ Error al descargar el video (${response.statusCode})');
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('⚠️ Error de conexión: $e'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return Center(child: CircularProgressIndicator());
    } else if (errorMessage.isNotEmpty) {
      return Center(child: Text(errorMessage, style: TextStyle(color: Colors.red)));
    } else if (videos.isEmpty) {
      return Center(child: Text("No hay videos disponibles"));
    }

    return ListView.builder(
      itemCount: videos.length,
      itemBuilder: (context, index) {
        return ListTile(
          title: Text(videos[index]),
          trailing: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              IconButton(
                icon: Icon(Icons.play_arrow, color: Colors.blue),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => VideoPlayerScreen(videoUrl: "$baseUrl/videos/${videos[index]}"),
                    ),
                  );
                },
              ),
              IconButton(
                icon: Icon(Icons.download, color: Colors.green),
                onPressed: () => _downloadVideo(context, videos[index]),
              ),
            ],
          ),
        );
      },
    );
  }
}
