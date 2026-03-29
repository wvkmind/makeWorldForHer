import 'dart:async';
import 'package:flutter/material.dart';
import '../models/character_state.dart';
import '../services/world_service.dart';
import '../widgets/scene_view.dart';
import '../widgets/chat_panel.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  static const rooms = ['living_room', 'bedroom', 'kitchen', 'bathroom', 'balcony'];
  static const serverUrl = 'http://10.0.2.2:8080'; // TODO: make configurable

  late final WorldService _world;
  var _state = CharacterState();
  final _messages = <ChatMessage>[];
  late final PageController _pageController;
  int _currentPage = 0;
  Timer? _engagedTimer;

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
    _world = WorldService(serverUrl: serverUrl);

    _world.stateStream.listen((newState) {
      setState(() {
        _state = newState;
        // Auto-scroll to the room the character is in
        final roomIdx = rooms.indexOf(newState.scene);
        if (roomIdx >= 0 && roomIdx != _currentPage) {
          _pageController.animateToPage(roomIdx,
              duration: const Duration(milliseconds: 400), curve: Curves.easeInOut);
        }
      });
    });

    _world.messageStream.listen((msg) {
      setState(() => _messages.add(msg));
      _startEngagedTimer();
    });

    _world.pushStream.listen((text) {
      setState(() => _messages.add(ChatMessage(text: text, isUser: false)));
    });

    _world.connect();
  }

  void _onSend(String text) {
    setState(() {
      _messages.add(ChatMessage(text: text, isUser: true));
    });
    _world.sendMessage(text);
    _startEngagedTimer();
  }

  void _startEngagedTimer() {
    _engagedTimer?.cancel();
    _engagedTimer = Timer(const Duration(seconds: 15), () {
      // Tell server to disengage (or just update local state)
      setState(() => _state.engaged = false);
    });
  }

  void _onPageChanged(int page) {
    setState(() => _currentPage = page);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: Stack(
                children: [
                  PageView.builder(
                    controller: _pageController,
                    onPageChanged: _onPageChanged,
                    itemCount: rooms.length,
                    itemBuilder: (_, i) => SceneView(
                      scene: rooms[i],
                      state: _state,
                      isActive: true,
                    ),
                  ),
                  // Page dots + connection indicator
                  Positioned(
                    top: 12,
                    right: 16,
                    child: Row(
                      children: [
                        // Connection dot
                        Container(
                          width: 8, height: 8,
                          margin: const EdgeInsets.only(right: 8),
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: _world.connected ? Colors.greenAccent : Colors.red,
                          ),
                        ),
                        ...List.generate(rooms.length, (i) => Container(
                          width: 8, height: 8,
                          margin: const EdgeInsets.symmetric(horizontal: 3),
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: i == _currentPage ? Colors.pinkAccent : Colors.white30,
                          ),
                        )),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            ChatPanel(messages: _messages, onSend: _onSend),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _engagedTimer?.cancel();
    _pageController.dispose();
    _world.dispose();
    super.dispose();
  }
}
