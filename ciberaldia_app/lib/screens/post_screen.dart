import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/services.dart'; // Para copiar al portapapeles

const String baseUrl = "http://82.25.74.175:8000"; // Cambia esto si es necesario

class PostScreen extends StatefulWidget {
  @override
  _PostScreenState createState() => _PostScreenState();
}

class _PostScreenState extends State<PostScreen> {
  String postContent = "";
  bool isLoading = true;
  String errorMessage = "";

  @override
  void initState() {
    super.initState();
    _fetchPost();
  }

  Future<void> _fetchPost() async {
    try {
      final response = await http.get(Uri.parse("$baseUrl/post"));

      if (response.statusCode == 200) {
        setState(() {
          postContent = response.body;
          isLoading = false;
          errorMessage = "";
        });
      } else {
        setState(() {
          errorMessage = "Error al obtener el post (${response.statusCode})";
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

  void _copyToClipboard() {
    Clipboard.setData(ClipboardData(text: postContent));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text("✅ Post copiado al portapapeles")),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Post del Día"), backgroundColor: Colors.blueAccent),
      body: isLoading
          ? Center(child: CircularProgressIndicator())
          : errorMessage.isNotEmpty
              ? Center(child: Text(errorMessage, style: TextStyle(color: Colors.red)))
              : Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Expanded(
                        child: SingleChildScrollView(
                          child: SelectableText(
                            postContent,
                            style: TextStyle(fontSize: 16),
                          ),
                        ),
                      ),
                      SizedBox(height: 16),
                      ElevatedButton.icon(
                        onPressed: _copyToClipboard,
                        icon: Icon(Icons.copy),
                        label: Text("Copiar post"),
                      ),
                    ],
                  ),
                ),
    );
  }
}
