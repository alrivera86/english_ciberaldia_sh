import 'package:dio/dio.dart';

class ApiService {
  final Dio _dio = Dio(BaseOptions(baseUrl: "http://tu-servidor.com/api"));

  Future<List<dynamic>> fetchVideos() async {
    try {
      Response response = await _dio.get("/videos");
      return response.data;
    } catch (e) {
      print("Error: $e");
      return [];
    }
  }
}
