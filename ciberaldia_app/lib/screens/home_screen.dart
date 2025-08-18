import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:ciberaldia_app/screens/video_list_screen.dart'; // ✅ Importa VideoListScreen correctamente
import 'package:ciberaldia_app/screens/video_player_screen.dart'; // ✅ Asegura que el reproductor de video esté disponible
import 'package:ciberaldia_app/screens/post_screen.dart'; // ✅ Importa la nueva pantalla para visualizar el post

const String baseUrl = "http://82.25.74.175:8000"; // 🔥 Cambia esto según tu servidor

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;
  List<String> videoFiles = [];
  bool isLoading = true;
  String errorMessage = "";
  String scriptOutput = ""; // ✅ Variable para guardar la salida del script
  bool isRunning = false; // ✅ Controla si el script está en ejecución

  @override
  void initState() {
    super.initState();
    _fetchVideos();
  }

  Future<void> _fetchVideos() async {
    try {
      final response = await http.get(Uri.parse("$baseUrl/videos"));
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        setState(() {
          videoFiles = List<String>.from(data["videos"]);
          isLoading = false;
          errorMessage = "";
        });
      } else {
        setState(() {
          errorMessage = "Error al obtener videos (${response.statusCode})";
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = "Error de conexión: $e";
        isLoading = false;
      });
    }
  }

  // ✅ Función para ejecutar el script y mostrar la salida en tiempo real
  Future<void> _executeScript() async {
    setState(() {
      scriptOutput = "Ejecutando script...\n";
      isRunning = true;
    });

    try {
      final response = await http.post(Uri.parse("$baseUrl/run"));
      if (response.statusCode == 200) {
        setState(() {
          scriptOutput += response.body;
          isRunning = false;
        });
      } else {
        setState(() {
          scriptOutput += "Error: No se pudo ejecutar el script.";
          isRunning = false;
        });
      }
    } catch (e) {
      setState(() {
        scriptOutput += "Error de conexión: $e";
        isRunning = false;
      });
    }
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    final List<Widget> _screens = [
      Center(
          child: Text('Bienvenido a CiberAlDía',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold))),
      Column(
        children: [
          ElevatedButton(
            onPressed: isRunning ? null : _executeScript, // ✅ Deshabilita el botón si está en ejecución
            child: Text(isRunning ? 'Ejecutando...' : 'Ejecutar Script'),
          ),
          Expanded(
            child: SingleChildScrollView(
              child: Container(
                padding: EdgeInsets.all(10),
                color: Colors.black,
                child: Text(
                  scriptOutput,
                  style: TextStyle(color: Colors.green, fontFamily: "monospace"),
                ),
              ),
            ),
          ),
        ],
      ),
      VideoListScreen( // ✅ Pantalla para visualizar los videos con botones de descarga
        videos: videoFiles,
        isLoading: isLoading,
        errorMessage: errorMessage,
      ),
      PostScreen(), // ✅ Se mantiene la pantalla de Post correctamente
    ];

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: Text('CiberAlDía'),
          backgroundColor: Colors.blueAccent,
        ),
        body: _screens[_selectedIndex], // ✅ Se usa la lista de pantallas correctamente
        bottomNavigationBar: BottomNavigationBar(
          items: const <BottomNavigationBarItem>[
            BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Inicio'),
            BottomNavigationBarItem(icon: Icon(Icons.play_arrow), label: 'Ejecutar'),
            BottomNavigationBarItem(icon: Icon(Icons.video_library), label: 'Visualizar Videos'),
            BottomNavigationBarItem(icon: Icon(Icons.article), label: 'Visualizar Post'),
          ],
          currentIndex: _selectedIndex,
          selectedItemColor: Colors.blue,
          unselectedItemColor: Colors.grey,
          onTap: _onItemTapped,
        ),
      ),
    );
  }
}
