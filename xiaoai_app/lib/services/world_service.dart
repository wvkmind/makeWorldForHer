import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/character_state.dart';

class WorldService {
  final String serverUrl;
  WebSocketChannel? _channel;
  bool _connected = false;

  final _stateController = StreamController<CharacterState>.broadcast();
  final _messageController = StreamController<ChatMessage>.broadcast();
  final _pushController = StreamController<String>.broadcast();

  Stream<CharacterState> get stateStream => _stateController.stream;
  Stream<ChatMessage> get messageStream => _messageController.stream;
  Stream<String> get pushStream => _pushController.stream;
  bool get connected => _connected;

  WorldService({required this.serverUrl});

  Future<void> connect() async {
    try {
      final wsUrl = serverUrl.replaceFirst('http', 'ws');
      _channel = WebSocketChannel.connect(Uri.parse('$wsUrl/ws/app'));
      _connected = true;

      _channel!.stream.listen(
        (data) => _handleMessage(jsonDecode(data)),
        onDone: () {
          _connected = false;
          // Auto reconnect after 3s
          Future.delayed(const Duration(seconds: 3), connect);
        },
        onError: (_) {
          _connected = false;
          Future.delayed(const Duration(seconds: 3), connect);
        },
      );
    } catch (e) {
      _connected = false;
      Future.delayed(const Duration(seconds: 3), connect);
    }
  }

  void sendMessage(String text) {
    if (_channel == null) return;
    _channel!.sink.add(jsonEncode({
      'type': 'user_message',
      'message': text,
    }));
  }

  void _handleMessage(Map<String, dynamic> data) {
    final type = data['type'];

    if (type == 'state_update' || type == 'ai_response' || type == 'ai_push') {
      // Update state
      if (data['state'] != null) {
        final state = CharacterState.fromJson(data['state']);
        _stateController.add(state);
      }

      // AI reply text
      if (type == 'ai_response' && data['reply'] != null) {
        _messageController.add(ChatMessage(
          text: data['reply'],
          isUser: false,
        ));
      }

      // AI push message
      if (type == 'ai_push' && data['message'] != null) {
        _pushController.add(data['message']);
      }
    }
  }

  void dispose() {
    _channel?.sink.close();
    _stateController.close();
    _messageController.close();
    _pushController.close();
  }
}
